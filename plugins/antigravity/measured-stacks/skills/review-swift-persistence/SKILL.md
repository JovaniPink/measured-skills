---
name: review-swift-persistence
description: "Reviews Swift persistence when SwiftData identity, context ownership, deletion, migration, or sync behavior is uncertain; does not assume CloudKit or authorize data mutation."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-stacks"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Swift Persistence Contract Review

Read [persistence review contract](references/persistence.md) only when its checks apply to the task. Project-local copies include a project contract; compare it with current repository settings before relying on it.

## Workflow

1. Identify the actual persistence engine, containers, configurations, model versions, authoritative write entrypoints, and synchronization protocol. Do not infer CloudKit from SwiftData.
2. Trace user intent to the owner that commits a write. Inspect model identity, relationships, defaults, deletion/tombstone semantics, and derived values.
3. Review schema changes against stored data and the supported application versions. Separate migration design from permission to execute a migration.
4. Check context/actor ownership and evidence for save failures, rollback, partial synchronization, and retries. Use synthetic records for proposed tests.
5. Return a contract map, verified defects, compatibility risks, and missing evidence. If this feature has no persistence boundary, return Not Needed. Do not mutate records or source.

## Boundaries

Do not enable cloud synchronization, delete durable data, migrate schemas, or treat an assistant-derived summary as authoritative. Preserve the project-defined mutation owner.

## Evidence and output

Report the authorized scope, applicable settings, observed evidence, result, missing evidence, and next bounded check. Use Not Needed when no applicable authorized work exists and Blocked when a required precondition is missing. Do not substitute required headings for semantic compliance or invent executed checks.

## Editable ordering

Separate draft order from durable order. Moving an item must preserve its ID and any unsaved fields keyed by that ID. Review no-op, boundary, invalid/stale-ID, deletion, cancellation, failed-save, reopen, and synchronization cases. Order-only changes must not accidentally create domain events. Preserve the existing conflict protocol; adding a drag gesture does not authorize a schema migration.

## Example

Synthetic example; not an observed client result.

Input: Two SwiftData contexts edit the same model and sync behavior is unspecified.

Output: Map context ownership and conflict handling. Persistence configuration alone does not establish synchronization or safe concurrent writes.
