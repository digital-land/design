#!/usr/bin/env python3
"""Remove unanswered discovery questions, and then empty stage headings, from each topic."""

import re
from pathlib import Path

UNANSWERED = {
    "",
    "n/a",
    "n / a",
    "na",
    "-",
    "unknown",
    "tbc",
    "tbd",
    "none",
    "not known",
    "not applicable",
    "as per above",
    "?",
}


def strip(body):
    parts = re.split(r"(?m)^(?=#{2,3} )", body)
    out, heading, kept = [], None, 0
    # a heading is kept only if something remains under it
    for part in parts:
        if part.startswith("### "):
            _, _, answer = part.partition("\n")
            if answer.strip().rstrip(".").lower() in UNANSWERED:
                continue
            kept += 1
            out.append(part)
        elif part.startswith("## "):
            out.append(part)
        else:
            out.append(part)
    # drop H2 headings with nothing under them
    result = []
    for i, part in enumerate(out):
        if part.startswith("## ") and not part.partition("\n")[2].strip():
            nxt = out[i + 1] if i + 1 < len(out) else ""
            if not nxt.startswith("### "):
                continue
        result.append(part)
    return "".join(result).strip()


def main():
    for p in sorted(Path("content/topic").glob("*.md")):
        m = re.match(r"(---\n.*?\n---\n)\n?(.*)", p.read_text(encoding="utf-8"), re.S)
        head, body = m.groups()
        new = strip(body)
        p.write_text(f"{head}\n{new}\n" if new else head, encoding="utf-8")


if __name__ == "__main__":
    main()
