#!/usr/bin/env python3
"""Find where each term is used in the snapshots and write dataset/term-usage.csv."""

import csv
import re
from pathlib import Path

import yaml

CONTENT = Path("content")


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, "")


def main():
    terms = {}
    for f in sorted((CONTENT / "term").glob("*.md")):
        fm, _ = read(f)
        names = {fm.get("name"), fm.get("plural"), f.stem.replace("-", " ")}
        names = sorted({n for n in names if n and len(n) > 3}, key=len, reverse=True)
        if names:
            terms[f.stem] = re.compile(
                r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])",
                re.I,
            )
    rows = []
    for f in sorted((CONTENT / "govuk").glob("*.md")):
        fm, body = read(f)
        for term, pattern in terms.items():
            n = len(pattern.findall(body))
            if n:
                rows.append(
                    {
                        "term": term,
                        "source-dataset": "govuk",
                        "source-reference": fm.get("reference", f.stem),
                        "document-url": fm.get("document-url", ""),
                        "count": n,
                    }
                )
    Path("dataset").mkdir(exist_ok=True)
    with open("dataset/term-usage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["term", "source-dataset", "source-reference", "document-url", "count"],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} uses of {len({r['term'] for r in rows})} terms")


if __name__ == "__main__":
    main()
