---
reference: fact-resource
name: Fact resource
plural: Fact resources
term: fact-resource
attribution: crown-copyright
description: the provenance of a fact
entry-date: '2026-11-12'
fields:
- field: end-date
- field: fact
- field: entry-date
- field: entry-number
- field: priority
  guidance: Used to order facts into a history, smaller values are higher priority than larger values.
- field: resource
- field: start-date
- field: entity
  guidance: The entity this fact belongs to. Denormalised from the fact dataset so provenance can be queried without a join.
- field: field
  guidance: The field this fact provides a value for. Denormalised from the fact dataset so provenance can be queried without a join.
licence: ogl3
phase: alpha
realm: provenance
themes:
- specification
typology: value
---


