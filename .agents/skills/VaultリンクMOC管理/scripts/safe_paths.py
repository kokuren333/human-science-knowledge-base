from pathlib import Path
import re
import unicodedata


WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}
INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1f]'


def sanitize_filename(title: str) -> str:
    name = unicodedata.normalize("NFC", str(title or "")).strip()
    name = re.sub(INVALID_CHARS, "", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if not name:
        name = "untitled"
    stem = name.split(".")[0].upper()
    if stem in WINDOWS_RESERVED:
        name = f"{name}-note"
    return name[:120].rstrip(" .") or "untitled"


def safe_join(root: Path, *parts: str) -> Path:
    root = Path(root).resolve()
    cleaned = [sanitize_filename(part) for part in parts if str(part) not in ("", ".")]
    path = root.joinpath(*cleaned).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes root: {path}")
    return path


def unique_path(path: Path) -> Path:
    path = Path(path)
    if not path.exists():
        return path
    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    counter = 2
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
