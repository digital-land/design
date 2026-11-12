#!/usr/bin/env python3
"""Check the markdown files in content/ have valid front-matter and links."""

import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

CONTENT = Path("content")
TERM_STATUS = {p.stem for p in (CONTENT / "term-status").glob("*.md")}
DATES = ("made-date", "start-date", "end-date", "entry-date")
LINK = re.compile(r"\]\(/?([a-z-]+)/([^)\s#]+)")
LINKED = {"term", "abbreviation", "legislation", "quotation", "source"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def read(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def valid_date(v):
    if isinstance(v, (date, datetime)):
        return True
    return bool(re.fullmatch(r"\d{4}-\d\d-\d\d(T\d\d:\d\d:\d\dZ)?", str(v)))


_FILES = {}


def exists(kind, target):
    """True if content/<kind>/**/<target>.md exists (directories may be sharded)."""
    if kind not in _FILES:
        _FILES[kind] = {p.stem for p in (CONTENT / kind).rglob("*.md")}
    return slug(target) in _FILES[kind]


def check(path, errors, warnings):
    where = str(path)
    try:
        fm, body = read(path)
    except yaml.YAMLError as e:
        errors.append(f"{where}: invalid YAML: {str(e).splitlines()[-1]}")
        return
    if fm is None:
        errors.append(f"{where}: no front-matter")
        return
    kind = path.relative_to(CONTENT).parts[0]
    ref = fm.get("reference")
    if kind != "datatype" and not ref:
        errors.append(f"{where}: no reference")
    elif ref and slug(path.stem)[:150] != slug(ref)[:150]:
        errors.append(f"{where}: filename does not match reference {ref!r}")
    for k in DATES:
        if fm.get(k) not in (None, "") and not valid_date(fm[k]):
            errors.append(f"{where}: invalid {k} {fm[k]!r}")
    if kind == "term":
        status = fm.get("term-status")
        if status not in TERM_STATUS:
            errors.append(f"{where}: term-status must be one of {sorted(TERM_STATUS)}")
        elif status != "draft" and not fm.get("documentation-url"):
            errors.append(f"{where}: term-status {status} needs a documentation-url")
        if not body.strip():
            errors.append(f"{where}: no definition text")
    for t in fm.get("terms") or []:
        if not (CONTENT / "term" / f"{t}.md").exists():
            warnings.append(f"{where}: unknown term {t}")
    for kind_, target in LINK.findall(body):
        if kind_ in LINKED and not exists(kind_, target):
            warnings.append(f"{where}: broken link {kind_}/{target}")


def main():
    strict = "--strict" in sys.argv
    errors, warnings = [], []
    paths = sorted(
        p for p in CONTENT.glob("*/**/*.md") if p.relative_to(CONTENT).parts[0] != "snapshot"
    )
    seen = {}
    for p in paths:
        check(p, errors, warnings)
        try:
            fm, _ = read(p)
        except yaml.YAMLError:
            continue
        ref = (fm or {}).get("reference")
        if ref:
            key = (p.relative_to(CONTENT).parts[0], str(ref).lower())
            if key in seen:
                errors.append(f"{p}: duplicate reference also in {seen[key]}")
            seen[key] = p
    for line in errors:
        print("error:", line)
    for line in warnings:
        print("warning:", line)
    print(
        f"{len(paths)} files, {len(errors)} errors, {len(warnings)} warnings",
        file=sys.stderr,
    )
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
