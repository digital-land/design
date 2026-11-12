#!/usr/bin/env python3
"""Ensure each GOV.UK page cited by a term or quotation has an entry in content/govuk."""

import importlib
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
planning = importlib.import_module("govuk-planning")
CONTENT = Path("content")
URL = re.compile(r"https://www\.gov\.uk(/[^\s#)\"']*)")
CURIE = re.compile(r"^definition: govuk:([^#\s]+)", re.M)


def references():
    """GOV.UK paths cited by terms (documentation-url, definition) and quotations (url)."""
    cited = {}
    for p in sorted((CONTENT / "term").glob("*.md")) + sorted((CONTENT / "quotation").rglob("*.md")):
        head = p.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        for key in ("documentation-url", "url", "document-url"):
            m = re.search(rf"^{key}: *(\S+)", head, re.M)
            if m and (u := URL.match(m.group(1))):
                cited.setdefault("/" + u.group(1).strip("/"), p)
        for ref in CURIE.findall(head):
            cited.setdefault("/" + ref.strip("/"), p)
    return cited


def existing():
    have = set()
    for p in (CONTENT / "govuk").glob("*.md"):
        m = re.search(r"^reference: *(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            have.add("/" + m.group(1).strip("/"))
    return have


def main():
    cited, have = references(), existing()
    missing = sorted(p for p in cited if p not in have)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen, failed = set(), []
    for path in missing:
        new = planning.fetch_page(path, CONTENT / "govuk", now, seen, False)
        if not new:
            failed.append(path)
        time.sleep(0.2)
    print(f"{len(missing)} pages missing, {len(missing) - len(failed)} added", file=sys.stderr)
    for path in failed:
        print(f"not added: {path} (cited by {cited[path]})", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
