#!/usr/bin/env python3
"""Seed content/dataset, content/field and draft terms from a checkout of digital-land/specification."""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

CONTENT = Path("content")


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}, path.read_text(encoding="utf-8").strip()
    return yaml.safe_load(m.group(1)) or {}, m.group(2).strip()


def write(path, fm, body=""):
    fm = {k: v for k, v in fm.items() if v not in ("", None, [])}
    text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text(f"---\n{text}---\n\n{body}\n" if body else f"---\n{text}---\n", encoding="utf-8")


def main(spec):
    today = date.today().isoformat()
    terms = {p.stem for p in (CONTENT / "term").glob("*.md")}
    for kind in ("dataset", "field"):
        out = CONTENT / kind
        out.mkdir(exist_ok=True)
        for p in sorted((spec / "content" / kind).glob("*.md")):
            fm, body = read(p)
            ref = fm.pop(kind, p.stem)
            if ref != ref.lower():  # legacy duplicates differing only by case
                continue
            new = {"reference": ref, "name": fm.pop("name", ""), "plural": fm.pop("plural", "")}
            if ref in terms:
                new["term"] = ref
            new.update(fm)
            entry = str(new.get("entry-date") or today)
            m = re.fullmatch(r"(\d\d)-(\d\d)-(\d{4})", entry)
            new["entry-date"] = f"{m[3]}-{m[2]}-{m[1]}" if m else entry
            write(out / f"{ref}.md", new, body)
            if kind == "dataset" and ref not in terms and fm.get("description"):
                desc = fm["description"].strip()
                write(
                    CONTENT / "term" / f"{ref}.md",
                    {
                        "reference": ref,
                        "name": new["name"],
                        "plural": new.get("plural", ""),
                        "term-status": "draft",
                        "entry-date": today,
                    },
                    desc[:1].upper() + desc[1:],
                )
                new["term"] = ref
                write(out / f"{ref}.md", new, body)
                terms.add(ref)
    print("seeded", file=sys.stderr)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
