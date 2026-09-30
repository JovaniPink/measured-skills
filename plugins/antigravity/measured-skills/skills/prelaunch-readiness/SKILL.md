---
name: prelaunch-readiness
description: Audit whether a web property, service, application, or major relaunch is ready for public use, separating repository checks from provider and live-runtime evidence. Use for launch checklists, release readiness, and go or no-go reviews.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Prelaunch Readiness

Audit only the surface being launched. Read [surface checks](references/surface-checks.md) for the applicable web, service, or application checks.

## Workflow

1. Define the release candidate, revision, target environment, owner, audience, and launch surface.
2. Locate the repository's release contract, runbooks, required checks, and provider configuration.
3. Verify functional, data, security, privacy, accessibility, operability, and rollback evidence proportionate to the launch.
4. Check user-visible claims against actual behavior and maturity. Distinguish prototype, tested, deployed, and publicly available states.
5. Verify platform-only facts from the platform when access exists. Mark them `UNVERIFIED` otherwise.
6. Classify every item as `PASS`, `FAIL`, `WAIVED`, or `UNVERIFIED`; include evidence and waiver owner.
7. Issue `READY`, `BLOCKED`, or `CONDITIONALLY READY` with the smallest list of launch blockers.

## Boundaries

- This skill audits readiness; it does not deploy, change DNS, publish stores, send announcements, or waive failures.
- A successful build does not prove provider configuration or live behavior.
- A merged change does not prove deployment, traffic, data migration, monitoring, or rollback readiness.
- Do not require irrelevant checklist items merely because they appear in a generic template.
