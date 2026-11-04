# Explanation and scope review

Date: 2026-11-04. Status: implementation and manual preparation; no receiving-client
model run or new acceptance. Baseline: main at `0a972d7b`, including the merged
chooser usability work. The catalog remains 90 skills in four packs, with 73
implicit and 17 explicit-only skills.

## Problem and decision

The existing catalog covers code explanation, requirements, rationale and bounded
review, but the default review action does not visibly connect those capabilities
into a facts-first assessment of a PR's necessity. Add one optional action under
**Review a change**, backed by a self-contained reference in `review-code-change`.
Keep ordinary defect review and its existing prompt unchanged.

The new action first inventories material behavior and operational changes, then
compares them with requirement evidence and smaller alternatives. Unknown intent
is not proof that removal is safe. The reviewer must preserve necessary security,
compatibility and recovery behavior and investigate an owner's premise rather
than automatically agree. Known product context is supplied up front.

The action is read-only: no edits, test execution, builds, delegation, external
comments, approvals or publication. One pass consumes the existing review budget;
it does not reset earlier rounds. Existing invocation classifications and client
exclusions remain intact. Selection, loading and useful output remain separate.

## Source disposition

Sources inspected during the November 4 research; the implementation is original
workflow text. No external skill implementation or article prose is imported.

| Source | Adopted or adapted | Limit |
| --- | --- | --- |
| [Lightman Miao, Don't review agent code. Interrogate it.](https://dev.to/lightman_miao_fcd6ce02a1c/dont-review-agent-code-interrogate-it-25pd), October 25, 2026 | Facts before judgment; require an explanation for material added mechanisms | Author anecdote, not a controlled dataset. The reported 30 PRs do not establish effectiveness or support skipping required human review. Missing rationale does not authorize deletion. |
| [Google, What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Review design, functionality and unnecessary complexity in context | General engineering guidance, not acceptance evidence for this mode. A summary does not replace required inspection. |
| [Google, The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html) | Prefer technical evidence to preference; avoid perfection as a gate | Does not authorize merging or change repository approval rules. |
| [Martin Fowler, Yagni](https://martinfowler.com/bliki/Yagni.html), May 26, 2015 | Distinguish speculative features from useful enabling work | Does not prove that every abstraction or future-facing change is unnecessary. |

## Implementation and evidence boundaries

- The shared registry adds `explain-scope` only to the existing `review` route.
  It reuses current task fields and the installed `review-code-change` identity.
  Generated offline and bundled guides receive the same prompt and action metadata.
- Literal search phrases expose this action's route; they do not infer arbitrary
  intent or grant authority. All five client prompts retain read-only boundaries.
- A regression first failed because the new mode was rejected and absent. Tests
  cover its restricted route, existing-prompt preservation, native/ordinary
  prompt correspondence, generated presentation and standalone reference delivery.
- The prior chooser wording regression is bound to its historical main checkpoint;
  current prompts still preserve every earlier standing limit. This does not
  rewrite historical observations or turn new guidance into acceptance.
- `docs/private-overlays.md` now uses `review-data-authority`, the current name.
  Historical migration records retain former names. Private product context stays
  with its owning repository; no public task dossier is introduced.

The companion manual lab preparation uses six synthetic decisions, including
necessary complexity, absent context and a misleading owner objection. It is not
an automated runner, measured effectiveness, or another release gate. Existing
Haiku results, preparation packets and source-freshness records are preserved.
The two-Mac companion links this committed contract and requires independent
source/loading checks; it does not alter staging tools, receipts or installations.

Before delivery, run the local repository gates and regenerate discovery,
distributions and archives. Preserve the source/artifact commit followed by a
manifest-only commit. Record exact test outcomes in the draft PR; do not infer
client behavior, human usability or release readiness from local checks.
