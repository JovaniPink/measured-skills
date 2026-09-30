---
name: dependency-supply-chain-review
description: Review software dependencies and build supply-chain evidence for provenance, integrity, maintenance, vulnerability, and compromise risk. Use for a read-only assessment of manifests, lockfiles, registries, build inputs, CI actions, artifacts, and update policy.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Dependency and Supply-Chain Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://slsa.dev/spec/v1.2/provenance).

## Workflow

1. Inventory direct and transitive dependency sources, lockfiles, registries, build tools, CI actions, and produced artifacts.
2. Check version constraints, integrity hashes, immutable pins, maintainer or publisher identity, and unexpected source changes.
3. Review known-vulnerability evidence using current authoritative advisory sources when network access is authorized.
4. Trace the build entry point, external downloads, generated code, credentials, and artifact signing or attestation evidence.
5. Use NIST SSDF outcomes to identify process gaps and SLSA provenance concepts to describe evidence.
6. Assess update, rollback, revocation, dependency confusion, typosquatting, and abandoned-package exposure.
7. Prioritize findings by reachability, exploitability, privilege, and ability to reproduce the build.

## Boundaries

- Do not claim a SLSA level unless independently verified against every applicable requirement.
- Do not update, install, execute, or publish dependencies during a read-only review.
- Absence from an advisory feed is not proof that a dependency is safe.

## Output

Return Inventory, Provenance evidence, Findings, Reachability, Build risks, Recommended controls, and Claim limits. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. No change is pinned in this review, so do not assign a finding state.
