---
reference: environment
name: Environment
cardinality: '1'
datatype: string
entry-date: '2026-11-12'
guidance: 'Indicates which environments the dataset is available in. One of `development`, `staging` or `production`. Each value includes the environments before it: `production` means available in production, staging and development; `staging` means available in staging and development; `development` means available in development only. If not set, the dataset is not available in any environment.'
parent-field: identifier
typology: value
---
