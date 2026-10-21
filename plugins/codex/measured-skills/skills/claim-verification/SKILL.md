---
name: claim-verification
description: "Verifies completion and check results when asked whether work is done, a fix is live, or an old receipt still applies after a change from revision A to B; keeps current proof, historical evidence, and missing checks distinct."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "adapted"
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

A supplied claim and receipt can support a bounded verdict without a checkout.
If only A's passing receipt and the existence of revision B are supplied, report
B as unverified. Do not invent a repository, run checks, or require access merely
to state that evidence limit.

## Evidence rules

- Cite files and lines for repository claims when practical.
- Record exact branches, revisions, check names, provider resources, timestamps, or URLs when they determine the verdict.
- Treat passing static checks, merge, deploy, live traffic, and correct behavior as separate facts.
- Say what could not be checked and why. Never convert missing access into a passing verdict.
- Re-read drift-prone evidence immediately before a conclusion that depends on it.
- Bind each result to its checked revision and inputs. A result at A does not verify B unless a justified scope comparison establishes that the relevant checked inputs are identical; label that comparison separately from execution at B.
- Keep `not run`, `not supplied`, `not found in the inspected scope`, and `does not exist` distinct. Missing evidence cannot establish a failing test, absent coverage, or a completed action.
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

Input: A supplied receipt records 12 passing unit tests at synthetic revision B, observed on 2026-10-20. No serving revision or runtime evidence is supplied. Is the fix live?

Output: The receipt confirms local checks at B; live behavior is unverified.

| Claim | Verdict | Authority | Evidence | Freshness |
| --- | --- | --- | --- | --- |
| The supplied receipt records passing unit tests at B | CONFIRMED | Local test receipt | 12 passes at B | Observed 2026-10-20; applies to B |
| The fix is live | UNVERIFIABLE | Serving configuration and runtime | Neither was supplied | Currentness unknown |

Preserve the local result. Next obtain the serving revision and an authorized runtime observation; the receipt alone cannot establish either.

Input: An old receipt records all checks passing at A. The current revision is B,
and no B receipt or input comparison is supplied. Is the work verified at B?

Output: UNVERIFIABLE at B. The supplied receipt remains historical evidence for A;
no result at B or relevant input-equivalence review was supplied. Next obtain a
B-bound receipt or inspect the changed inputs within the authorized scope. No
check has been run by this review, and the existence of tests is unknown.
