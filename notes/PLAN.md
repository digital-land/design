# Plan: a glossary of terms with sourced definitions

## Goal

Move towards the model in the [README](../README.md): a glossary of **terms**,
each with every definition found in legislation, the NPPF glossary and wider GOV.UK guidance.
Use it to improve the descriptions of datasets, fields and other items,
and to replace the model managed in [digital-land/specification](https://github.com/digital-land/specification/).

Served at https://design.planning.data.gov.uk, each term page `/term/<term>` shows:

- the term, its name, and its plural or collective name
- links to where the term is defined, with the quotation for each definition
- links to where the term is used

## Current state

- `content/legislation` — 153 instruments (England), with `made-date` and `start-date`
- `content/snapshot` — 236 GOV.UK pages as markdown (`bin/govuk-planning.py`)
- `content/term`, `content/quotation`, `content/abbreviation` — a handful of hand-written examples
- `content/class`, `dataset`, `field`, `column`, `intent`, `datatype`, `prefix` — mostly empty
- `bin/legislation2md.py` — converts legislation XML to markdown and already finds `<Term>` definitions
- the Makefile only has `init`; no build, no CSV compile, no server yet

## Model

One markdown file per entity, front-matter fields as in the README.

| Dataset | Key | Purpose |
| --- | --- | --- |
| term | `term/<slug>` | the concept: `name`, `plural`, `abbreviation`s, short `description` |
| quotation | `<source>-<location>` | verbatim definition or reference, with `source`, `url`, `terms` (list) |
| source | `source/<slug>` | a document: Act, SI, NPPF, GOV.UK page; links to `legislation` or `snapshot` |
| abbreviation | `abbreviation/<abbr>` | already exists; maps to `terms` |

Each quotation has a `role`: `definition` (the source defines the term) or `use` (it mentions it).
Definitions and uses are both links from term to quotation, so the term page can list both.
A term may have several definitions that differ (e.g. "development" in the 1990 Act and the NPPF);
show them side by side and record which one we adopt in the term's `description`.

## Steps

### 1. Fix the foundations

1. Agree front-matter for `term`, `quotation`, `source` (reference, name, plural, `source`, `url`, `role`, `terms`).
2. Fix existing examples (typo `abbreviaton/NPPF`; links use `term/x` not `/term/x`; one-file-per-entity naming).
3. Add a validator (`bin/check.py`): unique references, filename matches reference, every linked term/abbreviation exists, dates valid.
4. Add `make` targets: `init`, `check`, `snapshot`, `dataset` (compile each directory to CSV), `server`.

### 2. Extract definitions from legislation

1. Download `data.xml` for each instrument in `content/legislation` into `var/cache/legislation/`.
2. Extend `legislation2md.py` (or a new `bin/legislation-terms.py`) to emit one record per `<Term>` definition:
   term text, section reference, the defining paragraph as the quotation, the instrument, the in-force date.
3. Also capture "means" / "includes" interpretation clauses that lack `<Term>` markup (e.g. section 336 of the 1990 Act).
4. Write quotations to `content/quotation/<instrument>-<section>-<term>.md`; create a stub term if none exists.
5. Normalise term text: lower-case, singular, strip qualifiers like "(England)"; keep original wording as `alias`.
6. Handle amendments: use the current version, record the `start-date`; flag definitions repealed or superseded.
7. Review a sample (Town and Country Planning Act 1990, Planning Act 2008, CIL Regulations 2010) before running on everything.

### 3. Extract definitions from the NPPF glossary

1. Parse `govuk-guidance-national-planning-policy-framework-annex-b-glossary.md` into one quotation per entry.
2. Link each to the matching term, creating stubs; keep the anchor URL on gov.uk.
3. Resolve cross-references (entries that say "see Annex B" or point to the 1990 Act) as a `see-also` link rather than a duplicate definition.

### 4. Extract definitions and uses from GOV.UK guidance

1. Detect definitional sentences in snapshots ("X means", "X is", "known as", bold or glossary sections) as *candidates* only.
2. Review candidates by hand; keep the verbatim quotation and the page anchor.
3. Record every other mention of a known term in a snapshot as a `use` (generated, not hand-written).
4. Extend `bin/govuk-planning.py` seeds with the missing glossary-like pages as they are found (e.g. PPG glossary sections, data standards).

### 5. Build and link the term list

1. Seed the term list from the specification repo (datasets, fields, typologies) so we replace its model rather than start again.
2. Add terms found by steps 2 to 4 that appear in at least two sources or in the specification.
3. Merge synonyms and plurals; assign `abbreviation` records (NPPF, AWI, CIL, etc).
4. Link terms to each other (`broader`, `narrower`, `see-also`), keeping the hierarchy small.

### 6. Use terms to improve descriptions

1. For each dataset and field in the specification, add a `term` reference and replace the free-text description
   with the adopted definition, quoted and cited.
2. List fields that have no sourced term; resolve or mark "no official definition, plain English chosen" per the design principles.
3. Record conflicts between sources for review by policy colleagues.

### 7. Serve at design.planning.data.gov.uk

1. Update https://github.com/digital-land/planning-data-design to read `content/` (or the compiled CSVs).
2. Routes: `/term/` (index, A to Z), `/term/<term>`, `/quotation/<ref>`, `/source/<ref>`, `/abbreviation/<abbr>`.
3. Term page: name, plural, description, definitions (quotation, source, date, link to the exact anchor), then uses grouped by source.
4. Build "used in" indexes at build time by scanning content for `term/<slug>` links and term names.
5. Redirect old specification URLs to the new routes.
6. Add the `dataset/` CSV outputs so the specification repo can consume them until it is retired.

### 8. Retire the specification repo

1. Map every specification entity to a content directory; check nothing is lost.
2. Point https://digital-land.github.io/specification/ at the new site.
3. Archive the repo once downstream consumers (pipelines, config) read the new CSVs.

## Order of work

Foundations (1) first. Then run 2 and 3 in parallel on a small set of terms
(development, planning permission, local planning authority, heritage asset, brownfield land),
and look at the result on a term page before scaling up. Then 4 and 5, then 6 and 7.

## Open questions

- Which term wins when sources disagree, and who decides?
- How are definitions versioned? Legislation changes over time; do we keep superseded text?
- Do we store full quotations or only a link and offset? (Copying is allowed under OGL, but long quotes bloat the repo.)
- Do terms from the specification (e.g. "typology", "entity") belong in the same glossary as planning terms?
- Scope: England only, or also Wales, Scotland and Northern Ireland terms where they differ?
- Is the Obsidian vault the source of truth, or the compiled CSVs?
