# Planning Data design concept model

This repository contains the terms, definitions, data models, information, and content
used to design planning data for https://planning.data.gov.uk
and is presented at https://design.planning.data.gov.uk 

## Content structure

The content is maintained as individual markdown files in the [content](content/) directory
which are designed to be edited using markdown or text editor.
Collectively the content directory is an [Obsidian](https://obsidian.md/) vault.

Each markdown file contains dataset fields as front-matter, with the markdown block being the "text" field.

Each sub-directory in the content directory contains markdwon files of the same type, one file per-entity.
The markdown files in each sub-directory are complied into a CSV files in the [dataset/] directory by the 
make process.

## Related applications

The [planning-data-design](https://github.com/digital-land/planning-data-design) 
web application presents this content and data at https://design.planning.data.gov.uk

The content in this repository will be used to generate specifications and other metadata currently maintained in the 
[specification](https://github.com/digital-land/specification) repository, visible at https://digital-land.github.io/specification/

# Datasets

The following datasets are managed in this repository:

* [content/term](content/term) — a term used in data and on the platform, with synomyms, abbreviations, and acronyms
* [content/extract](content/extract) — a quotation from legislation, policy or other source which defines or references one or more term
* [content/legislation](content/legislation) — act or statutory instrument on legislation.gov.uk
* [content/term-status](content/term-status) — where the text of a term comes from: `legislation`, `guidance` or `draft`
* [content/source](content/source) — a source of information
* [content/topic](content/topic) — topic of data (previously called a "consideration") which can be collective nouns (plural) covering a number of related classes / datasets
* [content/theme](content/theme) — topic category (a "domain")
* [content/user](content/user) — category of user of planning data "as a `user`"
* [content/need](content/need) — "I need to consider `topic` when I `action`" 
* [content/action](content/action) — "apply for certificate of lawful development", "make a decision on a planning application 
* [content/operation](content/operation) — "which means I need to be able to: `operation` from `source-dataset` (plural) using `target-dataset` (plural) which is `quality`"
* [content/quality](content/quality) — data quality level
* [content/quality-dimension](content/quality-dimension) — data quality dimension
* [content/quality-dimension-need](content/quality-dimension-need) — data quality dimension for a given need
* [content/stage](content/stage) — stage in the development process used to sequence needs
* [content/class](content/class) — a type of entity used to create a dataset
* [content/prefix](content/prefix) — a CURIE prefix which can be used to find the `prefix-uri` which can be concatenated with a reference to construct a URI

# Properties

The properties in frontmatter are defined in the specification https://github.com/digital-land/specification/content, specifically each markdown file here contains the following common fields:

- [entity](content/field/entity.md) — a unique number for the entity assigned by planning.data.gov.uk 
- [prefix](content/field/prefix.md) — a CURIE prefix to provide scope for the reference, usually the class/dataset name or the provision reference
- [reference](content/field/reference.md) — a symbolic name for the item, matching the markdown filename
- [name](content/field/name.md) — a displayed singular name for the item
- [plural](content/field/plural.md) — a displayed name for a collectino of the items
- [start-date](content/field/start-date.md) — the date the entity applies from
- [made-date](content/field/made-date.md) — the date the entity was created, enacted or made
- [end-date](content/field/end-date.md) — the last date the entity applied until, otherwise blank
- [entry-date](content/field/entry-date.md) — the timestamp when the data was created or modified
- [documentation-url](content/field/documentation-url.md) — webpage describing the entity
- [document-url](content/field/document-url.md) — a link to a PDF or other document which is the material source of information about the entity which should appear on the documentation-url page

Markdown files should match a lower-case version of the reference, with spaces and other special characters 
not representable in a filename replaced with a hyphen.
Unknown values should be left blank, empty properties don't need to be included in the markdown files.
Dates and other datatypes are defined in the specification.


## Development

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ python -m venv .venv
    $ make init

Rebuld the content:

    $ make

Review your work locally before committing and pushing any changes:

    $ make server    # http://localhost:8000/

## Licence

The software in this project is open source and covered by the [LICENSE](LICENSE) file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
