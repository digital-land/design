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
        name = "".join(t.itertext()).strip().strip(",.;")
        if wanted is not None and slug(name) not in wanted:
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


NARROW = re.compile(
    r"\b(in this (section|Part|Chapter|Schedule|regulation|article|paragraph)|"
    r"for the purposes? of|in sections?|in relation to|in subsection)\b",
    re.I,
)


def collect(cache, legislation, wanted):
    """Return {term slug: [record]} for every definition in the cached XML."""
    found = {}
    for xml in sorted(cache.glob("*.xml")):
        ref, title, start = instrument(xml, legislation)
        root = ET.parse(xml).getroot()
        seen = set()
        for term, section, sub, container, tid in definitions(root, wanted):
            if not section:
                continue
            where = (sub or section).partition("-")[2] or "x"
            key = (slug(term), where)
            if key in seen:
                continue
            md = render(container, term)
            if not DEFINES.search(md):
                continue
            seen.add(key)
            kind, _, sec = section.partition("-")
            found.setdefault(slug(term), []).append(
                {
                    "term": term,
                    "reference": f"{ref.replace('/', '-')}-{where}-{slug(term)}",
                    "name": f"{title}, {kind} {sec}",
                    "url": f"https://www.legislation.gov.uk/{ref}/{kind}/{sec}"
                    + (f"#{tid}" if tid else ""),
                    "role": "reference" if REFERS.search(md) else "definition",
                    "start": start,
                    "text": md,
                    "instrument": ref,
                }
            )
    return found


def nppf_terms():
    return {
        t
        for f in Path("content/quotation").glob("nppf-annex-b-*.md")
        for t in re.findall(r"^- (.+)$", f.read_text(), re.M)
    }


def snapshot_files(term):
    """Number of GOV.UK snapshots that mention the term."""
    pattern = re.compile(r"(?<![\w-])" + re.escape(term.replace("-", " ")) + r"s?(?![\w-])")
    return sum(1 for text in snapshots() if pattern.search(text))


_SNAPSHOTS = []


def snapshots():
    if not _SNAPSHOTS:
        _SNAPSHOTS.extend(
            p.read_text(encoding="utf-8").lower()
            for p in Path("content/snapshot").glob("*.md")
        )
    return _SNAPSHOTS


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("terms", nargs="*", help="terms to extract")
    ap.add_argument("--all", action="store_true", help="every defined term")
    ap.add_argument("--min-instruments", type=int, default=2,
        help="with --all, keep terms defined in at least this many instruments")
    ap.add_argument("--with-nppf", action="store_true",
        help="with --all, also keep terms in the NPPF glossary")
    ap.add_argument("--min-snapshots", type=int, default=5,
        help="with --all, keep terms mentioned in at least this many snapshots")
    ap.add_argument("--max-per-term", type=int, default=8, help="quotations kept per term")
    ap.add_argument("-c", "--cache", default="var/cache/legislation", type=Path)
    ap.add_argument("-l", "--legislation", default="content/legislation", type=Path)
    ap.add_argument("-o", "--output", default="content/quotation", type=Path)
    args = ap.parse_args()
    wanted = None if args.all else {slug(t) for t in args.terms}
    found = collect(args.cache, args.legislation, wanted)
    if args.all:
        keep = nppf_terms() if args.with_nppf else set()
        found = {
            t: recs
            for t, recs in found.items()
            if t in keep
            or (
                len({r["instrument"] for r in recs}) >= args.min_instruments
                and snapshot_files(t) >= args.min_snapshots
            )
        }
    for t, recs in found.items():  # keep the most general definitions
        recs.sort(key=lambda r: (r["role"] != "definition", "/ukpga/" not in r["url"], bool(NARROW.search(r["text"][:200]))))
        found[t] = recs[: args.max_per_term]
    args.output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for recs in found.values():
        for r in recs:
            lines = [
                "---",
                f"reference: {r['reference']}",
                f"name: {yaml(r['name'])}",
                f"url: {r['url']}",
                "source-class: legislation",
                f"role: {r['role']}",
                f"terms:\n- {slug(r['term'])}",
                f"start-date: {r['start']}" if r["start"] else None,
                f"entry-date: {now}",
                "---",
                "",
                r["text"],
                "",
            ]
            out = args.output / f"{r['reference']}.md"
            out.write_text("\n".join(l for l in lines if l is not None), encoding="utf-8")
    print(f"{sum(len(v) for v in found.values())} quotations for {len(found)} terms", file=sys.stderr)


if __name__ == "__main__":
    main()
