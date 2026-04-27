import argparse
from datetime import date
from pathlib import Path


BEGIN = "<!-- AUTO-GENERATED:BEGIN related-notes -->"
END = "<!-- AUTO-GENERATED:END related-notes -->"


def ensure_block(text: str) -> str:
    if BEGIN in text and END in text:
        return text
    if not text.endswith("\n"):
        text += "\n"
    return text + f"\n{BEGIN}\n{END}\n"


def add_link_to_moc(moc_path: Path, link: str) -> bool:
    moc_path.parent.mkdir(parents=True, exist_ok=True)
    if moc_path.exists():
        text = moc_path.read_text(encoding="utf-8")
    else:
        title = moc_path.stem
        today = date.today().isoformat()
        text = (
            "---\n"
            f'title: "{title}"\n'
            f'description: "{title} に関するノートの入口。"\n'
            "aliases: []\n"
            "tags:\n"
            "  - 種類/MOC\n"
            "draft: false\n"
            "publish: true\n"
            f'created: "{today}"\n'
            f'updated: "{today}"\n'
            "enableToc: true\n"
            "---\n\n"
            f"# {title}\n"
        )
    text = ensure_block(text)
    item = f"- [[{link}]]"
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END)
    block = text[start:end]
    if item in block:
        return False
    lines = [line for line in block.splitlines() if line.strip()]
    lines.append(item)
    lines = sorted(set(lines))
    new_block = "\n" + "\n".join(lines) + "\n"
    new_text = text[:start] + new_block + text[end:]
    moc_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--moc", required=True)
    parser.add_argument("--link", required=True)
    args = parser.parse_args()
    changed = add_link_to_moc(Path(args.moc), args.link)
    print("updated" if changed else "already present")


if __name__ == "__main__":
    main()
