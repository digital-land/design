#!/usr/bin/env python3
"""Convert a legislation.gov.uk XML file (data.xml) to markdown."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET

LEG = "{http://www.legislation.gov.uk/namespaces/legislation}"
HTML = "{http://www.w3.org/1999/xhtml}"
PLEVELS = ["P1", "P2", "P3", "P4", "P5", "P6"]
TERMS = {}  # term text -> anchor id, for terms defined in this document
HEADED = ("Part", "Chapter", "Pblock", "PsubBlock", "Schedule")


def name(e):
    return e.tag.split("}")[-1]


def ws(s):
    return re.sub(r"\s+", " ", s).strip()


def inline(e):
    """Render the content of an element as inline markdown."""
    out = [e.text or ""]
    for c in e:
        n = name(c)
        s = inline(c)
        if n in ("InternalLink", "ExternalLink", "Citation"):
            uri = c.get("DocumentURI") or c.get("URI")
            if uri and s.strip():
                s = f"[{s}]({uri})"
        elif n == "Term":
            if s.strip():
                tid = c.get("id")
                if tid:
                    TERMS.setdefault(s.strip(), tid)
                    s = f'<a id="{tid}"></a>**{s}**'
                else:
                    s = f"**{s}**"
        elif n in ("Emphasis", "Italic"):
            s = f"*{s}*" if s.strip() else s
        elif n in ("Strong", "Bold"):
            s = f"**{s}**" if s.strip() else s
        elif n in ("Superior", "Sup"):
            s = f"<sup>{s}</sup>"
        elif n in ("Inferior", "Sub"):
            s = f"<sub>{s}</sub>"
        out.append(s)
        out.append(c.tail or "")
    return "".join(out)


def text(e):
    return ws(inline(e))


def quote(blocks):
    lines = "\n\n".join(blocks).split("\n")
    return "\n".join(f"> {l}" if l else ">" for l in lines)


def indent(s, n):
    pad = " " * n
    return "\n".join(pad + l if l else l for l in s.split("\n"))


def table(t):
    rows = []
    for tr in t.iter(HTML + "tr"):
        cells = [
            ws(inline(c)).replace("|", "\\|")
            for c in tr
            if c.tag in (HTML + "td", HTML + "th")
        ]
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(r) + " |" for r in rows]
    lines.insert(1, "|" + " --- |" * width)
    return "\n".join(lines)


class Renderer:
    def heading(self, s, level, amend):
        if not s:
            return []
        if amend:
            return [f"**{s}**"]
        return ["#" * min(level, 6) + " " + s]

    def children(self, e, level, amend, skip=()):
        blocks = []
        for c in e:
            if name(c) not in skip:
                blocks += self.block(c, level, amend)
        return blocks

    def block(self, e, level=2, amend=False):
        n = name(e)
        if n in (
            "Text",
            "Para",
            "P",
            "P1para",
            "P2para",
            "P3para",
            "P4para",
            "P5para",
            "P6para",
            "Pnumber",
            "Title",
            "Number",
            "Reference",
            "TitleBlock",
        ):
            pass
        if n == "Text":
            return [text(e)]
        if n == "BlockAmendment":
            return [quote(self.children(e, level, True))]
        if n == "AppendText":
            return [text(e)]
        if n in ("OrderedList", "UnorderedList"):
            return self.list_(e, n == "OrderedList", level, amend)
        if n in ("Tabular", "table") or e.tag == HTML + "table":
            t = e if e.tag == HTML + "table" else e.find(HTML + "table")
            return [table(t)] if t is not None else []
        if n in HEADED:
            return self.headed(e, level, amend)
        if n == "P1group":
            return self.p1group(e, level, amend)
        if n in PLEVELS:
            return self.plevel(e, level, amend)
        if n in (
            "Body",
            "Schedules",
            "Para",
            "P",
            "P1para",
            "P2para",
            "P3para",
            "P4para",
            "P5para",
            "P6para",
            "ScheduleBody",
            "ListItem",
            "Division",
            "Contents",
        ):
            if n == "Schedules":
                return self.children(e, level, amend)
            return self.children(e, level, amend)
        if n in ("Title", "Number", "TitleBlock", "Reference", "Pnumber"):
            return []
        if n in ("Metadata",):
            return []
        # unknown container: inline text if it has any, else recurse
        s = text(e)
        return [s] if s and not len(e) else self.children(e, level, amend)

    def headed(self, e, level, amend):
        n = name(e)
        number = e.find(LEG + "Number")
        title = e.find(LEG + "Title")
        tb = e.find(LEG + "TitleBlock")
        ref = e.find(LEG + "Reference")
        if title is None and tb is not None:
            title = tb.find(LEG + "Title")
        parts = [text(x) for x in (number, title) if x is not None]
        head = " – ".join(p for p in parts if p)
        out = self.heading(head, level, amend)
        if ref is not None:
            out.append(f"*{text(ref)}*")
        return out + self.children(
            e, level + 1, amend, skip=("Number", "Title", "TitleBlock", "Reference")
        )

    def p1group(self, e, level, amend):
        title = e.find(LEG + "Title")
        p1s = e.findall(LEG + "P1")
        t = text(title) if title is not None else ""
        if len(p1s) == 1 and p1s[0].find(LEG + "Pnumber") is not None:
            num = text(p1s[0].find(LEG + "Pnumber"))
            out = self.heading(f"{num}. {t}" if t else num, level, amend)
            return out + self.plevel(p1s[0], level + 1, amend, numbered=False)
        out = self.heading(t, level, amend)
        return out + self.children(e, level + 1, amend, skip=("Title",))

    def plevel(self, e, level, amend, numbered=True):
        n = name(e)
        num = e.find(LEG + "Pnumber")
        label = text(num) if num is not None else ""
        para = e.find(LEG + n + "para")
        inner = []
        if para is not None:
            inner = self.children(para, level, amend)
        if n == "P1":
            if numbered and label:
                inner = [f"**{label}**" + (" " + inner[0] if inner else "")] + inner[1:]
            return inner
        label = label if n == "P2" and not label.startswith("(") else label
        fmt = f"({label})" if label and not label.startswith("(") else label
        if n == "P2":
            first = f"{fmt} " + inner[0] if inner else fmt
            return [first] + inner[1:]
        # P3 and below: nested bullet list items
        item = f"- {fmt} " + (inner[0] if inner else "")
        rest = [indent(b, 2) for b in inner[1:]]
        return ["\n\n".join([item] + rest) if rest else item]

    def list_(self, e, ordered, level, amend):
        items = []
        for li in e.findall(LEG + "ListItem"):
            blocks = self.children(li, level, amend)
            if not blocks:
                continue
            first = "- " + blocks[0]
            rest = [indent(b, 2) for b in blocks[1:]]
            items.append("\n\n".join([first] + rest))
        return ["\n".join(items)] if items else []


PROTECT = re.compile(r"<a id=[^>]*></a>\*\*.*?\*\*|\[[^\]]*\]\([^)]*\)|\*\*.*?\*\*")


def link_terms(md):
    """Link each use of a defined term to its definition anchor."""
    if not TERMS:
        return md
    terms = sorted(TERMS, key=len, reverse=True)
    use = re.compile(
        r"(?<![\w-])(" + "|".join(re.escape(t) for t in terms) + r")(?![\w-])"
    )

    def sub(m):
        return f"[{m.group(1)}](#{TERMS[m.group(1)]})"

    def line(l):
        # leave headings and quoted amendments (other Acts' text) alone
        if l.startswith(("#", ">")):
            return l
        out, pos = [], 0
        for m in PROTECT.finditer(l):
            out.append(use.sub(sub, l[pos : m.start()]))
            out.append(m.group(0))
            pos = m.end()
        out.append(use.sub(sub, l[pos:]))
        return "".join(out)

    return "\n".join(line(l) for l in md.split("\n"))


def convert(path):
    root = ET.parse(path).getroot()
    r = Renderer()
    out = []
    prelims = root.find(f".//{LEG}PrimaryPrelims")
    if prelims is None:
        prelims = root.find(f".//{LEG}SecondaryPrelims")
    if prelims is not None:
        t = prelims.find(LEG + "Title")
        out.append("# " + (text(t) if t is not None else "Legislation"))
        for tag in ("Number", "LongTitle", "DateOfEnactment"):
            x = prelims.find(LEG + tag)
            if x is not None and text(x):
                out.append(text(x) if tag != "DateOfEnactment" else f"*{text(x)}*")
    else:
        t = root.find(f".//{{*}}title")
        out.append("# " + (text(t) if t is not None else "Legislation"))
    for tag in ("PrimaryPreamble", "SecondaryPreamble", "Body", "Schedules"):
        for e in root.iter(LEG + tag):
            if tag == "Schedules":
                t = e.find(LEG + "Title")
                if t is not None:
                    out.append("## " + text(t))
                out += r.children(e, 3, False, skip=("Title",))
            else:
                out += r.children(e, 2, False)
    md = "\n\n".join(b for b in out if b and b.strip()) + "\n"
    return link_terms(md)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xml", help="XML file from legislation.gov.uk")
    ap.add_argument("output", nargs="?", help="markdown file (default: stdout)")
    a = ap.parse_args()
    md = convert(a.xml)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(md)
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
