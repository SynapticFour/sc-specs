# GA4GH Differences

- SC uses ULID, GA4GH DRS uses arbitrary string IDs
- SC /stream combines access method resolution + streaming in one call
- SC sc-query is more generic than Beacon (Beacon is genomic-specific)
- SC error format is RFC 9457; GA4GH has its own error schema
