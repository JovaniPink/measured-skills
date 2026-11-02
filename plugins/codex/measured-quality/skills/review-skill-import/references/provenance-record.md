# Provenance record

Record one entry for every authorized transfer of owned original skill material. Do not create a tracked source record for a third-party skill catalog.

```json
{
  "skill": "skill-name",
  "disposition": "public_candidate",
  "implementation_method": "original | clean-room",
  "source_url": "primary format, interoperability, or correctness authority",
  "pinned_revision": "immutable revision or explained retrieval receipt",
  "upstream_license": "format-authority status and confirmation that workflow behavior is independently authored",
  "reviewed_on": "YYYY-MM-DD",
  "reviewed_material": ["paths or artifact identifiers"],
  "local_changes": "material differences",
  "security_review": "report path, URL, or not-applicable with reason",
  "rereview_triggers": ["paths, dependency changes, or release conditions"],
  "revocation": "how to disable, remove, or replace the skill"
}
```

Use the catalog's five disposition values: `covered`, `partial`, `public_candidate`, `private_overlay`, and `rejected`. Use `not-applicable` only where the schema permits it and with a reason. Use an immutable commit or digest for an owned source artifact. Keep licensing evidence and required notices with the transferred material.
