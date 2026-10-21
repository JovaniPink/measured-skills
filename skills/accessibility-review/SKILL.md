---
name: accessibility-review
description: "Reviews accessibility when asked to check keyboard access, screen-reader behavior, focus, contrast, or WCAG requirements; incomplete testing cannot establish conformance."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Accessibility Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://www.w3.org/TR/WCAG22/).

## Workflow

1. Identify supported surfaces, technologies, content types, user journeys, and stated conformance target if any.
2. Inspect semantics, names, roles, values, headings, landmarks, labels, errors, status messages, and focus management.
3. Test keyboard order, traps, shortcuts, pointer alternatives, motion, timing, and input assistance.
4. Review contrast, text scaling, reflow, zoom, orientation, target size, spacing, and non-text alternatives.
5. Map each finding to an exact WCAG 2.2 success criterion and level when supported.
6. Separate automated findings from keyboard, screen-reader, magnification, cognitive, and user testing needs.
7. Record environment, browser, assistive technology, viewport, zoom, and evidence limitations.

## Boundaries

- Do not claim WCAG conformance from automated scans or partial surface testing.
- Do not treat overlay widgets as substitutes for accessible product behavior.
- Do not include sensitive user data in screenshots or test evidence.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Scope, Findings by criterion, User impact, Automated evidence, Manual evidence, Untested areas, and Remediation priority. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. When a pinned change is under review, mark each finding `new`, `unchanged`, `updated`, or `absent` against the state before the change; otherwise report severity alone.

## Example

Synthetic example; not an observed client result.

Input: The checkout dialog opens, but Tab moves behind it.

Output: warning: focus escapes the active dialog. Keyboard users can reach obscured controls; verify focus containment and return focus after close.
