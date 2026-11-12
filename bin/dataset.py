#!/usr/bin/env python3
"""Compile the markdown files in each content directory into dataset/<name>.csv."""

import csv
import re
import sys
from pathlib import Path

import yaml

CONTENT = Path("content")
OUT = Path("dataset")


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}, path.read_text(encoding="utf-8")
    return yaml.safe_load(m.group(1)) or {}, m.group(2).strip()


def main():
    OUT.mkdir(exist_ok=True)
    for d in sorted(p for p in CONTENT.iterdir() if p.is_dir()):
        rows = []
        for f in sorted(d.glob("*.md")):
            fm, body = read(f)
            fm = {
                k: "; ".join(map(str, v)) if isinstance(v, list) else v
                for k, v in fm.items()
            }
            rows.append({**fm, "text": body})
        if not rows:
            continue
        fields = []
        for r in rows:
            fields += [k for k in r if k not in fields]
        with open(OUT / f"{d.name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"{d.name}: {len(rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
