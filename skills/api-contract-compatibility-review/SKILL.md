---
name: api-contract-compatibility-review
description: Review API, event, schema, and client changes for backward, forward, and rollout compatibility. Use when producers and consumers may upgrade independently or when a change can alter behavior, shape, timing, errors, or semantics.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# API Contract Compatibility Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://www.rfc-editor.org/rfc/rfc9110.txt).

## Workflow

1. Inventory producers, consumers, versions, transports, schemas, ownership, and independent deployment paths.
2. Compare request, response, event, error, authentication, pagination, ordering, idempotency, and timing semantics.
3. Identify additive, breaking, ambiguous, or behaviorally breaking changes, including optionality and default shifts.
4. Review tolerant-reader assumptions, unknown fields, enum expansion, precision, units, locale, and time handling.
5. Define contract tests and compatibility fixtures across old and new producer-consumer combinations.
6. Specify negotiation, versioning, deprecation, rollout, telemetry, and rollback behavior.
7. Separate documented contracts from accidental implementation behavior and unratified proposals.

## Boundaries

- Do not call a change backward compatible from schema shape alone.
- Do not remove or reinterpret a field without consumer evidence and deprecation authority.
- Passing one consumer test does not prove compatibility for unknown consumers.

## Output

Return Contract inventory, Compatibility findings, Consumer risk, Test matrix, Rollout, Deprecation, and Unresolved authority. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. Mark each finding `new`, `unchanged`, `updated`, or `absent` against the pinned base revision.
