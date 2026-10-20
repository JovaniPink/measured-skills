---
name: claim-verification
description: "Checks claims such as \"is this done\", \"did that deploy go out\", or \"is the fix live\" against current evidence; keeps local tests, merge, deployment, and live behavior separate."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Claim Verification

Turn each material claim into a falsifiable statement, then verify it against the authority capable of proving it.

## Workflow

1. Preserve the claim's original meaning. Split bundled claims into independently testable statements.
2. Identify the required evidence class:
   - repository state for file, code, test, and configuration claims
   - Git hosting state for PR, review, check, and merge claims
   - provider state for deployment, configuration, traffic, and acceptance claims
   - runtime observation for user-visible or production behavior
3. Inspect current evidence directly. Do not use a PR description, stale local checkout, generated summary, or curated repository page as proof of a different authority.
4. Classify each claim as `CONFIRMED`, `REFUTED`, `PARTIAL`, or `UNVERIFIABLE`.
5. Separate verified work that must not be redone from actual gaps.
6. Recommend the smallest action supported by the evidence. Do not implement it unless the user also asked for a change.

## Evidence rules

- Cite files and lines for repository claims when practical.
- Record exact branches, revisions, check names, provider resources, timestamps, or URLs when they determine the verdict.
- Treat passing static checks, merge, deploy, live traffic, and correct behavior as separate facts.
- Say what could not be checked and why. Never convert missing access into a passing verdict.
- Re-read drift-prone evidence immediately before a conclusion that depends on it.
- Similar names do not prove that two resources, branches, or environments are the same. Confirm identity by identifier, URL, or direct inspection.
- When the user disputes a verdict and current evidence still supports it, state the evidence once and record the disagreement. The verdict changes only with new evidence, while the user's direction still decides the next action.

## Output

Lead with the supported verdict, then a claim table containing the claim,
verdict, authority, exact evidence, and freshness. Preserve confirmed work and
include actual gaps, unresolved evidence, and a next justified action only where
applicable. Omit empty categories; do not invent remediation when all requested
claims are confirmed.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: Tests passed locally, but the deployed revision is unknown. Is the fix live?

Output: Local checks passed. Live deployment is unverified because no serving revision or runtime observation was supplied.
