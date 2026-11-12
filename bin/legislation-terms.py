#!/usr/bin/env python3
"""Extract definitions of terms from legislation.gov.uk XML as quotations."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
legislation2md = __import__("legislation2md")
LEG = legislation2md.LEG


UNIT = re.compile(r"(section|regulation|article|rule)-")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def yaml(s):
    s = str(s)
    return '"' + s.replace('"', '\\"') + '"' if re.search(r"[:#\"'\[\]{}]", s) else s


def instrument(path, legislation):
    """Reference, title and start-date for the instrument cached as <path>."""
    ref = path.stem.replace("-", "/", 2)
    meta = legislation / f"{path.stem}.md"
    title, start = ref, ""
    if meta.exists():
        for line in meta.read_text().splitlines():
            if line.startswith("name: "):
                title = line[6:].strip('"')
            if line.startswith("start-date: "):
                start = line[12:]
    return ref, title, start


def definitions(root, wanted):
    """Yield (term, section id, subsection id, element) for each defining Text."""
    parent = {c: p for p in root.iter() for c in p}
    for t in root.iter(LEG + "Term"):
        name = (t.text or "").strip().strip(",.;")
        if slug(name) not in wanted:
            continue
        text = parent[t]
        if text.tag != LEG + "Text":
            continue
        section = sub = None
        e = text
        while e in parent:
            e = parent[e]
            i = e.get("id", "")
            if UNIT.match(i) and sub is None:
                sub = i
            if e.tag == LEG + "P1" and UNIT.match(i):
                section = i
                break
            if e.tag == LEG + "Schedule":
                section = None  # amendments or provisions of other law
                break
        container = parent[text]
        if container.tag == LEG + "Para" and parent.get(container) is not None:
            if parent[container].tag == LEG + "ListItem":
                container = parent[container]
        yield name, section, sub, container, t.get("id")


DEFINES = re.compile(
    r"”[^.“]{0,120}?\b(means|includes|has the meaning|has the same meaning|"
    r"have the meaning|shall be construed|is to be construed|in relation to)\b"
)
REFERS = re.compile(
    r"(has|have) (the same|the) meaning|construed in accordance|shall be construed"
)


def render(container, term):
    """Render the paragraph holding a definition, with any sub-paragraphs."""
    md = "\n\n".join(legislation2md.Renderer().children(container, 3, False))
    md = re.sub(r'<a id="[^"]*"></a>\*\*(.*?)\*\*', r"\1", md)
    md = re.sub(r"[ \t]+", " ", md).strip()
    return md.replace(f"“{term}”", f"“[{term}](term/{slug(term)})”", 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("terms", nargs="+", help="terms to extract")
    ap.add_argument("-c", "--cache", default="var/cache/legislation", type=Path)
    ap.add_argument("-l", "--legislation", default="content/legislation", type=Path)
    ap.add_argument("-o", "--output", default="content/quotation", type=Path)
    args = ap.parse_args()
    wanted = {slug(t) for t in args.terms}
    args.output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for xml in sorted(args.cache.glob("*.xml")):
        ref, title, start = instrument(xml, args.legislation)
        root = ET.parse(xml).getroot()
        seen = set()
        for term, section, sub, text, tid in definitions(root, wanted):
            where = (sub or section or "").partition("-")[2] or "x"
            key = (slug(term), where)
            if key in seen:
                continue
            md = render(text, term)
            if not DEFINES.search(md):
                continue
            seen.add(key)
            role = "reference" if REFERS.search(md) else "definition"
            if not section:
                continue
            kind, _, sec = section.partition("-")
            reference = f"{ref.replace('/', '-')}-{where}-{slug(term)}"
            url = f"https://www.legislation.gov.uk/{ref}/{kind}/{sec}" + (f"#{tid}" if tid else "")
            lines = [
                "---",
                f"reference: {reference}",
                f"name: {yaml(f'{title}, {kind} {sec}')}",
                f"url: {url}",
                "source-class: legislation",
                f"role: {role}",
                f"terms:\n- {slug(term)}",
                f"start-date: {start}" if start else None,
                f"entry-date: {now}",
                "---",
                "",
                md,
                "",
            ]
            out = args.output / f"{reference}.md"
            out.write_text("\n".join(l for l in lines if l is not None), encoding="utf-8")
            print(out)


if __name__ == "__main__":
    main()
