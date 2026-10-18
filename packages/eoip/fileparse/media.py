"""Image metadata/optional local OCR and email body/attachment extraction."""

from __future__ import annotations

import io
from collections.abc import Iterator
from email import policy
from email.parser import BytesParser
from pathlib import Path
from tempfile import TemporaryDirectory

from eoip.fileparse.common import Extraction, dependency, json_cell
from eoip.fileparse.contracts import ParseError
from eoip.fileparse.text import VisibleHTML
from eoip.fileparse.tools import image_ocr


def parse_image(content: bytes, out: Extraction) -> None:
    image_module = dependency("PIL.Image")
    image_sequence = dependency("PIL.ImageSequence")
    try:
        with image_module.open(io.BytesIO(content)) as image:
            out.document.metadata.update(
                {"image_format": image.format, "width": image.width, "height": image.height, "mode": image.mode}
            )
            frame_count = getattr(image, "n_frames", 1)
            if image.width * image.height > out.options.max_image_pixels:
                raise ParseError("image_limit", "Image exceeds max_image_pixels")
            if frame_count > out.options.max_members:
                raise ParseError("member_limit", "Image frame count exceeds max_members")
            pixels = 0
            for index, frame in enumerate(image_sequence.Iterator(image), 1):
                pixels += frame.width * frame.height
                if pixels > out.options.max_image_pixels:
                    raise ParseError("image_limit", "Image frames exceed max_image_pixels")
                frame.load()
                if out.options.ocr:
                    png = io.BytesIO()
                    frame.convert("RGB").save(png, format="PNG")
                    out.section("ocr", image_ocr(png.getvalue(), out.options), frame=index, method="tesseract")
            out.document.metadata["frames"] = frame_count
            out.document.metadata["ocr_requested"] = out.options.ocr
            if not out.options.ocr:
                out.document.warnings.append("Image pixels were decoded; OCR is disabled, so no visual text is indexed")
            elif not out.document.sections:
                out.document.warnings.append("OCR completed but returned no text")
    except image_module.DecompressionBombError as exc:
        raise ParseError("image_limit", "Image exceeds the Pillow decompression-bomb limit") from exc


def email_members(content: bytes, suffix: str, out: Extraction) -> Iterator[tuple[str, bytes]]:
    if suffix == ".msg":
        if not out.options.enable_msg:
            raise ParseError("unlicensed_adapter", "MSG parsing is disabled under CRA-035 / Conflict X-16 licensing policy")
        errors = dependency("extract_msg.exceptions")
        try:
            yield from _email_members(content, suffix, out)
        except (errors.InvalidFileFormatError, errors.UnsupportedMSGTypeError) as exc:
            raise ParseError("invalid_email", "MSG is malformed or is not a supported Outlook message") from exc
    elif suffix == ".mbox":
        import mailbox
        with TemporaryDirectory(prefix="eoip-mbox-") as temporary:
            path = Path(temporary) / "input.mbox"
            path.write_bytes(content)
            mbox = mailbox.mbox(str(path))
            try:
                messages = [(f"message_{idx + 1}.eml", msg.as_bytes()) for idx, msg in enumerate(mbox)]
            finally:
                mbox.close()
        for name, msg_bytes in messages:
            yield name, msg_bytes
    else:
        yield from _email_members(content, suffix, out)


def _email_members(content: bytes, suffix: str, out: Extraction) -> Iterator[tuple[str, bytes]]:
    if suffix == ".msg":
        extract_msg = dependency("extract_msg")
        with TemporaryDirectory(prefix="eoip-msg-") as temporary:
            path = Path(temporary) / "input.msg"
            path.write_bytes(content)
            with extract_msg.Message(str(path)) as message:
                out.document.title = message.subject or out.document.title
                out.document.metadata.update(
                    {"subject": message.subject, "sender": message.sender, "to": message.to,
                     "date": json_cell(message.date)}
                )
                if message.body:
                    out.section("email_body", message.body, body_type="plain")
                elif message.htmlBody:
                    parser = VisibleHTML()
                    parser.feed(message.htmlBody.decode("utf-8"))
                    out.section("email_body", "".join(parser.parts), body_type="html")
                for index, attachment in enumerate(message.attachments):
                    if index >= out.options.max_members:
                        raise ParseError("member_limit", "MSG attachments exceed max_members")
                    data = attachment.data
                    if not isinstance(data, bytes):
                        raise ParseError("unsupported_attachment", "Embedded Outlook items require an explicit MSG export")
                    name = attachment.longFilename or attachment.shortFilename
                    if not name:
                        raise ParseError("invalid_attachment", "MSG attachment has no filename")
                    yield name, data
        return

    message = BytesParser(policy=policy.default).parsebytes(content)
    if not message.keys():
        raise ParseError("invalid_format", "EML has no message headers")
    out.document.title = str(message.get("Subject", "")) or out.document.title
    out.document.metadata["subject"] = str(message.get("Subject", ""))
    out.document.metadata["from"] = str(message.get("From", ""))
    out.document.metadata["to"] = str(message.get("To", ""))
    if "Cc" in message:
        out.document.metadata["cc"] = str(message.get("Cc", ""))
    if "Bcc" in message:
        out.document.metadata["bcc"] = str(message.get("Bcc", ""))
    out.document.metadata["date"] = str(message.get("Date", ""))
    out.document.metadata["message_id"] = str(message.get("Message-ID", ""))
    if "In-Reply-To" in message:
        out.document.metadata["in_reply_to"] = str(message.get("In-Reply-To", ""))
    if "References" in message:
        out.document.metadata["references"] = str(message.get("References", ""))
    out.document.metadata["headers"] = {str(key): str(value) for key, value in message.items()}
    parts = list(message.walk())
    if len(parts) > out.options.max_members:
        raise ParseError("member_limit", "Email MIME parts exceed max_members")
    for index, part in enumerate(parts):
        if part.defects:
            raise ParseError("invalid_email", f"Malformed MIME part {index}: {type(part.defects[0]).__name__}")
        if part.is_multipart():
            continue
        data = part.get_payload(decode=True)
        if not isinstance(data, bytes):
            raise ParseError("invalid_email", "MIME part cannot be decoded")
        name = part.get_filename()
        if name:
            yield name, data
        elif part.get_content_type() in {"text/plain", "text/html"}:
            try:
                text = data.decode(part.get_content_charset() or "utf-8", errors="strict")
            except (UnicodeDecodeError, LookupError) as exc:
                raise ParseError("invalid_encoding", "Email body charset is invalid") from exc
            if part.get_content_type() == "text/html":
                parser = VisibleHTML()
                parser.feed(text)
                text = "".join(parser.parts)
            out.section("email_body", text, mime_part=index, body_type=part.get_content_type())
        else:
            out.document.metadata.setdefault("unnamed_mime_parts", [])
            # Unnamed non-text parts must not silently disappear.
            yield f"part_{index}.{part.get_content_subtype()}", data
    out.document.metadata["headers"] = json_cell_map(message)


def json_cell_map(message) -> dict:
    return {str(key): json_cell(str(value)) for key, value in message.items()}
