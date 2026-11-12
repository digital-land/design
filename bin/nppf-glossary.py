#!/usr/bin/env python3
"""Write a quotation for each entry in the NPPF Annex B glossary snapshot."""

import re
import sys
from datetime import date
from pathlib import Path

SNAPSHOT = Path(
    "content/snapshot/govuk-guidance-national-planning-policy-framework-annex-b-glossary.md"
)
URL = "https://www.gov.uk/guidance/national-planning-policy-framework-annex-b-glossary"
ENTRY = re.compile(r"^\*\*(.+?):\*\*(?:\s*\[\[footnote \d+\]\]\([^)]*\))?\s*(.*)$")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def entries(text):
    out, cur = [], None
    body = text.split("\n---\n", 1)[-1]
    for line in body.splitlines():
        m = ENTRY.match(line)
        if m:
            cur = [m.group(1).strip(), [m.group(2)]]
            out.append(cur)
        elif cur and line.startswith(("## ", "# ")):
            cur = None
        elif cur:
            cur[1].append(line)
    return [(n, "\n".join(b).strip()) for n, b in out]


def main():
    out = Path("content/quotation")
    today = date.today().isoformat()
    count = 0
    for name, text in entries(SNAPSHOT.read_text(encoding="utf-8")):
        if not text:
            continue
        s = slug(name)
        see = re.fullmatch(r"See (.+?)\.?", text)
        terms = [s]
        role = "definition"
        if see:
            role = "reference"
            text = f"See [{see.group(1)}](term/{slug(see.group(1))})."
        ref = f"nppf-annex-b-{s}"
        title = f"National Planning Policy Framework, Annex B: Glossary, {name}"
        (out / f"{ref}.md").write_text(
            "\n".join(
                [
                    "---",
                    f"reference: {ref}",
                    f'name: "{title}"',
                    f"url: {URL}",
                    "source-class: GOV.UK",
                    f"role: {role}",
                    "terms:",
                    *[f"- {t}" for t in terms],
                    f"entry-date: {today}",
                    "---",
                    "",
                    text,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        count += 1
    print(f"{count} quotations written", file=sys.stderr)


if __name__ == "__main__":
    main()
