"""Bounded streaming local recovery assets; never archive environment credentials."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath

import yaml
from eoip.snapshot import backup, restore, validate_restore

MAX_BYTES = 64 * 1024**3
MAX_FILES = 100_000
MAX_METADATA = 1024**2
MAX_SNAPSHOT = 256 * 1024**2
CHUNK = 1024**2
SHA256 = re.compile(r"[0-9a-f]{64}")
SECRET_KEYS = {
    "password", "token", "apitoken", "apikey", "accesstoken", "clientsecret", "secret",
    "authorization", "privatekey", "signingkey", "accesskey", "secretkey", "refreshtoken",
}


def _path(name: str) -> PurePosixPath:
    relative = PurePosixPath(name)
    if (
        not name or relative.is_absolute() or relative.as_posix() != name
        or any(part in {".", ".."} or any(char in part for char in '\\:<>\"|?*')
               or any(ord(char) < 32 for char in part)
               or part.endswith((".", " ")) or PureWindowsPath(part).is_reserved()
               for part in relative.parts)
    ):
        raise ValueError("Invalid recovery asset path")
    if name == "snapshot.json":
        return relative
    if relative.parts[0] == "config" and len(relative.parts) >= 2 and relative.suffix in {
        ".json", ".yaml", ".yml",
    }:
        return relative
    if (
        relative.parts[:2] == ("models", "blobs") and len(relative.parts) == 3
        and relative.name.startswith("sha256-") and SHA256.fullmatch(relative.name[7:])
    ):
        return relative
    if relative.parts[:2] == ("models", "manifests") and len(relative.parts) >= 3:
        return relative
    raise ValueError("Unsupported recovery asset path")


def _configuration(content: bytes, name: str) -> None:
    if len(content) > MAX_METADATA:
        raise ValueError("Recovery configuration exceeds metadata bound")
    document = json.loads(content) if name.endswith(".json") else yaml.safe_load(content)

    seen = set()
    checked = set()

    def check(value, depth=0):
        if depth > 100:
            raise ValueError("Recovery configuration exceeds nesting bound")
        if isinstance(value, (dict, list)):
            if id(value) in seen:
                raise ValueError("Recovery configuration contains recursive aliases")
            if id(value) in checked:
                return
            seen.add(id(value))
        if isinstance(value, dict):
            for key, item in value.items():
                if (
                    re.sub(r"[^a-z0-9]", "", str(key).lower()) in SECRET_KEYS
                    and item not in (None, "")
                    and (not isinstance(item, str) or not item.startswith(("env://", "vault://")))
                ):
                    raise ValueError("Recovery configuration must use secret references")
                check(item, depth + 1)
        elif isinstance(value, list):
            for item in value:
                check(item, depth + 1)
        if isinstance(value, (dict, list)):
            seen.remove(id(value))
            checked.add(id(value))

    check(document)


def _model_references(content: bytes) -> list[tuple[str, int]]:
    if len(content) > MAX_METADATA:
        raise ValueError("Recovery model manifest exceeds metadata bound")
    document = json.loads(content)
    if not isinstance(document, dict) or document.get("schemaVersion") != 2:
        raise ValueError("Unsupported recovery model manifest")
    layers = document.get("layers")
    if not isinstance(layers, list) or len(layers) > MAX_FILES:
        raise ValueError("Invalid recovery model layers")
    refs = []
    for entry in [document.get("config"), *layers]:
        if not isinstance(entry, dict):
            raise ValueError("Invalid recovery model reference in manifest")  # noqa: TRY004
        digest, size = entry.get("digest"), entry.get("size")
        if (
            not isinstance(digest, str) or not digest.startswith("sha256:")
            or not SHA256.fullmatch(digest[7:]) or type(size) is not int or size < 0
        ):
            raise ValueError("Invalid recovery model digest or size")
        refs.append((f"models/blobs/sha256-{digest[7:]}", size))
    return refs


def _references(records: dict, references: dict[str, int]) -> None:
    for name, size in references.items():
        if name not in records or records[name]["size"] != size:
            raise ValueError("Recovery model manifest references missing or mismatched weights")


def _add_references(references: dict[str, int], content: bytes) -> None:
    for name, size in _model_references(content):
        if name in references and references[name] != size:
            raise ValueError("Recovery model manifests disagree on weight size")
        references[name] = size
    if len(references) > MAX_FILES:
        raise ValueError("Recovery model references exceed file bound")


def _sources(root: Path, prefix: str):
    if not root.exists():
        if prefix == "config":
            raise ValueError("Recovery configuration directory is missing")
        return
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Invalid recovery asset directory")
    resolved = root.resolve()
    for path in root.rglob("*"):
        if path.is_symlink() or not path.resolve().is_relative_to(resolved):
            raise ValueError("Recovery asset symlinks are forbidden")
        if path.is_file():
            name = f"{prefix}/{path.relative_to(root).as_posix()}"
            _path(name)
            yield name, path
        elif not path.is_dir():
            raise ValueError("Recovery assets must be regular files or directories")


def backup_bundle(store, data_dir, destination, *, config_dir, model_dir, max_bytes=MAX_BYTES):
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_BYTES:
        raise ValueError("Invalid recovery bundle byte bound")
    destination = Path(destination)
    roots = [Path(data_dir).resolve(), Path(config_dir).resolve(), Path(model_dir).resolve()]
    if any(destination.resolve().is_relative_to(root) for root in roots[1:]):
        raise ValueError("Recovery bundle destination must be outside asset directories")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.TemporaryDirectory(prefix="eoip-recovery-") as staging:
            snapshot = Path(staging) / "snapshot.json"
            summary = backup(store, data_dir, snapshot)
            sources = [("snapshot.json", snapshot)]
            for root, prefix in ((Path(config_dir), "config"), (Path(model_dir), "models")):
                for asset in _sources(root, prefix):
                    if len(sources) >= MAX_FILES:
                        raise ValueError("Recovery bundle exceeds file bound")
                    sources.append(asset)
            records, references, total = {}, {}, 0
            folded_names = set()
            with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".tmp", delete=False) as handle:
                temporary = Path(handle.name)
            with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
                for name, source in sources:
                    if name.casefold() in folded_names:
                        raise ValueError("Recovery asset paths collide")
                    folded_names.add(name.casefold())
                    before = source.stat()
                    limit = MAX_SNAPSHOT if name == "snapshot.json" else MAX_METADATA
                    if not name.startswith("models/blobs/") and before.st_size > limit:
                        raise ValueError("Recovery metadata exceeds byte bound")
                    total += before.st_size
                    if total > max_bytes:
                        raise ValueError("Recovery bundle exceeds byte bound")
                    hasher, size = hashlib.sha256(), 0
                    metadata = bytearray()
                    with source.open("rb") as incoming, archive.open(name, "w", force_zip64=True) as output:
                        while chunk := incoming.read(CHUNK):
                            size += len(chunk)
                            if size > before.st_size:
                                raise ValueError("Recovery source changed during backup")
                            hasher.update(chunk)
                            output.write(chunk)
                            if name.startswith(("config/", "models/manifests/")):
                                metadata.extend(chunk)
                    after = source.stat()
                    if size != before.st_size or (
                        before.st_size, before.st_mtime_ns, before.st_ino, before.st_dev
                    ) != (
                        after.st_size, after.st_mtime_ns, after.st_ino, after.st_dev
                    ):
                        raise ValueError("Recovery source changed during backup")
                    sha = hasher.hexdigest()
                    if name.startswith("models/blobs/") and sha != source.name[7:]:
                        raise ValueError("Recovery model weight checksum mismatch")
                    if name.startswith("config/"):
                        _configuration(bytes(metadata), name)
                    elif name.startswith("models/manifests/"):
                        _add_references(references, bytes(metadata))
                    records[name] = {"size": size, "sha256": sha}
                _references(records, references)
                manifest = {
                    "schema_version": "1.0", "classification": "RESTRICTED", "files": records,
                    "model_blobs": sum(name.startswith("models/blobs/") for name in records),
                }
                encoded = json.dumps(manifest, separators=(",", ":")).encode()
                if len(encoded) > MAX_METADATA:
                    raise ValueError("Recovery bundle manifest exceeds byte bound")
                archive.writestr("bundle.json", encoded)
            with temporary.open("r+b") as handle:
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
            return {**summary, "file": str(destination), "asset_files": len(records) - 1,
                    "model_blobs": manifest["model_blobs"], "asset_bytes": total}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def restore_bundle(store, data_dir, source, *, config_dir, model_dir, max_bytes=MAX_BYTES):
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_BYTES:
        raise ValueError("Invalid recovery bundle byte bound")
    for value in (Path(config_dir), Path(model_dir)):
        if any(path.is_symlink() for path in (value, *value.parents)):
            raise ValueError("Recovery asset target symlinks are forbidden")
    targets = {"config": Path(config_dir).resolve(), "models": Path(model_dir).resolve()}
    data = Path(data_dir).resolve()
    if any(path == data or path.is_relative_to(data) or data.is_relative_to(path)
           for path in targets.values()) or (
        targets["config"].is_relative_to(targets["models"])
        or targets["models"].is_relative_to(targets["config"])
    ):
        raise ValueError("Recovery targets must be separate directories")
    for value in targets.values():
        if value.exists() and (not value.is_dir() or any(value.iterdir())):
            raise ValueError("Recovery requires empty configuration and model targets")
    with tempfile.TemporaryDirectory(prefix="eoip-recovery-") as temporary:
        staging = Path(temporary)
        with zipfile.ZipFile(source) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(infos) > MAX_FILES + 1 or len({name.casefold() for name in names}) != len(names):
                raise ValueError("Recovery bundle contains duplicate or excessive files")
            if any(stat.S_ISLNK(info.external_attr >> 16) or info.is_dir() for info in infos):
                raise ValueError("Recovery bundle symlinks and directory entries are forbidden")
            if "bundle.json" not in names or archive.getinfo("bundle.json").file_size > MAX_METADATA:
                raise ValueError("Missing or oversized recovery bundle manifest")
            manifest = json.loads(archive.read("bundle.json"))
            if (
                not isinstance(manifest, dict)
                or set(manifest) != {"schema_version", "classification", "files", "model_blobs"}
                or manifest["schema_version"] != "1.0" or manifest["classification"] != "RESTRICTED"
                or not isinstance(manifest["files"], dict)
            ):
                raise ValueError("Invalid recovery bundle manifest")
            records = manifest["files"]
            if set(names) != {"bundle.json", *records} or "snapshot.json" not in records:
                raise ValueError("Recovery bundle files differ from manifest")
            total, references = 0, {}
            for info in infos:
                if info.filename == "bundle.json":
                    continue
                name = info.filename
                relative = _path(name)
                record = records[name]
                if (
                    stat.S_ISLNK(info.external_attr >> 16) or info.is_dir()
                    or not isinstance(record, dict) or set(record) != {"size", "sha256"}
                    or type(record["size"]) is not int or record["size"] < 0
                    or record["size"] != info.file_size or not isinstance(record["sha256"], str)
                    or not SHA256.fullmatch(record["sha256"])
                ):
                    raise ValueError("Invalid recovery bundle asset metadata")
                total += info.file_size
                limit = MAX_SNAPSHOT if name == "snapshot.json" else MAX_METADATA
                if total > max_bytes or (not name.startswith("models/blobs/") and info.file_size > limit):
                    raise ValueError("Recovery bundle exceeds byte bound")
                output = staging.joinpath(*relative.parts)
                output.parent.mkdir(parents=True, exist_ok=True)
                hasher, size = hashlib.sha256(), 0
                with archive.open(info) as incoming, output.open("wb") as handle:
                    while chunk := incoming.read(CHUNK):
                        size += len(chunk)
                        if size > info.file_size:
                            raise ValueError("Recovery bundle asset exceeds declared size")
                        handle.write(chunk)
                        hasher.update(chunk)
                if size != info.file_size or hasher.hexdigest() != record["sha256"]:
                    raise ValueError("Recovery bundle asset checksum mismatch")
                if name.startswith("models/blobs/") and record["sha256"] != relative.name[7:]:
                    raise ValueError("Recovery model weight checksum mismatch")
                if name.startswith("config/"):
                    _configuration(output.read_bytes(), name)
                elif name.startswith("models/manifests/"):
                    _add_references(references, output.read_bytes())
            _references(records, references)
            blobs = sum(name.startswith("models/blobs/") for name in records)
            if type(manifest["model_blobs"]) is not int or manifest["model_blobs"] != blobs:
                raise ValueError("Recovery model blob count mismatch")
        validate_restore(store, data_dir, staging / "snapshot.json")
        result = restore(store, data_dir, staging / "snapshot.json")
        for group, target in targets.items():
            target.mkdir(parents=True, exist_ok=True)
            for path in (staging / group).rglob("*"):
                if path.is_file():
                    destination = target / path.relative_to(staging / group)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with path.open("rb") as incoming, destination.open("xb") as output:
                        while chunk := incoming.read(CHUNK):
                            output.write(chunk)
                        output.flush()
                        os.fsync(output.fileno())
        return {**result, "asset_files": len(records) - 1, "model_blobs": blobs}
