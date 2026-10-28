# Motion terms and evidence checks

Use these terms to explain a finding. Do not require a shared visual style.

## Relationships and evidence

- Chronology says what happened first. Correlation says values vary together. Neither proves causation.
- Modeled causality is a simulation's assumption. Reported causality is a source's claim. Name the source and its limits before endorsing it.
- Revision shows how a record changed. Provenance shows where a claim came from and who can support it.
- Label examples, simulations, predictions, and live observations where readers see them. A realistic animation does not change their evidence status.
- Replay cadence is the speed of presentation. Domain time is when the event occurred. Show both when confusing them could change the reader's conclusion.

## Roles and intensity

Possible roles are orientation, feedback, continuity, sequence, comparison, causality, provenance, uncertainty, and progress. Name the reader action each role helps.

| Level | Local meaning |
| --- | --- |
| M0 | Static content. No motion is needed. |
| M1 | Brief feedback for an action. |
| M2 | An explanatory transition that the reader controls. |
| M3 | Sustained playback or coordinated presentation. |

These levels describe the current design. A higher number is not a better result.

## Accessibility requirements and catalog preferences

Use the stated conformance target and the exact behavior. The [WCAG 2.2 standard](https://www.w3.org/TR/WCAG22/) is the authority. The Understanding pages explain its criteria; they do not add normative requirements.

[Animation from Interactions, 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) is Level AAA. It addresses the ability to disable interaction-triggered motion unless it is essential. Apply it when reviewing that criterion or a separately chosen product requirement. Do not relabel it as AA.

[Pause, Stop, Hide, 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) is Level A. For movement, blinking, or scrolling, check all three conditions: it starts automatically, lasts more than five seconds, and appears alongside other content. For automatic updates alongside other content, there is no five-second exception. Check the essential-activity exception and whether users can pause, stop, hide, or, for updates, control the frequency. A focus-only pause is not a usable pause control. An indirect action such as scrolling into view can start automatic motion, so both criteria may apply.

This catalog also prefers complete static content, a static start for unknown motion preferences, and no automatic replay after returning from a hidden page. Report these as catalog preferences when the criterion does not require them. Keep keyboard, focus, flashing, and screen-reader checks separate; a reduced-motion setting does not prove full conformance.

## Original review examples

A chart labels its data as a simulation, keeps the full table available, and lets readers step through changes. Report that supported behavior. If no reader study exists, leave the comprehension benefit unverified.

A replay hides its conclusion until an animation callback and has a failed keyboard check. Lead with those blockers. Do not lead with its smooth appearance or call the complete experience accessible.

A user asks whether a short button transition fails AA solely because motion cannot be disabled. Explain the AAA criterion and inspect any other applicable criteria. Do not invent an AA failure or a blanket pass.
