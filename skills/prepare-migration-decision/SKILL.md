---
name: prepare-migration-decision
description: "Prepares a migration decision when owners must approve data writers, cutover, reconciliation, and rollback; records a proposal and evidence without granting approval itself."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Data Authority and Migration Ratification

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Map current authoritative stores, exact-byte custody, projections, writers, readers, and reconciliation paths.
2. Define proposed target authority, allowed writers, read paths, transformations, conflict rules, and data contracts.
3. Describe migration phases, compatibility, backfill, cutover, dual-operation limits, contraction, and cleanup.
4. Specify reconciliation invariants, thresholds, sampling, quarantine, retry, and evidence ownership.
5. Define rollback or roll-forward behavior for code, state, partially migrated data, and downstream consumers.
6. Name the decision owner, consulted owners, required evidence, go or no-go gates, and ratification record.
7. Keep status proposed until the named owner provides explicit ratification evidence.

## Boundaries

- Do not declare a new authority, writer, migration, cutover, or production state ratified without owner evidence.
- Do not execute migrations, enable writes, or change production systems.
- Do not expose private schemas, topology, identities, or customer data in public outputs.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Current authority, Proposed contract, Migration phases, Reconciliation, Rollback, Risks, Decision owner, Required evidence, and Status.

## Example

Synthetic example; not an observed client result.

Input: A proposed cutover changes the only writer, but no owner has approved it.

Output: The writer change remains proposed. Record the deciding owner, reconciliation evidence, rollback condition, and approval status before cutover.
