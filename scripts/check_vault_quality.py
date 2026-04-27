from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "title",
    "description",
    "aliases",
    "tags",
    "created",
    "updated",
    "draft",
    "publish",
    "status",
    "enableToc",
}

FRONTMATTER_ORDER = [
    "title",
    "description",
    "aliases",
    "tags",
    "created",
    "updated",
    "draft",
    "publish",
    "status",
    "enableToc",
]

REQUIRED_SECTIONS = [
    "関連ノート候補",
    "MOC更新候補",
    "参考文献",
    "未解決問題",
    "更新ログ",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def frontmatter_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---", 4)
    if end < 0:
        return set()
    keys: set[str] = set()
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            keys.add(line.split(":", 1)[0].strip())
    return keys


def frontmatter_key_order(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---", 4)
    if end < 0:
        return []
    keys: list[str] = []
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            keys.append(line.split(":", 1)[0].strip())
    return keys


def image_links(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)


def citation_numbers(text: str) -> set[str]:
    return set(re.findall(r"\[(\d+)\]", text))


def reference_numbers(text: str) -> set[str]:
    refs = re.search(r"##\s*参考文献(?P<body>.*?)(?:\n##\s+|\Z)", text, re.S)
    if not refs:
        return set()
    return set(re.findall(r"^\[(\d+)\]", refs.group("body"), re.M))


def check_file(path: Path, root: Path) -> list[str]:
    text = read_text(path)
    issues: list[str] = []

    missing_fm = REQUIRED_FRONTMATTER - frontmatter_keys(text)
    if missing_fm:
        issues.append("missing frontmatter: " + ", ".join(sorted(missing_fm)))

    key_order = frontmatter_key_order(text)
    if key_order and key_order[: len(FRONTMATTER_ORDER)] != FRONTMATTER_ORDER:
        issues.append("frontmatter order differs from standard")

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            issues.append(f"missing section: {section}")

    imgs = image_links(text)
    for img in imgs:
        candidate = (path.parent / img).resolve() if not img.startswith("content/") else (root.parent / img).resolve()
        try:
            candidate.relative_to(root.parent.resolve())
        except ValueError:
            issues.append(f"image outside workspace: {img}")
            continue
        if not candidate.exists():
            issues.append(f"missing image file: {img}")

    cites = citation_numbers(text)
    refs = reference_numbers(text)
    if not refs:
        issues.append("missing numbered references")
    elif not (cites & refs):
        issues.append("no in-text citation matching references")

    if "教育・研究目的" not in text and ("精神医学" in str(path) or "精神科" in text or "疾患" in str(path)):
        issues.append("medical/psychiatric note lacks education-purpose disclaimer")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="content")
    args = parser.parse_args()
    root = Path(args.root)
    markdown_files = sorted(root.rglob("*.md"))

    total_issues = 0
    for path in markdown_files:
        issues = check_file(path, root)
        if issues:
            total_issues += len(issues)
            rel = path.as_posix()
            print(f"\n{rel}")
            for issue in issues:
                print(f"  - {issue}")

    print(f"\nchecked={len(markdown_files)} issues={total_issues}")
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
