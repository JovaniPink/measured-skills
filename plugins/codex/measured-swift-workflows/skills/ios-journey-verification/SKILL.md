---
name: ios-journey-verification
description: "Verifies a named iOS journey when explicitly asked to run fixture-based acceptance steps on selected schemes; excludes inferred live-data journeys, device claims, and broad simulator resets."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-swift-workflows"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# iOS Journey Verification

Read [fixture journey evidence](references/journeys.md) only when its checks apply to the task. Project-local copies include a project contract; compare it with current repository settings before relying on it.

Read [compatibility and evidence preflight](references/currency.md) before selecting targets or reporting acceptance.

## Workflow

1. Name the journey, fixture boundary, selected scheme, existing test IDs, destination, expected observations, and authorized test paths. Read the project contract before launching.
2. Compute a deduplicated path/test allowlist from task authority and repository state; preserve existing edits and exclude generated/vendor/signing paths. Return Not Needed if no authorized journey remains.
3. Confirm the fixture configuration and that app-hosted tests cannot construct live clients. If that boundary cannot be established, stop and report Blocked before launch.
4. Run only repository-defined commands for the selected scheme/destination. Do not erase broad simulator state, request permissions, export personal data, or change capabilities to make a run pass.
5. Record each expected step as observed, failed, or unobserved with test output or screenshot evidence. Separate unit, app-hosted, simulator, manual accessibility, physical-device, and real backend evidence.

## Boundaries

A passing simulator journey cannot prove model inference, device memory/thermal behavior, live integrations, or manual accessibility. Missing tools and destinations are blockers; never fabricate a pass.

## Evidence and output

Report the authorized scope, applicable settings, observed evidence, result, missing evidence, and next bounded check. Use Not Needed when no applicable authorized work exists and Blocked when a required precondition is missing. Do not substitute required headings for semantic compliance or invent executed checks.

## Example

Synthetic example; not an observed client result.

Input: The fixture opens a form and saves it in the simulator; no physical device was tested.

Output: The selected simulator fixture journey passed. Device behavior remains unverified; report the scheme, simulator, and exact steps tested.
