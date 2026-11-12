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


PLANNING_ACTS = (
    "/ukpga/1990/8/", "/ukpga/1990/9/", "/ukpga/2004/5/", "/ukpga/2008/29/",
    "/ukpga/2011/20/", "/ukpga/2013/27/", "/ukpga/2016/22/", "/ukpga/2017/20/",
    "/ukpga/2023/55/", "/ukpga/2025/34/", "/ukpga/2021/30/", "/ukpga/1979/46/",
)
PLANNING_NAME = re.compile(
    r"Planning|Neighbourhood|Community Infrastructure|Brownfield|Biodiversity Gain|"
    r"Heritage|Hedgerows|Habitats|Environmental Impact|Permitted Development", re.I
)


def planning(fm):
    """True if the quotation is from legislation about planning, not general law."""
    return any(a in fm["url"] for a in PLANNING_ACTS) or bool(
        "/uksi/" in fm["url"] and PLANNING_NAME.search(fm["name"])
    )


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


def unlink(term):
    """Remove links to a deleted term from datasets."""
    for f in (CONTENT / "dataset").glob("*.md"):
        text = f.read_text(encoding="utf-8")
        new = re.sub(rf"^term: {re.escape(term)}\n", "", text, count=1, flags=re.M)
        if new != text:
            f.write_text(new, encoding="utf-8")


def generated(path, qs, term):
    """True if the term file is the unedited text of one of its quotations."""
    fm, body = read(path)
    if fm.get("plural"):  # generated terms have no plural; this one has been edited
        return False
    return any(body == clean(b, term) or body == b for _, b in qs)


def main():
    rebuild = "--rebuild" in sys.argv
    skip = deleted()
    ignore = {
        l.strip()
        for l in Path("notes/ignore-terms.txt").read_text().splitlines()
        if l.strip() and not l.startswith("#")
    }
    quotes = {}
    for p in sorted((CONTENT / "quotation").rglob("*.md")):
        fm, body = read(p)
        for t in fm.get("terms", []):
            quotes.setdefault(t, []).append((fm, body))
    today = date.today().isoformat()
    created, unresolved = 0, []
    for term, qs in sorted(quotes.items()):
        out = CONTENT / "term" / f"{term}.md"
        if term in skip:
            continue
        draft = out.exists() and read(out)[0].get("term-status") == "draft"
        if out.exists() and not draft:
            if not (rebuild and generated(out, qs, term)):
                continue
        leg = [
            (score(fm, b), fm, b)
            for fm, b in qs
            if fm.get("role") == "definition" and fm.get("source-class") == "legislation"
        ]
        leg = [x for x in leg if x[0] >= 0 and planning(x[1])]
        if term in ignore:
            leg = []
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
            nppf.sort(key=lambda x: not x[0]["reference"].startswith("nppf-"))
            fm, body = nppf[0]
            status = "guidance"
            text = body
            name = (
                fm["name"].split("Glossary, ", 1)[1]
                if "Glossary, " in fm["name"]
                else term.replace("-", " ")
            )
        else:
            unresolved.append(term)
            if out.exists() and not draft:  # was generated from a quotation no longer acceptable
                out.unlink()
                unlink(term)
            continue
        name = name[:1].upper() + name[1:]
        plural = ""
        if draft:  # promote a draft: keep its names, replace the unsourced text
            old = read(out)[0]
            name, plural = old.get("name", name), old.get("plural", "")
        out.write_text(
            "\n".join(
                [
                    "---",
                    f"reference: {term}",
                    f"name: {yaml(name)}",
                    *([f"plural: {yaml(plural)}"] if plural else []),
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
