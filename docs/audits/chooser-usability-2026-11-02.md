# Chooser usability change - November 2, 2026

This is an owner change and review, not a usability result. No participant used the new
page, and no model task ran.

## Why

The maintainer tried the public chooser for "Finish existing work" and found it hard to
use. Measurements of the live page (site revision `a78390a`) agree:

| Observation | Measured |
| --- | --- |
| Phone page length (375 by 812) | 30,614 px, about 38 screens |
| First "Copy request" | 5,245 px down, about 6.5 screens |
| Search, assistant and stack controls | All four overflow the phone width by 46 px and clip their text |
| Requests | 110 requests, median 1,168 characters, longest 2,417 |
| Repeated limits | Five boundary sentences appear in 85 of 110 requests |
| Placeholders | 16 requests ask for a "comparison revision" and 17 ask for a "plan file", although the page says you need neither |

## What changed in this repository

- Requests no longer ask a person to supply a comparison revision or a plan file. They
  tell the assistant to discover both and say so when none exists. The few places that
  need a plan now ask for a "reviewed plan" as a path, link or short description.
- Each route declares the exact fields its requests use, with a label and a hint. A
  check fails if the fields and the placeholders in the requests disagree.
- The seven standing limits (five boundary sentences and two wordings of the
  missing-skill fallback) are named once as data. Every request still carries every limit
  it carried before. The site can dim them instead of hiding them.
- Each action exposes structured facts (skill, pack, invocation, starter-set membership,
  availability, native commands) so the page can say it in plain words.
- Assistants have short labels. The old longer labels are kept as notes.
- The example result for finish-work no longer starts with a hedge. Pages label it once.
- Ten requests had a double space between sentences. They are single-spaced now, and a
  check requires every request to be single-spaced sentences so the page can show and
  copy the same text.

## Equivalence

A test compares every request with its predecessor at `773e72f6` sentence by sentence.
The only permitted differences are the four rewritten opening sentences, one comparison
phrase in the review request and the `[PLAN_FILE]` to `[PLAN]` rename. A second test
shows that no request lost a standing limit. The generated Markdown guide and the offline
chooser keep their structure; the offline chooser now also shows the assistant note.

## Effect on generated files

Only the `choose-workflow` skill's generated reference (`workflow-index.md`) changed. It
is rebuilt from the requests, so it follows them. That changes three plugin trees, one of
the 90 Claude.ai archives and the release manifest. No `SKILL.md`, invocation class,
license or other skill changed. The other 89 archives are byte-identical.

## Effect on the prepared Haiku retest packet

The prepared (unrun) Claude packet stages a copy of `choose-workflow`. That staged
`workflow-index.md` no longer matches the current Claude projection. The planned task
does not use that file, but the earlier statement that all 31 staged files match the
current projection applies only to the source before this change. The staged plugin must
be rebuilt and re-hashed, and the static preflight repeated, before any task. This does
not need a model request.

## Limits

- No uncoached participant, accessibility audit, screen-reader pass or device test is
  claimed. The ten-card exercise remains unscored.
- The site page is a separate change in its own repository and needs its own review.
- The offline chooser was not redesigned; it only gained the assistant note.
- Three modes (finish-work assess, maintain-pr prepare and prompt-review assess) use
  their own limit wording, so the page shows no separate standing-limit styling for them.
  Their reviewed wording was not rewritten to force uniformity.
- The long hand-written guides in `docs/finish-existing-work.md` and
  `docs/feature-development-workflow.md` still use the old placeholder names in their own
  examples. They are not generated from the chooser and were left for a later pass.
