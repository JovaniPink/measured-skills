# Provenance Policy

Every canonical skill has an entry in `provenance/catalog.json`.

## Capability dispositions

- `covered`: a shipped public skill supplies the generic capability
- `partial`: a shipped public skill covers part of the capability and names the remaining gap
- `public_candidate`: independently authorable and useful across unrelated contexts
- `private_overlay`: correct execution depends on a private authority, identity, topology, contract, dataset, customer, or product
- `rejected`: proprietary, unsafe, obsolete, duplicative, unsupported, or without demonstrated use

Capability disposition is separate from implementation method. An implementation method is `original`, `clean-room`, `adapted`, `vendored`, `reference-only`, or `not-applicable`.

## Required evidence

Each public entry records source URL, license, pinned revision or an explicit non-applicable value, review date, material reviewed, local changes, capability disposition, implementation method, security disposition, re-review triggers, and revocation conditions. `provenance/schema.json` is authoritative and rejects unknown fields, wrong types, invalid dates or URLs, unsupported enum values, and missing required evidence.

Online freshness pins use a strong ETag, a meaningful last-modified value, a byte-level content hash, or a reviewed normalized-content hash. Normalization is limited to named per-request HTML values such as session tokens and telemetry timing; regression tests require substantive authority-content changes to alter the marker.

Use only owned original work and primary authorities needed for format, interoperability, or correctness: laws, specifications, standards bodies, and official platform documentation. Discovery links, community discussions, and third-party skill catalogs are not implementation authorities.

## Public implementation and research boundary

Do not copy external text, examples, names, structure, scripts, or distinctive expression. Third-party skill catalogs are not tracked, cited, mirrored, compared, installed, or used as implementation sources in this repository or its distributions. Keep comparative investigation outside this repository. A separately governed private research repository may retain original assessments, source permalinks, and hashes when its own policy permits them; this exception does not permit importing third-party prose, examples, structure, or behavioral authority here. External investigation may identify questions, rejection criteria, or safety boundaries; public rules require independent primary-authority review and original experiments. Current skills must remain independently authored from owned original work and the applicable primary authority.

Use `original` for newly authored primary-source work after external exposure. Reserve `clean-room` for work whose recorded process supports that description. Preserve historical provenance under its original date; passing an automated independence check cannot establish authorship or lack of exposure.

Repository-independence validation rejects external skill-repository links and install identifiers, repository-to-repository capability mappings, source-specific attribution, and non-primary behavior provenance. Links to repositories owned by the `JovaniPink` GitHub account and pinned CI dependency provenance are narrow operational exceptions; CI dependencies do not authorize skill behavior. `provenance/ci-tools.json` records the exact version, source, license, reviewed wheel hash, and use of every direct or transitive Python tool installed by CI.

## Owned adaptation records

`source_url` identifies the format or correctness authority. An owned adaptation also records `owned_origin`, which identifies its implementation lineage separately: a full ancestor commit in this public catalog, the same skill's canonical entrypoint path, the entrypoint SHA-256, and the MIT LICENSE SHA-256 at that commit. `pinned_revision` must equal that owned revision. Current validation requires the Git objects, their ancestry, and both hashes to match. Private origin names and mappings are not required or published.

This is evidence for a declared owned adaptation, not a comprehensive authorship or licensing certificate. It does not authorize third-party skill imports. Do not replace an unsupported clean-room label with an unsupported original label. The [originality disposition](audits/originality-disposition-2026-10-20.md) separates the four corrected owned adaptations from the [40 corrected process declarations](audits/clean-room-declaration-review-2026-10-20.md) and the unaccepted release qualification. Current labels are 83 original and four adapted. The retained write evidence supports the declared method; it does not independently qualify expression or licensing.

The primary-authority URL check has three exact resource exceptions: OWASP's official ASVS 5.0.0 JSON requirement document and CPython's official 3.15-branch documentation contents and unittest sources on their raw-content host. These are primary documents, not external skill implementations. The full response remains content-hashed, and the global review-age limit remains in force. No general repository-host exception is granted. The source branch can change; this binding does not assert an immutable release or the latest standard version.

## Placement policy

A capability belongs in the public core only when it is reusable across independent contexts, independently sourceable, safe to expose, and testable without private facts. It belongs in a private overlay when correct use depends on a private authority, identity, topology, contract, dataset, customer, or product. It belongs in neither when it is proprietary, unsafe, obsolete, duplicative, unsupported, or lacks demonstrated use.

## Revocation

Remove an item from generated distributions and marketplaces through ordinary reviewed commits when its license, authorship, security behavior, or provenance cannot be supported. Preserve Git history and a migration notice in `deprecated/` when users need a safe replacement path.
