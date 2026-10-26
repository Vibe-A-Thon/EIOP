"""Render every help PDF page and inspect DOCX structural/content parity."""

from pathlib import Path
import json

from docx import Document
from PIL import Image, ImageDraw
import pymupdf


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "self-help-manual" / "docs"
PREVIEW = ROOT / ".audit-scratch" / "manual-preview"
PREVIEW.mkdir(parents=True, exist_ok=True)
results = []

for pdf in sorted(DOCS.glob("*.pdf")):
    doc = pymupdf.open(pdf)
    docx_path = pdf.with_suffix(".docx")
    word = Document(docx_path)
    word_text = " ".join(p.text for p in word.paragraphs)
    pages = []
    for n, page in enumerate(doc, 1):
        text = page.get_text()
        if len(text.strip()) < 30:
            raise RuntimeError(f"Nearly blank PDF page: {pdf.name} page {n}")
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.25, 1.25), alpha=False)
        output = PREVIEW / f"{pdf.stem}-page-{n}.png"
        pix.save(output)
        pages.append(output)
    if not word.inline_shapes:
        raise RuntimeError(f"No screenshot in DOCX: {docx_path.name}")
    if not word_text.strip() or pdf.stem.replace("-", " ").split()[0].lower() not in word_text.lower():
        raise RuntimeError(f"DOCX appears empty: {docx_path.name}")
    results.append({"name": pdf.name, "pages": len(pages), "docx_images": len(word.inline_shapes), "pdf_images": sum(len(p.get_images()) for p in doc)})
    thumbs = []
    for source in pages:
        image = Image.open(source).convert("RGB")
        image.thumbnail((600, 780))
        tile = Image.new("RGB", (630, 820), "#eef3f5")
        tile.paste(image, ((630-image.width)//2, 10))
        draw = ImageDraw.Draw(tile)
        draw.text((18, 795), source.stem, fill="#24434e")
        thumbs.append(tile)
    columns = 2
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns*630, rows*820), "#d7e2e6")
    for i, tile in enumerate(thumbs):
        sheet.paste(tile, ((i%columns)*630, (i//columns)*820))
    sheet.save(PREVIEW / f"{pdf.stem}-contact.png")

print(json.dumps(results, indent=2))
