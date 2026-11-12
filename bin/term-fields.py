#!/usr/bin/env python3
"""Add `definition` (a CURIE for the page holding the definition) and `quotation` (the reference of its quotation) to terms.

The quotation is found by matching the term's `documentation-url` to a quotation file.
"""

import re
import sys
from pathlib import Path

CONTENT = Path("content")
HOSTS = (
    ("https://www.legislation.gov.uk/", "legislation"),
    ("http://www.legislation.gov.uk/id/", "legislation"),
    ("https://www.gov.uk/", "govuk"),
)


# terms whose glossary entry only says "See <term>"
ALIASES = {"brownfield-land": "previously-developed-land"}


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    return m.group(1), m.group(2)


def field(head, key):
    m = re.search(rf"^{key}: *(.*)$", head, re.M)
    return m.group(1).strip().strip('"') if m else ""


def curie(url):
    """legislation:ukpga/1990/8/section/55 or govuk:guidance/viability, without any fragment."""
    url = url.split("#")[0]
    for host, prefix in HOSTS:
        if url.startswith(host):
            ref = url[len(host):].strip("/")
            ref = re.sub(r"/(made|enacted)$", "", ref)
            return f"{prefix}:{ref}"
    return ""


def quotations():
    out = {}
    for p in sorted((CONTENT / "quotation").rglob("*.md")):
        head, _ = read(p)
        if field(head, "role") != "definition":
            continue
        url = field(head, "url").split("#")[0]
        terms = re.findall(r"^- (.+)$", head.split("terms:", 1)[-1], re.M)
        for t in terms:
            out.setdefault((t, url), field(head, "reference"))
    return out


def main():
    quotes = quotations()
    missing = []
    for f in sorted((CONTENT / "term").glob("*.md")):
        head, body = read(f)
        if field(head, "term-status") not in ("legislation", "guidance"):
            continue
        url = field(head, "documentation-url")
        ref = quotes.get((ALIASES.get(f.stem, f.stem), url.split("#")[0]))
        if not ref:
            missing.append(f.stem)
            continue
        lines = [l for l in head.splitlines()]
        keep, skip = [], False
        for l in lines:  # drop any previous definition and quotation fields
            if l.startswith(("definition:", "quotation:")):
                skip = l.startswith("quotation:")
                continue
            if skip and (l.startswith(" ") or not l.strip()):
                continue
            skip = False
            keep.append(l)
        at = max(
            [i for i, l in enumerate(keep) if l.startswith(("documentation-url:", "legislation:"))]
        )
        keep[at + 1 : at + 1] = [f"definition: {curie(url)}", f"quotation: {ref}"]
        f.write_text("---\n" + "\n".join(keep) + "\n---\n" + body, encoding="utf-8")
    print(f"{len(missing)} terms without a matching quotation: {' '.join(missing)}", file=sys.stderr)


if __name__ == "__main__":
    main()
