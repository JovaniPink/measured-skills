---
name: dependency-supply-chain-review
description: "Reviews dependencies and build inputs when asked whether a package, lockfile update, CI action, or artifact can be trusted; checks provenance and integrity without installing it."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Inventory, Provenance evidence, Findings, Reachability, Build risks, Recommended controls, and Claim limits. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. No change is pinned in this review, so do not assign a finding state.

## Example

Synthetic example; not an observed client result.

Input: A CI action changes from a commit SHA to a moving branch.

Output: warning: the build input is no longer immutable. Review the intended revision and restore a verified immutable reference.
