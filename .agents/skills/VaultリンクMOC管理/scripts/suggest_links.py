import argparse
from collections import Counter
from pathlib import Path

from vault_index import build_index


def ngrams(text: str, n: int = 2) -> Counter:
    text = "".join(str(text or "").split()).lower()
    return Counter(text[i:i + n] for i in range(max(0, len(text) - n + 1)))


def score_note(query_text: str, query_tags: set, note: dict) -> tuple[float, list[str]]:
    haystack = " ".join([
        str(note.get("title", "")),
        " ".join(note.get("aliases", [])),
        " ".join(note.get("tags", [])),
        " ".join(note.get("headings", [])),
    ])
    q = ngrams(query_text)
    h = ngrams(haystack)
    overlap = sum(min(count, h.get(token, 0)) for token, count in q.items())
    tag_overlap = query_tags.intersection(set(note.get("tags", [])))
    score = overlap + 8 * len(tag_overlap)
    reasons = []
    if overlap:
        reasons.append("タイトル・見出し・alias の文字 n-gram が重なる")
    if tag_overlap:
        reasons.append("タグが重なる: " + ", ".join(sorted(tag_overlap)))
    return float(score), reasons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="content")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    query_tags = {tag.strip() for tag in args.tags.split(",") if tag.strip()}
    query_text = f"{args.title} {args.summary} {' '.join(query_tags)}"
    scored = []
    for note in build_index(Path(args.root)):
        score, reasons = score_note(query_text, query_tags, note)
        if score > 0:
            scored.append((score, note, reasons))
    scored.sort(key=lambda item: item[0], reverse=True)
    for score, note, reasons in scored[:args.limit]:
        print(f"- [[{note['title']}]] ({score:.1f}) - {note['path']}")
        print(f"  理由: {'; '.join(reasons)}")


if __name__ == "__main__":
    main()
