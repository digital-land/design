#!/usr/bin/env python3
"""Snapshot GOV.UK pages about planning policy in England as markdown."""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.gov.uk"
QUERIES = [
    "national planning policy framework",
    "planning practice guidance",
    "planning policy England",
    "planning consultation England",
    "spatial development strategies",
    "design and placemaking planning practice guidance",
    "local plans England",
    "neighbourhood planning",
    "permitted development rights",
    "planning application guidance",
    "National Planning Policy for Waste",
    "planning policy for traveller sites",
    "planning obligations section 106",
]
PREFIXES = ("/guidance/", "/government/publications/", "/government/collections/",
    "/government/consultations/",
)
SKIP_TYPES = {"html_publication_index"}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "digital-land-design"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2**attempt)
        except OSError:
            time.sleep(2**attempt)
    return None


def search(query, count):
    params = urllib.parse.urlencode(
        {"q": query, "count": count, "fields": "link"}
    )
    data = get_json(f"{BASE}/api/search.json?{params}") or {}
    return [r["link"] for r in data.get("results", []) if "link" in r]


class Markdown(HTMLParser):
    """Minimal HTML to markdown converter for GOV.UK govspeak."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.href = []
        self.lists = []
        self.row = None
        self.rows = []
        self.cell = None

    def w(self, s):
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if re.fullmatch(r"h[1-6]", tag):
            self.w("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("p", "div", "blockquote"):
            self.w("\n\n")
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self.w("\n")
        elif tag == "li":
            lst = self.lists[-1] if self.lists else ["ul", 0]
            lst[1] += 1
            mark = "-" if lst[0] == "ul" else f"{lst[1]}."
            self.w("\n" + "  " * max(len(self.lists) - 1, 0) + mark + " ")
        elif tag == "br":
            self.w("  \n")
        elif tag in ("strong", "b"):
            self.w("**")
        elif tag in ("em", "i"):
            self.w("*")
        elif tag == "a":
            self.href.append(a.get("href", ""))
            self.w("[")
        elif tag == "table":
            self.rows = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]|p|blockquote", tag):
            self.w("\n\n")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.w("\n")
        elif tag in ("strong", "b"):
            self.w("**")
        elif tag in ("em", "i"):
            self.w("*")
        elif tag == "a" and self.href:
            href = self.href.pop()
            if href.startswith("/"):
                href = BASE + href
            self.w(f"]({href})")
        elif tag in ("td", "th") and self.cell is not None:
            text = re.sub(r"\s+", " ", "".join(self.cell)).strip()
            self.cell = None
            if self.row is not None:
                self.row.append(text.replace("|", "\\|"))
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            self.table()

    def handle_data(self, data):
        self.w(re.sub(r"\s+", " ", data))

    def table(self):
        rows = [r for r in self.rows if r]
        if rows:
            n = max(len(r) for r in rows)
            rows = [r + [""] * (n - len(r)) for r in rows]
            lines = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * n]
            lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
            self.out.append("\n\n" + "\n".join(lines) + "\n\n")
        self.rows = []

    def result(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def to_markdown(html):
    p = Markdown()
    p.feed(html or "")
    return p.result()


def body_of(doc):
    d = doc.get("details", {})
    body = d.get("body")
    if isinstance(body, list):  # multi-format bodies
        body = next((b.get("content") for b in body if "html" in b.get("content_type", "")), "")
    if body:
        return body
    html = f"<p>{doc.get('description') or ''}</p>"
    for part in d.get("parts", []) or []:  # guides
        html += f"<h2>{part.get('title', '')}</h2>{part.get('body', '')}"
    return html


def yaml(s):
    s = str(s)
    return json.dumps(s, ensure_ascii=False) if re.search(r"[:#\"'\[\]{}]", s) else s


def snapshot(path, outdir, now, seen, force):
    path = urllib.parse.urlparse(path).path.rstrip("/")
    if not path.startswith(PREFIXES) or path in seen:
        return []
    seen.add(path)
    doc = get_json(f"{BASE}/api/content{path}")
    if not doc or doc.get("document_type") in SKIP_TYPES:
        return []
    slug = path.split("/")[-1]
    parent = (doc.get("links", {}).get("parent") or [{}])[0].get("base_path")
    if parent:
        slug = f"{parent.split('/')[-1][:100]}--{slug[:100]}"
    out = outdir / f"{slug}.md"
    new = []
    if force or not out.exists():
        first = (doc.get("first_published_at") or doc.get("public_updated_at") or "")[:10]
        lines = [
            "---",
            "prefix: govuk",
            f"reference: {slug}",
            f"name: {yaml(doc.get('title', slug))}",
            f"entry-date: {now}",
            f"start-date: {first}",
            f"document-url: {BASE}{path}",
        ]
        if parent:
            lines.append(f"documentation-url: {BASE}{parent}")
        lines += ["---", "", f"# {doc.get('title', slug)}", "", ""]
        out.write_text(
            "\n".join(lines) + to_markdown(body_of(doc)), encoding="utf-8"
        )
        new.append(out)
        print(out, file=sys.stderr)
    for att in doc.get("details", {}).get("attachments", []) or []:
        url = att.get("url", "")
        if att.get("attachment_type") == "html" and url.startswith(("/", BASE)):
            new += snapshot(url, outdir, now, seen, force)
    return new


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--output", default="content/snapshot", type=Path)
    ap.add_argument("-n", "--count", default=20, type=int, help="results per query")
    ap.add_argument("-q", "--query", action="append", help="search query (repeatable)")
    ap.add_argument("-f", "--force", action="store_true", help="overwrite existing")
    args = ap.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen = set()
    total = 0
    for q in args.query or QUERIES:
        for link in search(q, args.count):
            total += len(snapshot(link, args.output, now, seen, args.force))
            time.sleep(0.2)
    print(f"{total} pages written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
