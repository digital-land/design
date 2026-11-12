#!/usr/bin/env python3
"""Create a term for each term with quotations, using the most authoritative definition.

Precedence: a general definition from legislation, then the NPPF glossary.
Existing term files are never changed.
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

CONTENT = Path("content")
NARROW = re.compile(
    r"\b(in this (section|Part|Chapter|Schedule|regulation|article|paragraph)|"
    r"for the purposes? of|in sections?|in relation to|in subsection)\b",
    re.I,
)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def yaml(s):
    return '"' + s.replace('"', '\\"') + '"' if re.search(r"[:#\"'\[\]{}]|^\W", s) else s


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    fm = {}
    key = None
    for line in m.group(1).splitlines():
        if line.startswith("- ") and key:
            fm.setdefault(key, []).append(line[2:].strip())
        elif ": " in line or line.endswith(":"):
            key, _, v = line.partition(":")
            fm[key] = v.strip().strip('"') or []
    return fm, m.group(2).strip()


def score(fm, body):
    n = 0
    first = body.lstrip()[:1]
    n += 3 if first in "“\"" else 0
    n -= 3 if NARROW.search(body[:200]) else 0
    n -= 1 if not re.search(r"\bmeans\b", body) else 0
    n += 1 if "/ukpga/" in fm["url"] else 0
    n += 1 if "/ukpga/1990/8/" in fm["url"] else 0
    return n


def clean(text, term):
    """Remove the link to the term itself from a quotation."""
    text = re.sub(r"\[([^\]]*)\]\(term/" + re.escape(term) + r"\)", r"\1", text)
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)


def deleted():
    """Terms removed from the repository on purpose; do not recreate them."""
    log = subprocess.run(
        ["git", "log", "--diff-filter=D", "--name-only", "--format=", "--", "content/term"],
        capture_output=True,
        text=True,
    ).stdout
    return {Path(l).stem for l in log.split()}


def main():
    skip = deleted()
    quotes = {}
    for p in sorted((CONTENT / "quotation").glob("*.md")):
        fm, body = read(p)
        for t in fm.get("terms", []):
            quotes.setdefault(t, []).append((fm, body))
    today = date.today().isoformat()
    created, unresolved = 0, []
    for term, qs in sorted(quotes.items()):
        out = CONTENT / "term" / f"{term}.md"
        if out.exists() or term in skip:
            continue
        leg = [
            (score(fm, b), fm, b)
            for fm, b in qs
            if fm.get("role") == "definition" and fm.get("source-class") == "legislation"
        ]
        leg = [x for x in leg if x[0] >= 0]
        nppf = [
            (fm, b)
            for fm, b in qs
            if fm.get("role") == "definition" and fm.get("source-class") == "GOV.UK"
        ]
        if leg:
            _, fm, body = max(leg, key=lambda x: (x[0], len(x[2])))
            status = "legislation"
            text = clean(body, term)
            m = re.search(r"\[([^\]]*)\]\(term/" + re.escape(term) + r"\)", body)
            name = m.group(1) if m else term.replace("-", " ")
        elif nppf:
            fm, body = nppf[0]
            status = "guidance"
            text = body
            name = fm["name"].split("Glossary, ", 1)[-1]
        else:
            unresolved.append(term)
            continue
        name = name[:1].upper() + name[1:]
        out.write_text(
            "\n".join(
                [
                    "---",
                    f"reference: {term}",
                    f"name: {yaml(name)}",
                    f"term-status: {status}",
                    f"documentation-url: {fm['url']}",
                    f"entry-date: {today}",
                    "---",
                    "",
                    text,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        created += 1
    print(f"{created} terms created; {len(unresolved)} without a definition", file=sys.stderr)
    (Path("var") / "unresolved-terms.txt").write_text("\n".join(unresolved) + "\n")


if __name__ == "__main__":
    main()
