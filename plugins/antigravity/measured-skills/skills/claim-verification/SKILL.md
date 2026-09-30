---
name: claim-verification
description: Verify claims that work is complete, broken, missing, merged, deployed, or live by checking the relevant repository and platform evidence. Use when a review, handoff, PR, agent, or collaborator makes claims that would materially change the next action.
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

## Output

Return the supported verdict first, then a claim table with `Claim`, `Verdict`, `Authority`, and `Evidence`. Include confirmed work to preserve, actual gaps, unresolved evidence, and the next justified action only where applicable.

## Continuity and evidence

State the supported verdict before the claim table. Preserve authority, exact evidence, and freshness for each claim. Omit empty gap categories and do not invent remediation when every requested claim is confirmed.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
