# Plan: migrate content into the design model

## Goal

Migrate the content in this repository into the model outlined in the [README](../README.md)
This is content intended to be served at https://design.planning.data.gov.uk by https://github.com/digital-land/planning-data-design

Every term, topic, dataset and field is named in the singular, with the plural recorded in its `plural` field.
`make check` should fail on any `reference` that is not singular, unless listed in an exception file.

## Building

* `make check` checks the integrity of the content
* `make review` creates `notes/dataset-review.md`, highlighting datasets in the dataset realm with names which don't substantially match a definition from legislation or guidance.

### content/term

The glossary of **terms**,
each with every definition found in legislation, the NPPF glossary and wider GOV.UK guidance.
Use it to improve the descriptions of datasets, fields and other items,
and to replace the model managed in [digital-land/specification](https://github.com/digital-land/specification/).

Served at https://design.planning.data.gov.uk, each term page `/term/<term>` will show:

- the term, its name, and its plural or collective name
- links to where the term is defined, with the quotation for each definition
- links to where the term is used

### Term text and status

The text of a term file is the most authoritative definition available:
quoted directly from the source where one exists, otherwise constructed by us.
The `term-status` field records where it came from:

| `term-status` | Text is | `documentation-url` |
| --- | --- | --- |
| `legislation` | definition substantially matches a definition in an Act or statutory instrument | link to the definition on legislation.gov.uk (section anchor) |
| `guidance` | definition substantially matches GOV.UK content, such as the NPPF glossary or PPG | link to the GOV.UK page and anchor |
| `draft` | constructed by us, with no authoritative definition found | blank, or the best related source |

Choose the status by precedence: `legislation`, then `guidance`, then `draft`.
Other definitions found (including those that differ) stay as quotations linked to the term,
so the term page still shows every source.
Move a term from `draft` to `guidance` or `legislation` when a definition is found;
list `draft` terms for review.

Each quotation has a `role`: `definition` (the source defines the term) or `use` (it mentions it).
Definitions and uses are both links from term to quotation, so the term page can list both.
New terms take the best content available, on the assumption that it will be reviewed and edited.
Conflicting definitions are noted in `notes/dataset-review.md` for review.
A term may have several definitions that differ (e.g. "development" in the 1990 Act and the NPPF);
show them side by side and record which one we adopt in the term's `description`.

## Progress

- Step 1: validator (`make check`), `make dataset` (CSV per directory, term usage); front-matter agreed; examples not yet fixed
- Step 2: done by `make legislation terms` — XML for 147 of 153 instruments (6 failed to download); terms kept if in the NPPF glossary or defined in 2+ instruments and mentioned in 5+ snapshots; unmarked interpretation clauses still to do
- Step 3: done — 129 NPPF glossary quotations
- Step 4: done for known terms — `bin/govuk-candidates.py` found 13 candidate quotations (`role: candidate`), 6 promoted to `definition` and 6 marked `use`; 3 new defined terms listed in `notes/govuk-candidates.md`, 1 added; usage counts by `bin/term-usage.py`. Draft terms are promoted when a definition is found
- Step 5: done — `bin/seed-specification.py` seeded 283 datasets and 537 fields (case-duplicates skipped) and 110 draft terms from dataset descriptions; each dataset links to its term
- Step 6: started — `make review` writes `notes/dataset-review.md` comparing dataset descriptions with sourced definitions; descriptions not yet replaced
- Step 7 (topics): done by `bin/consideration2topic.py` and `bin/topic-strip.py` (unanswered questions removed) — 275 topics, 122 archived skipped, no stages, each dataset carries its `topic`; 9 datasets left without a topic (their considerations were archived); names to check are in `notes/topic-review.md`; topics have no draft terms yet, only those matching an existing term are linked
- Steps 8 and 9: not started

Legislation picks: terms are only taken from planning legislation (`planning()` in `bin/build-terms.py`),
and `notes/ignore-terms.txt` lists generic words (address, document, company) whose statutory definitions are sense-specific.
`python3 bin/build-terms.py --rebuild` regenerates terms that are still the unedited text of a quotation.

## Steps

### 1. Fix the foundations

1. Agree front-matter for `term` (reference, name, plural, `term-status`, `documentation-url`), `quotation` and `source` (reference, name, `source`, `url`, `role`, `terms`).
   Validate `term-status` is one of `draft`, `guidance`, `legislation`, and that `documentation-url` is set unless `draft`.
2. Fix existing examples (typo `abbreviaton/NPPF`; links use `term/x` not `/term/x`; one-file-per-entity naming).
3. Add a validator (`bin/check.py`): unique references, filename matches reference, every linked term/abbreviation exists, dates valid.
4. Add `make` targets: `init`, `check`, `govuk`, `dataset` (compile each directory to CSV), `server`.

### 2. Extract definitions from legislation

1. Download `data.xml` for each instrument in `content/legislation` into `var/cache/legislation/`.
2. Extend `legislation2md.py` (or a new `bin/legislation-terms.py`) to emit one record per `<Term>` definition:
   term text, section reference, the defining paragraph as the quotation, the instrument, the in-force date.
3. Also capture "means" / "includes" interpretation clauses that lack `<Term>` markup (e.g. section 336 of the 1990 Act).
4. Write quotations to `content/quotation/legislation/<instrument>-<section>-<term>.md`; create a stub term if none exists.
5. Where the best definition is legislation, set the term's text to it, `term-status: legislation` and `documentation-url` to the section.
6. Normalise term text: lower-case, singular, strip qualifiers like "(England)"; keep original wording as `alias`.
7. Handle amendments: use the current version, record the `start-date`; flag definitions repealed or superseded.
8. Review a sample (Town and Country Planning Act 1990, Planning Act 2008, CIL Regulations 2010) before running on everything.

### 3. Extract definitions from the NPPF glossary

1. Parse `govuk-guidance-national-planning-policy-framework-annex-b-glossary.md` into one quotation per entry.
2. Link each to the matching term, creating stubs; keep the anchor URL on gov.uk.
3. Where no legislative definition exists, set the term's text to the glossary entry and `term-status: guidance`.
4. Resolve cross-references (entries that say "see Annex B" or point to the 1990 Act) as a `see-also` link rather than a duplicate definition.

### 4. Extract definitions and uses from GOV.UK guidance

1. Detect definitional sentences in snapshots ("X means", "X is", "known as", bold or glossary sections) as *candidates* only.
2. Review candidates by hand; keep the verbatim quotation and the page anchor.
3. Promote a reviewed candidate to the term's text with `term-status: guidance` only if no legislative or NPPF definition exists.
4. Record every other mention of a known term in a snapshot as a `use` (generated, not hand-written).
5. Extend `bin/govuk-planning.py` seeds with the missing glossary-like pages as they are found (e.g. PPG glossary sections, data standards).

### 5. Build and link the term list

1. Seed the term list from the specification repo (datasets, fields, typologies) so we replace its model rather than start again.
2. Mark every term seeded from the specification `draft` until a sourced definition is found.
3. Add terms found by steps 2 to 4 that appear in at least two sources or in the specification.
4. Merge synonyms and plurals; assign `abbreviation` records (NPPF, AWI, CIL, etc).
5. Link terms to each other (`broader`, `narrower`, `see-also`), keeping the hierarchy small.

### 6. Use terms to improve descriptions

1. For each dataset and field in the specification, add a `term` reference and replace the free-text description
   with the adopted definition, quoted and cited.
2. List `draft` terms and fields that have no sourced term; resolve or mark "no official definition, plain English chosen" per the design principles.
3. Record conflicts between sources for review by policy colleagues.

### 7. Migrate considerations to topics

Source: `content/consideration/` in [planning-data-design](https://github.com/digital-land/planning-data-design), 398 files.

Considerations have a `stage`. Skip those marked `Archived` and drop the stage from the rest: topics are categories, not something which moves through stages.

1. Add `bin/consideration2topic.py`; it reads the source repo (path as an argument), drops `stage: Archived`, and writes `content/topic/<reference>.md`. Re-runnable, so it can be repeated as the source changes until that repo is retired.
2. Naming: considerations are plural ("Article 4 Directions"). Set `name` to the singular, `plural` to the original title, and `reference` to the singular slug. Singularise by rule, write the result to a review list, and fix by hand; the dataset field `consideration: ancient-woodlands` shows the old slugs in use.
3. Field mapping:

   | Source | Topic |
   | --- | --- |
   | `title` | `name` (singular) and `plural` |
   | `description` | `description`; skip the placeholder "Planning consideration: X" |
   | `datasets` | skipped; the topic is added to each listed `content/dataset` instead |
   | `legislation`, `specification` | `legislation` where the URL resolves to a record in `content/legislation`, otherwise a link in the body |
   | `synonyms` | `synonyms`; where a synonym is also a topic, link it rather than duplicate it |
   | `tags` | `tags`, to map to `theme` later (`local plan`, `local land charge` and so on are not all themes) |
   | `github_discussion_number` | `github-discussion` |
   | `created`, `updated` | `start-date`, `entry-date` |
   | `frequency_of_updates` | skipped for now; we'll revisit quality dimensions against user and needs |
   | `useful_links` | a `## Links` section in the body, to move to the quotation and source datasets |

4. Body: remove the unanswered discovery questions (answered "N/A", "Unknown" or left blank) from each topic and keep the answers, as a stopgap until they are replaced with structured `need`, `source` and `quotation` records. The topic text should become a single sourced definition.
5. Link each topic to a `term` where one matches. The topic's definition comes from the term, not the other way round, so a topic with no term gets a `draft` term.
6. Replace `consideration` with `topic` in `content/dataset` and `content/field`. A dataset whose consideration is archived gets no topic; list those for review.
7. Extend `bin/check.py`: topic references are unique and singular, and `topic` links resolve.
8. Update the README to remove the word "consideration" once migrated.
9. Write a redirect for each of the 122 archived considerations, in the format used by the [redirects](https://github.com/digital-land/planning-data-design/tree/main/redirects) directory of planning-data-design, so old `/consideration/<slug>` URLs still resolve.

### 8. Serve at design.planning.data.gov.uk

1. Update https://github.com/digital-land/planning-data-design to read `content/` (or the compiled CSVs).
2. Routes: `/term/` (index, A to Z), `/term/<term>`, `/quotation/<ref>`, `/source/<ref>`, `/abbreviation/<abbr>`, `/topic/` and `/topic/<topic>`.
3. Term page: name, plural, description, definitions (quotation, source, date, link to the exact anchor), then uses grouped by source.
4. Build "used in" indexes at build time by scanning content for `term/<slug>` links and term names.
5. Redirect old specification URLs to the new routes.
6. Add the `dataset/` CSV outputs so the specification repo can consume them until it is retired.

### 9. Retire the specification and consideration sources

1. Map every specification entity to a content directory; check nothing is lost.
2. Point https://digital-land.github.io/specification/ at the new site.
3. Archive the repo once downstream consumers (pipelines, config) read the new CSVs.
4. Remove `content/consideration` from planning-data-design once topics are served from here.

## Order of work

Foundations (1) first. Then run 2 and 3 in parallel on a small set of terms
(development, planning permission, local planning authority, heritage asset, brownfield land),
and look at the result on a term page before scaling up. Then 4 and 5, then 6 and 7 (topics; start with the 33 "On the platform" ones), then 8.

## Open questions

- **Draft terms for topics:** 232 terms were generated from topic descriptions, many of which describe the data rather than define the term.
  Who reviews them, and should they be listed in `make review` alongside the other `draft` terms?
- **Topics and themes:** `tags` (`local plan`, `local land charge`, `building-control` and so on) are not all themes.
  Which tags map to a `theme`, and should the rest be dropped?
- **Datasets without a topic:** 9 datasets (`site`, `waste-plan`, `supplementary-plan` and others) belonged to archived considerations.
  Should they get a new topic, share an existing one, or stay without?
- **Missing datasets:** topics named `central-activites-zone` (a typo), `development-plan-event` and `using-coal-mining-information`, which aren't in `content/dataset`.
  Are these the datasets `central-activities-zone` and `development-plan-event`, or should they be dropped?
- **Case-duplicate fields:** `brownfield-land` uses `Deliverable`, `Hectares` and `Notes`, which duplicate lower-case fields.
  Should they be renamed in that dataset?
- **Warnings on quotations:** 584 `make check` warnings come from quotations with a `terms` list naming terms which were deliberately not created (`committee`, `proprietor`, `a`, `b`).
  Should those entries be removed from `terms`, or the warning silenced?
- **Legislation:** XML could not be downloaded for 6 of 153 instruments.
  Which should be fetched by hand, and are all 153 in scope?
- **Singular names:** `make check` does not yet enforce singular references.
  What should the exception file hold, for names such as "Archaeological remains" and "Energy and renewable statistics"?
- **Topic coverage:** a topic such as "Development plan and timetable" has several datasets, and a dataset can sit in only one topic.
  Should a dataset be able to have more than one topic?
