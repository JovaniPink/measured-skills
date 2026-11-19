# Code review and system impact journey

This follow-up implements the maintainer-authorized audit refinements from the
November 17 baseline `fd3c088efca83c6cf09d499aa6e94393931ba0aa`. It keeps the
0.19.0 preview, 90 skills, four packs, and client invocation controls intact.

## Changes and acceptance criteria

| Change | Required behavior |
| --- | --- |
| Review vocabulary | Code review, pull request review, and review this PR rank Review a change first. |
| Role and lifecycle discovery | Preparation, feedback assessment, system impact, and postrelease learning each have a focused read-only route. The original first seven navigation tasks retain their order. |
| Specific task phrases | A more specific contained phrase outranks an equally scored generic phrase; exact, substring, fuzzy, and named-skill thresholds retain their meaning. |
| Review scope | A named PR uses its committed comparison. Staged, unstaged, and untracked contents enter a review only when the requested scope includes the working tree. Pasted diffs remain valid scoped input. |
| Evidence and claims | Current status separates the November 17 candidate from the November 5 freeze and the bounded November 16 native observations. |
| Reusable practice | The review guide gives authors, reviewers, and maintainers no-install requests, a conditional retry example, and a link from review to observed outcomes. |

The registry now has 21 tasks. New tasks use existing skills: `request-review`,
`address-review`, `assess-change-impact`, and `learn-after-launch`. They prepare
analysis and drafts only. Selecting one does not authorize edits, test execution,
messages, installations, or publication. Repair and draft-PR maintenance remain
explicit existing scopes.

## Review and verification

The discovery and scope regressions reproduced the original failures before the
fixes. An independent source review found a strict typing failure in the new test
helpers; the annotations were corrected and the strict typing check passed. The
review found no additional introduced source blocker in its inspected boundary.

The integrated candidate must pass the repository's workflow, typing, lint,
generation, packaging, deterministic validation, and unit-test gates. The final
PR records commands and results against its actual head. The discovery export's
`source_revision` identifies committed inputs; the release manifest's
`source_commit` identifies the generated artifact source. Preserve both ancestors
with a merge commit.

The website consumes a pinned copy of the same generated catalog and matcher.
Its own review covers exact skill results, task and scope selection, clipboard
behavior, consent-gated categorical events, and the review-led introduction.
Website build and browser results belong to that repository and revision.

## Qualification boundary

These deterministic regressions and source reviews do not establish native-model
behavior, client installation acceptance, human comprehension, conversion, time
savings, or deployment. Earlier observations retain their recorded revisions and
limitations. The [current release status](../release-status.md) and
[release decision](release-decision-0.19.0.md) keep remaining gates explicit.

The synthetic retry example is original teaching material. Its findings depend
on the stated identity, uniqueness, conflict handling, and side-effect boundary;
it is not captured assistant output or an executed result.
