#!/usr/bin/env python3
"""Create a draft term for each topic which has no term, and link the topic to it.

The term text is the topic description, otherwise the answer to
"What is the 'X' consideration?" kept in the topic body.
"""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

CONTENT = Path("content")

# plain English text for topics with neither a description nor an answer
DEFINITIONS = {
    "affordability-index": "A measure of how affordable housing is for local people, usually the ratio of house prices to earnings.",
    "aircraft-noise": "Noise from aircraft, mapped as contours around airports, which is a consideration for noise-sensitive development.",
    "annual-position-statement": "A statement published by a local planning authority each year setting out its housing land supply position.",
    "business-improvement-district": "A defined area where local businesses vote to pay an additional levy to fund improvements to the area.",
    "coastal-erosion-risk": "The risk of land being lost to erosion of the coast, mapped to show the areas likely to be affected.",
    "critical-drainage-area": "An area within flood zone 1 which has critical drainage problems and which has been notified to the local planning authority by the Environment Agency.",
    "development-plan-policy": "A policy set out in a development plan, used to guide decisions on planning applications.",
    "energy-and-renewable-statistics": "Statistics on energy use and the generation of renewable energy for an area.",
    "housing-and-economic-land-availability-assessment-helaa": "An assessment of the land available for housing and economic development in an area, used to inform plan making.",
    "local-flood-data": "Data about local sources of flooding, such as surface water, groundwater and ordinary watercourses.",
    "local-listed-building-consent-order": "An order made by a local planning authority granting listed building consent for specified works to listed buildings in its area.",
    "local-plan-consultation-and-representation": "A consultation on a local plan, and the representations made in response to it.",
    "protected-rural-landscape": "A rural landscape protected by policy because of its character or quality.",
    "strategic-housing-market-assessments-shmas": "An assessment of the need for housing across a housing market area.",
    "village-green-status": "Whether land is registered as a town or village green, giving local people the right to use it for recreation.",
}


def read(path):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", path.read_text(encoding="utf-8"), re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2).strip()) if m else ({}, "")


def write(path, fm, body=""):
    fm = {k: v for k, v in fm.items() if v not in ("", None, [])}
    text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text(
        f"---\n{text}---\n\n{body}\n" if body else f"---\n{text}---\n", encoding="utf-8"
    )


def answer(body):
    m = re.search(
        r"### What is the '.*?' consideration\?\n\n(.*?)(?=\n###|\n## |\Z)", body, re.S
    )
    text = m.group(1).strip() if m else ""
    return "" if text.upper() in ("", "N/A", "NA", "UNKNOWN") else text.split("\n\n")[0]


def main():
    today = date.today().isoformat()
    missing = []
    for p in sorted((CONTENT / "topic").glob("*.md")):
        fm, body = read(p)
        ref = fm["reference"]
        term = CONTENT / "term" / f"{ref}.md"
        if not term.exists():
            text = fm.get("description") or answer(body) or DEFINITIONS.get(ref, "")
            if not text:
                missing.append(ref)
                continue
            write(
                term,
                {
                    "reference": ref,
                    "name": fm["name"],
                    "plural": fm.get("plural", ""),
                    "term-status": "draft",
                    "entry-date": today,
                },
                text[:1].upper() + text[1:],
            )
        if fm.get("term") != ref:
            new = {}
            for k, v in fm.items():
                new[k] = v
                if k == "plural":
                    new["term"] = ref
            write(p, new, body)
    print("no text for:", ", ".join(missing), file=sys.stderr)


if __name__ == "__main__":
    main()
