---
reference: fact
name: Fact
plural: Facts
term: fact
attribution: crown-copyright
description: a field and its value for an entity
entity-maximum: '0'
entity-minimum: '0'
entry-date: '2026-11-12'
fields:
- field: end-date
  guidance: Meaning is yet to be defined. Currently always blank.
- field: entity
- field: fact
- field: field
- field: entry-date
  guidance: The newest entry-date of this fact with the highest priority from the fact-resource dataset.
- field: priority
  guidance: The lowest priority of any fact-Used to order facts into a history, smaller values are higher priority than larger values.
- field: reference-entity
  guidance: The entity referenced by the value, found using the lookup dataset.
- field: start-date
- field: value
key-field: fact
licence: ogl3
phase: alpha
realm: provenance
themes:
- specification
typology: value
---


