#!/usr/bin/env python3
"""Migrate considerations from planning-data-design into content/topic.

usage: consideration2topic.py <path to planning-data-design/content/consideration>

Archived considerations are skipped. Writes content/topic,
notes/topic-review.md, and replaces `consideration` with `topic` in content/dataset.
"""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

CONTENT = Path("content")
PREPOSITIONS = {"of", "in", "for", "to", "with", "on", "from", "by", "at"}
# words which look plural but aren't, or whose singular is irregular
KEEP = {
    "bgs",
    "gas",
    "news",
    "species",
    "status",
    "business",
    "access",
    "waterways",
    "lidar",
    "remains",
}
IRREGULAR = {"people": "person", "children": "child", "men": "man", "women": "woman"}
# source slug -> singular name, where the rules get it wrong
OVERRIDES = {
    "areas-which-would-benefit-from-flood-defences": "Area which would benefit from flood defences",
    "bgs-soil-chemistry-for-environmental-assessments": "BGS soil chemistry for environmental assessments",
    "local-area-requirements": "Local area requirement",
    "article-4-directions": "Article 4 direction",
    "britpits-mines-quarries": "Britpits mine & quarry",
    "common-land-and-village-greens": "Common land and village green",
    "development-plans-and-timetables": "Development plan and timetable",
    "drainage-agreements-and-consents": "Drainage agreement and consent",
    "great-crested-newts-edna-pond-surveys": "Great crested newt eDNA pond survey",
    "greater-london-archaeological-priority-areas": "Greater London archaeological priority area",
    "historic-parks-and-gardens": "Historic park and garden",
    "land-registry-polygons-red-line-boundaries": "Land registry polygon / red line boundary",
    "local-plan-consultations-and-representations": "Local plan consultation and representation",
    "national-parks-and-the-broads": "National park and the Broads",
    "nhs-trusts": "NHS trust",
    "planning-applications-decisions": "Planning application and decision",
    "public-parks-and-gardens": "Public park and garden",
    "public-paths-byways": "Public path and byway",
    "safeguarding-aerodromes-technical-sites-and-military-explosives-storage-areas": "Safeguarded aerodrome, technical site and military explosives storage area",
    "sensitive-areas-nitrates": "Sensitive area - nitrate",
}


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2).strip()) if m else ({}, "")


def write(path, fm, body=""):
    fm = {k: v for k, v in fm.items() if v not in ("", None, [])}
    text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\n{text}---\n\n{body}\n" if body else f"---\n{text}---\n", encoding="utf-8"
    )


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def singular_word(w):
    lw = w.lower()
    if lw in KEEP or lw in {"s"} or len(lw) < 4:
        return w
    if lw in IRREGULAR:
        return IRREGULAR[lw]
    if lw.endswith("ies"):
        return w[:-3] + "y"
    if lw.endswith(("sses", "xes", "ches", "shes")):
        return w[:-2]
    if lw.endswith(("ss", "us", "is", "ics")):
        return w
    if lw.endswith("s"):
        return w[:-1]
    return w


def singular(title):
    """Singularise the head noun: the last word before the first preposition."""
    words = title.split()
    end = len(words)
    for i, w in enumerate(words):
        if i and w.lower() in PREPOSITIONS:
            end = i
            break
    words[end - 1] = singular_word(words[end - 1])
    return " ".join(words)


def legislation_reference(url):
    m = re.match(
        r"https?://www\.legislation\.gov\.uk/(ukpga|uksi|asp|anaw|wsi|ukla|ukcm|nia|uksi)/(\d{4})/(\d+)",
        url or "",
    )
    if not m:
        return None
    ref = "/".join(m.groups())
    return (
        ref
        if (CONTENT / "legislation" / ref.replace("/", "-")).with_suffix(".md").exists()
        else None
    )


def main(source):
    today = date.today().isoformat()
    datasets = {p.stem: read(p)[0] for p in (CONTENT / "dataset").glob("*.md")}
    by_consideration = {}
    for ref, fm in datasets.items():
        if fm.get("consideration"):
            by_consideration.setdefault(fm["consideration"], []).append(ref)
    terms = {p.stem for p in (CONTENT / "term").glob("*.md")}

    topics = {}  # reference -> (path, source slug)
    skipped, review = [], []
    for p in sorted(Path(source).glob("*.md")):
        fm, body = read(p)
        if fm.get("template") != "consideration":
            continue  # index page
        if fm.get("stage") == "Archived":
            skipped.append(p.stem)
            continue
        title = fm["title"].strip()
        name = OVERRIDES.get(p.stem) or singular(title)
        owned = by_consideration.get(p.stem, [])
        if (
            len(owned) == 1
            and str(datasets[owned[0]].get("plural", "")).lower() == title.lower()
        ):
            name = datasets[owned[0]][
                "name"
            ]  # the dataset already has the singular name
        ref = slug(name)
        if ref in topics:
            review.append(
                f"- `{p.stem}`: reference {ref} already used by `{topics[ref][1]}`"
            )
            ref = slug(title)
        topics[ref] = (p, p.stem)

        links = []
        refs = []
        for key in ("legislation", "specification"):
            item = fm.get(key)
            if not item:
                continue
            leg = (
                legislation_reference(item.get("url")) if key == "legislation" else None
            )
            if leg:
                refs.append(leg)
            else:
                links.append(
                    f"- {key.capitalize()}: [{item.get('text') or item.get('url')}]({item.get('url')})"
                )
        for item in fm.get("useful_links") or []:
            links.append(
                f"- [{item.get('text') or item.get('url')}]({item.get('url')})"
            )

        desc = (fm.get("description") or "").strip()
        if desc.startswith("Planning consideration:"):
            desc = ""
        out = {
            "reference": ref,
            "name": name,
            "plural": title,
            "term": ref if ref in terms else "",
            "description": desc,
            "legislation": refs,
            "synonyms": fm.get("synonyms") or [],
            "tags": fm.get("tags") or [],
            "github-discussion": fm.get("github_discussion_number") or "",
            "start-date": str(fm.get("created") or ""),
            "entry-date": str(fm.get("updated") or fm.get("created") or today),
        }
        missing = [d for d in fm.get("datasets") or [] if d not in datasets]
        if missing:
            review.append(
                f"- `{ref}`: datasets not in content/dataset: {', '.join(missing)}"
            )
        text = body
        if links:
            text = (text + "\n\n" if text else "") + "## Links\n\n" + "\n".join(links)
        write(CONTENT / "topic" / f"{ref}.md", out, text)
        if name.lower() != title.lower():
            review.append(f"- `{ref}`: {title} → {name}")

    # datasets: consideration -> topic, or the topic which lists the dataset
    listed = {}
    for ref, (path, _) in topics.items():
        for d in read(path)[0].get("datasets") or []:
            listed.setdefault(d, ref)
    source_to_topic = {s: r for r, (_, s) in topics.items()}
    orphans = []
    for ref, fm in datasets.items():
        c = fm.get("consideration")
        topic = source_to_topic.get(c) or listed.get(ref)
        if not c and not topic:
            continue
        path = CONTENT / "dataset" / f"{ref}.md"
        fm, body = read(path)
        fm.pop("consideration", None)
        if topic:
            out = {}
            for k, v in fm.items():
                out[k] = v
                if k == "term":
                    out["topic"] = topic
            out.setdefault("topic", topic)
            fm = out
        else:
            orphans.append(f"- `{ref}`: consideration `{c}` is archived or missing")
        write(path, fm, body)

    lines = [
        "# Topic migration review",
        "",
        f"{len(topics)} topics written, {len(skipped)} archived considerations skipped.",
        "",
        "## Names and references to check",
        "",
        *review,
        "",
        "## Datasets without a topic",
        "",
        *orphans,
        "",
    ]
    Path("notes/topic-review.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"{len(topics)} topics, {len(skipped)} skipped, {len(orphans)} orphan datasets",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main(sys.argv[1])
