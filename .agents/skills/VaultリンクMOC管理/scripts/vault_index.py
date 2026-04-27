import argparse
import json
import re
from pathlib import Path


EXCLUDE_DIRS = {".agents", ".git", "node_modules", ".obsidian", "public", "dist", "tmp"}
FRONTMATTER_RE = re.compile(r"\A\ufeff?---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def parse_scalar(value: str):
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value.strip('"\'')


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = {}
    current_key = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            data[key] = [] if value == "" else parse_scalar(value)
    return data


def iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def extract_note(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    fm = parse_frontmatter(text)
    headings = [m.group(2).strip() for m in HEADING_RE.finditer(text)]
    links = sorted(set(WIKILINK_RE.findall(text)))
    aliases = fm.get("aliases", [])
    tags = fm.get("tags", [])
    if isinstance(aliases, str):
        aliases = [aliases]
    if isinstance(tags, str):
        tags = [tags]
    title = fm.get("title") or (headings[0] if headings else path.stem)
    return {
        "title": title,
        "aliases": aliases,
        "tags": tags,
        "headings": headings,
        "wikilinks": links,
        "path": str(path.relative_to(root)).replace("\\", "/"),
    }


def build_index(root: Path) -> list:
    root = root.resolve()
    if not root.exists():
        return []
    return [extract_note(path, root) for path in iter_markdown(root)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="content")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root)
    notes = build_index(root)
    if args.json:
        print(json.dumps(notes, ensure_ascii=False, indent=2))
    else:
        for note in notes:
            print(f"{note['title']}\t{note['path']}")


if __name__ == "__main__":
    main()
