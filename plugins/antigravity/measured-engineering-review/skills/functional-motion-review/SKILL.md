---
name: functional-motion-review
description: Review motion in editorial and data interfaces for clarity, accessible content, and truthful evidence. Use for animation-gated content or sample data presented as live; not routine styling or animation implementation.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Functional Motion Review

Assess whether motion helps a named reader task. Review only; this skill does not authorize code changes, installs, analytics, user recruitment, publication, or deployment.

Read [motion terms and evidence checks](references/motion-evidence.md) before assigning motion roles or intensity, judging replay time, or making an accessibility finding.

## Review

1. Identify the reader's question and the intended benefit. Separate a proposed benefit from observed comprehension findings.
2. Trace each displayed object to its authority, version, timestamp, and evidence kind. Domain state must commit independently of animation completion. Keep live observations, examples, simulations, predictions, and retrospectives visibly distinct.
3. Name the relationship the motion expresses. A sequence or connector cannot prove causation. Use the reference to distinguish chronology, correlation, modeled causality, reported causality, revision, and provenance.
4. Assign a local role and intensity using the reference. These terms describe a review; they are not adoption targets. Ordinary reading can remain static.
5. Inspect complete initial content, document order, native links and disclosures, keyboard operation, focus, non-color labels, reduced motion, and interruption. The catalog prefers a static start when motion preference is unknown and no automatic replay when a hidden page returns. Keep those preferences distinct from WCAG requirements.
6. Compare exact baseline and candidate builds, dependencies, bundle sizes, layout shifts, long tasks, and repeatable lab runs under the same device settings. A Lighthouse navigation result does not measure interaction latency or field Core Web Vitals.
7. Examine consented, counterbalanced task findings when available: errors, completion times, and confusion. Preference and dwell time do not establish comprehension. Keep absent participant evidence explicitly absent. When comprehension evidence is missing, name the smallest check that would supply it: a test-local observation the reviewer can run against the existing build, or a separately consented study with a named owner. Do not propose production instrumentation, a session-recording provider, or a new runnable application to fill the gap.

## Route detailed reviews

- Use `accessibility-review` for criterion-level findings and assistive-technology checks.
- Use `performance-scalability-diagnosis` for measured performance regressions.
- Use `api-contract-compatibility-review` when a presentation change touches producer or consumer contracts.
- Use `authority-boundary-review` if the evidence authority itself is unresolved.

If a companion is unavailable, report that limit and use its primary authority without inventing a completed review. Do not duplicate its full procedure here.

## Stop and report

Reject fake live activity, hidden essential content, unlabeled synthetic outcomes, playback that cannot be interrupted, and analytics scope expansion. Offer a test-local observation or a separately consented study instead of new tracking. Do not repair a domain contract to accommodate animation. Keep each project's terms, runtime, and visual identity local; reuse a recipe only after multiple pilots demonstrate the same behavior. Missing evidence is not an engagement improvement or an accessibility conformance claim.

## Output

Lead with the supported finding about the reader task. Put a blocking failure or incomplete evidence before any proposed benefit. The first sentence states the finding; do not open with file paths, reference titles, or an account of what you read. Attach each source to the finding it supports. Preserve the requested detail, failed checks, uncertainty, and relevant unfinished work.

Then return `Intended benefit`, `Evidence and domain authority`, `Motion role and intensity`, `Static and keyboard behavior`, `Reduced motion and interruption`, `Bundle and performance evidence`, `Comprehension findings`, `Risks`, and `Missing evidence`. Label each conclusion as repository inspection, browser observation, automated test, participant finding, or recommendation. Record the date and exact reviewed revision inside `Evidence and domain authority`, never before the finding. Give a next action only when one is needed.

WCAG 2.3.3 interaction animation is Level AAA. Pause, Stop, Hide (2.2.2) is Level A with separate conditions. Use the reference to assess those conditions; do not describe every motion preference as a universal AA requirement.
