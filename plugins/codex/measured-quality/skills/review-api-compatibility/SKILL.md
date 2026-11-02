---
name: review-api-compatibility
description: "Reviews breaking API, event, and schema changes when asked whether old clients still work or independent upgrades are safe; checks behavior and rollout order as well as field shapes."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Contract inventory, Compatibility findings, Consumer risk, Test matrix, Rollout, Deprecation, and Unresolved authority. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. Mark each finding `new`, `unchanged`, `updated`, or `absent` against the pinned base revision.

## Example

Synthetic example; not an observed client result.

Input: In the supplied A-to-B API diff, `total` changes from an integer to a string. The supplied older client decoder requires an integer, and those clients remain deployed.

Output: error, new: the response type breaks the supplied older decoder. Contract inventory: A emits an integer; B emits a string; deployed older consumers require A. Evidence is the API diff and decoder contract. Test matrix: decode A and B responses with both old and new clients; results are pending. Preserve the existing type or add a compatible field, then verify consumer migration before deprecating the old contract. The rollout owner and migration completion are unresolved; this review authorizes neither rollout nor deprecation.
