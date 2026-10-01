---
name: skill-import-provenance
description: Review provenance before transferring owned original skill material between authorized repositories or distributions. Invoke explicitly for an owned-source transfer or a decision about whether proposed external skill material must be rejected; third-party skill catalogs are never implementation sources.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "trust-decision"
disable-model-invocation: true
---

# Skill Import Provenance

Keep owned original work and primary authorities separate from external rejection evidence. Read [provenance record](references/provenance-record.md) before proposing an owned-source transfer.

## Workflow

1. Resolve the exact owned source, revision, artifact, author, license, destination, and authority for the proposed transfer.
2. If the source is a third-party skill catalog, stop. Do not track, cite, mirror, adapt, vendor, or use it as an implementation source. Any authorized investigation stays outside Git and can influence rejection boundaries only.
3. Confirm ownership, or separately documented authority, for every transferred file, and confirm that the license permits the destination use.
4. Inventory the exact files proposed for transfer and their dependencies, scripts, assets, hooks, and network behavior.
5. Run or obtain a security review appropriate to the package's influence and execution surface.
6. Choose one capability disposition used throughout the catalog:
   - `covered`: an accepted public capability already satisfies the need
   - `partial`: existing public coverage leaves a named gap
   - `public_candidate`: the capability is reusable and can be independently supported
   - `private_overlay`: correct use depends on private context or authority
   - `rejected`: the capability is unsafe, unsupported, obsolete, duplicative, or not permitted
7. For current catalog work, use `original` or an honestly preserved historical `clean-room` method. Do not introduce new `adapted`, `vendored`, or third-party `reference-only` implementations.
8. Record provenance before materializing the transfer using the exact schema field names, including `pinned_revision`, `reviewed_on`, and `reviewed_material`.
9. Apply the smallest authorized change. Preserve required notices and avoid unrelated updates.
10. Validate the result in every supported host and record rereview triggers, update policy, and revocation path.

## Stop conditions

Stop on any third-party skill-catalog source, unclear ownership, incompatible or absent licensing, unverifiable artifact origin, unexplained binary content, unsafe activation, or a review scope that cannot cover the proposed package. Do not install or materialize a rejected source.
