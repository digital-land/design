#!/usr/bin/env python3
"""Replace references in markdown body text with doctate links.

See https://github.com/psd/doctate. A reference is written `[text][prefix:key]` and the
`[prefix:key]: /path` definitions are listed at the end of the file:

    [England][term:england]          [term:england]: /term/england
    [CIL][abbreviation:cil]          [abbreviation:cil]: /abbreviation/cil
    [... Act 1990][legislation:ukpga/1990/8]   [legislation:ukpga/1990/8]: /legislation/ukpga/1990/8
    [Viability][govuk:guidance/viability]      [govuk:guidance/viability]: /govuk/guidance/viability

Existing links to entities are converted, then plain-text mentions of legislation, multi-word
terms, GOV.UK page titles and abbreviations are linked. Run again at any time: it is idempotent.
"""

import re
import sys
from pathlib import Path

CONTENT = Path("content")
DATASETS = {p.name for p in CONTENT.iterdir() if p.is_dir()}
TARGETS = ("term", "term-status", "abbreviation", "quotation", "dataset", "field", "user", "legislation", "govuk")
DEFINITION = re.compile(r"^\[([a-z-]+:[^\]\s]+)\]: (\S+)\s*$")
# links, reference links, inline code, HTML, bare URLs: left alone when linking plain text
PROTECT = re.compile(
    r"\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\[[^\]]*\]|`[^`]*`|<[^>]+>|https?://\S+|^\[[^\]]+\]: .*$|^#+ .*$",
    re.M,
)
LEGISLATION_URL = re.compile(
    r"^https?://www\.legislation\.gov\.uk/(?:id/)?((?:ukpga|uksi|asp|anaw|asc|nia|ukla|wsi|ssi)/\d{4}/\d+)"
    r"(?:/(?:made|enacted|contents|contents/made|data\.\w+))?(#[\w-]+)?/?$"
)
GOVUK_URL = re.compile(r"^https://www\.gov\.uk(/[^\s#]*?)/?(#[\w-]+)?$")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def front(path):
    m = re.match(r"(---\n.*?\n---\n?)(.*)", path.read_text(encoding="utf-8"), re.S)
    return (m.group(1), m.group(2)) if m else ("", path.read_text(encoding="utf-8"))


def field(head, key):
    m = re.search(rf"^{key}: *(.*)$", head, re.M)
    return m.group(1).strip().strip('"\'') if m else ""


class Index:
    """The entities that can be linked to."""

    def __init__(self):
        self.files = {d: {p.stem for p in (CONTENT / d).rglob("*.md")} for d in DATASETS}
        self.legislation, self.govuk = {}, {}
        self.terms, self.abbreviations, self.titles = {}, {}, {}
        for p in (CONTENT / "legislation").glob("*.md"):
            head, _ = front(p)
            self.legislation[field(head, "reference")] = field(head, "name")
        for p in (CONTENT / "govuk").glob("*.md"):
            head, _ = front(p)
            ref = field(head, "reference").strip("/")
            self.govuk[ref] = field(head, "name")
        for p in (CONTENT / "term").glob("*.md"):
            head, _ = front(p)
            for key in ("name", "plural"):
                n = field(head, key)
                if n and len(n.split()) > 1:
                    self.terms[n.lower()] = p.stem
        for p in (CONTENT / "abbreviation").glob("*.md"):
            a = field(*[front(p)[0], "reference"])
            if len(a) > 2:
                self.abbreviations[a] = p.stem

    def target(self, label):
        prefix, _, key = label.partition(":")
        path = key.split("#")[0]
        if prefix == "legislation":
            ok = path in self.legislation
        elif prefix == "govuk":
            ok = path in self.govuk
        else:
            ok = slug(path) in {slug(s) for s in self.files.get(prefix, ())}
        return ok

    def url(self, label):
        prefix, _, key = label.partition(":")
        return f"/{prefix}/{key}"


def convert_links(body, index, defs):
    """Existing links to entities, `[x](term/y)` or a legislation.gov.uk or gov.uk URL."""

    def sub(m):
        text, url = m.group(1), m.group(2).strip()
        label = None
        if (r := re.fullmatch(r"/?([a-z-]+)/([^)\s#]+)", url)) and r.group(1) in TARGETS:
            kind, key = r.group(1), r.group(2)
            if kind in ("term", "quotation", "dataset", "field", "term-status", "user"):
                label = f"{kind}:{key}"
            elif kind == "abbreviation":
                label = f"abbreviation:{key.lower()}"
        elif r := LEGISLATION_URL.match(url):
            if r.group(1) in index.legislation:
                label = f"legislation:{r.group(1)}{r.group(2) or ''}"
        elif r := GOVUK_URL.match(url):
            ref = r.group(1).strip("/")
            if ref in index.govuk:
                label = f"govuk:{ref}{r.group(2) or ''}"
        if not label:
            return m.group(0)
        defs[label] = index.url(label)
        return f"[{text}][{label}]"

    return re.sub(r"\[([^\]\[]+)\]\(([^)\s]+)\)", sub, body)


def link_mentions(body, index, defs, own):
    """Link plain-text mentions of legislation, multi-word terms, GOV.UK titles and abbreviations."""
    held = []

    def hold(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    body = PROTECT.sub(hold, body)

    def link(pattern, label, text_of=lambda m: m.group(0), first=False, flags=0):
        nonlocal body

        def sub(m):
            defs[label] = index.url(label)
            return hold_text(f"[{text_of(m)}][{label}]")

        def hold_text(s):
            held.append(s)
            return f"\x00{len(held) - 1}\x00"

        body = re.sub(pattern, sub, body, count=1 if first else 0, flags=flags)

    for ref, name in sorted(index.legislation.items(), key=lambda kv: -len(kv[1])):
        for n in {name, re.sub(r"^The ", "", name)}:
            if len(n) > 12 and n in body:
                link(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", f"legislation:{ref}")
    for name, stem in sorted(index.terms.items(), key=lambda kv: -len(kv[0])):
        if stem == own or f"term:{stem}" in defs and False:
            continue
        link(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", f"term:{stem}", first=True, flags=re.I)
    for ref, name in sorted(index.govuk.items(), key=lambda kv: -len(kv[1])):
        if len(name.split()) > 2 and len(name) > 14 and name.lower() not in index.terms:
            link(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", f"govuk:{ref}", first=True)
    for abbr, stem in index.abbreviations.items():
        link(r"(?<![\w-])" + re.escape(abbr) + r"(?![\w-])", f"abbreviation:{stem}", first=True)
    # restore held text, which may itself hold earlier placeholders
    for _ in range(4):
        body = re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], body)
    return body


def process(path, index):
    head, body = front(path)
    if not head:
        return False
    lines = body.rstrip("\n").split("\n")
    while lines and (DEFINITION.match(lines[-1]) or not lines[-1].strip()):
        lines.pop()  # drop the old definitions: they are regenerated
    text = "\n".join(lines)
    defs = {}
    own = path.stem if path.parent.name == "term" else None
    # definitions of labels already used in reference links
    text = convert_links(text, index, defs)
    text = link_mentions(text, index, defs, own)
    used = set(re.findall(r"\]\[([a-z-]+:[^\]\s]+)\]", text))
    out = text
    if used:
        out += "\n\n" + "\n".join(f"[{l}]: {index.url(l)}" for l in sorted(used))
    out = out.strip("\n") + "\n"
    if head + ("\n" if not head.endswith("\n\n") and body.startswith("\n") else "") + out == head + body:
        return False
    path.write_text(head + ("\n" if body.startswith("\n") else "") + out, encoding="utf-8")
    return True


def main():
    index = Index()
    dirs = ("term", "quotation", "dataset", "field", "abbreviation", "term-status")
    changed = 0
    for d in dirs:
        for p in sorted((CONTENT / d).rglob("*.md")):
            changed += process(p, index)
    print(f"{changed} files changed", file=sys.stderr)


if __name__ == "__main__":
    main()
