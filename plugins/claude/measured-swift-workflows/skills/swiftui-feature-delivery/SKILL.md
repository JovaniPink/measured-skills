---
name: swiftui-feature-delivery
description: Deliver an explicitly requested SwiftUI feature within approved files and targets. Use for bounded implementation with state ownership, availability, accessibility, and test evidence; do not trigger for read-only review or generic Swift questions.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-swift-workflows"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# SwiftUI Feature Delivery

Read [state, availability and acceptance](references/delivery.md) only when its checks apply to the task. Project-local copies include a project contract; compare it with current repository settings before relying on it.

## Workflow

1. Establish the requested behavior, acceptance journey, targets, existing edits, and repository instructions before selecting an implementation.
2. Read deployment targets, language mode, default isolation, schemes, and dependency policy. Consult only the relevant reference sections and installed-version authorities.
3. Build a deduplicated repository-relative allowlist from the authorized task and current tracked/untracked changes. Existing changes are evidence, not automatic permission. Exclude dependencies, generated output, build caches, and signing material. If no authorized path remains, return Not Needed.
4. Implement the smallest coherent slice. Keep one state owner, stable identifiers, cancellable effects, explicit error recovery, and supported APIs. Check Dynamic Type, semantic control labels, Reduce Motion, and compact/regular layouts where applicable.
5. Run the narrow behavior check, then applicable existing gates. Inspect the final diff against the allowlist. Report edits, observed checks, missing journey evidence, and remaining risks separately.

## Done when

The slice is done when the requested behavior works within the allowlist, the narrow behavior check and applicable gates pass or are reported as unavailable, and the final diff matches the allowlist. Stop and ask only when the slice needs a path outside the allowlist, an action listed under Boundaries, or a product decision the repository cannot answer.

## Boundaries

Never run repository-wide mutating formatters or add dependencies, raise targets, alter signing/entitlements, migrate persistence, or perform external writes without explicit task authority.

## Evidence and output

Lead with the result and anything that needs the user's decision. Then report the authorized scope, applicable settings, observed evidence, missing evidence, and next bounded check. Use Not Needed when no applicable authorized work exists and Blocked when a required precondition is missing. Do not substitute required headings for semantic compliance or invent executed checks.
