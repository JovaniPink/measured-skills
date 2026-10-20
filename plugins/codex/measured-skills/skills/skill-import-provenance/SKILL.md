---
name: skill-import-provenance
description: "Reviews an owned skill transfer when explicitly asked to import it; checks ownership, license, exact source, and public boundaries before any copy or installation."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "explicit"
  provenance: "original"
  risk_class: "trust-decision"
---

# Skill Import Provenance

Keep owned original work and primary authorities separate from external rejection evidence. Read [provenance record](references/provenance-record.md) before proposing an owned-source transfer.

## Workflow

1. Resolve the exact owned source, revision, artifact, author, license, destination, and authority for the proposed transfer.
2. If the source is a third-party skill catalog, stop. Do not track, cite, mirror, adapt, vendor, or use it as an implementation source. Keep authorized investigation outside this repository and its distributions. Separately governed private research may retain original assessments, permalinks, and hashes under its own policy; it cannot supply imported prose, structure, or implementation authority here. Public behavior still requires owned work, primary authorities, and original evidence.
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

## Example

Synthetic example; not an observed client result.

Input: An owned skill transfer lacks an exact source revision.

Output: Transfer is blocked until source identity and ownership evidence are established. Do not copy an unidentified payload into the destination.
