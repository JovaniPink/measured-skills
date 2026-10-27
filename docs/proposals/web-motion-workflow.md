# Design, build, and review web motion

Provisional post-0.18 workflow. The proposed `web-motion-design` skill is not yet
registered or installed. Use these as ordinary requests until a separately
approved release includes it. Do not invent a native command or loading receipt.

## Choose the output

| Route | Example | Completion evidence |
| --- | --- | --- |
| Product interaction | Selecting a stage or changing a filter | State, keyboard, focus, and error/recovery behavior |
| Expressive explanation or atmosphere | A process illustration or pixel-art scene | Choreography, truthful content, controls, and static equivalence |
| Showcase asset | An exported product demonstration | Source fidelity, timing, seams, output format, and labeling |

Production content stays readable and usable without waiting for an animation.
Expressive motion is a legitimate design objective; it does not require every
element to move or every site to share one visual language.

## Design request

> Design motion for [component or route] in [repository]. Read project instructions
> and inspect the current source and design references first. The desired feeling
> and purpose are [intent]. Choose the product, expressive, or showcase route.
> Specify the focal point, choreography, state, interruption, responsive behavior,
> static fallback, and reduced-motion treatment. Keep observed facts separate from
> estimates. Use existing tools and assets. Return a concise implementable spec;
> do not edit code, install dependencies, or publish.

## Implementation request

> Implement [accepted specification] in [repository] within [routes and files].
> Preserve unrelated work. Keep semantic state independent of animation completion
> and keep the static content usable. Run repository checks and inspect the actual
> browser behavior, including keyboard, reduced motion, interruption, and enlarged
> text. Keep visible and accessible labels consistent, and preserve focus when
> playback pauses or the scene leaves view. Record
> exact revisions and unavailable evidence. Leave the change ready for review;
> do not merge, deploy, or release.

If implementation is already authorized in the session, retain that authority.
Do not manufacture an additional approval step for routine decisions within it.

## Review request

> Review [base and head, plus any uncommitted scope] against [specification]. Use
> functional-motion-review when that installed skill is available, and verify its
> loading separately from output quality. Inspect meaning, source truthfulness,
> complete static content, focus, reduced motion, pause/replay, and performance
> evidence. Check speech-control labels and narrow/enlarged-text layouts. Separate
> mocked events from observed browser behavior, and identify evidence made stale
> by later changes. Report concrete findings and limits. Do not edit or publish.

Repair accepted findings under existing implementation authority, rerun affected
checks, and review the changed scope. Self-review is not independent review.

## Two-machine use

On each machine, verify the checkout revision, local instructions, toolchain,
browser versions, and available skills. Reuse the reviewed specification and
source hashes. Do not transfer credentials, client caches, or acceptance claims.
Record a missing Safari, mobile-device, or second-machine check as unavailable or
not run; one successful Chromium run does not establish parity.

## Evidence and recovery

Keep local tests, browser observations, hosted checks, deployment, and participant
findings distinct. A recording is useful review material, not proof of smooth live
performance. A pixel comparison cannot prove usable semantics or comprehension.

Rollback should remove the presentation enhancement while retaining content,
navigation, and domain state. An ordinary source revert is not proof that an
installed copy or deployed site has rolled back.

The [skill proposal](web-motion-design.md) records routing, prepared cases, source
review, and the later registration checkpoint. Neither document expands 0.18.0.
