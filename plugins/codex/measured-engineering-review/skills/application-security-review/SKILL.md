---
name: application-security-review
description: Review application or service security against current threat evidence and verifiable control requirements. Use for read-only assessment of authentication, authorization, input handling, data protection, session, error, configuration, and abuse risks; do not use this skill to audit agent packages.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Application Security Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://owasp.org/www-project-application-security-verification-standard/).

## Workflow

1. Define assets, actors, trust boundaries, entry points, sensitive operations, and credible abuse cases.
2. Inspect architecture, code, configuration, tests, and runtime evidence for relevant controls.
3. Map findings to versioned OWASP ASVS requirements where the evidence supports an exact mapping.
4. Use the OWASP Top 10 only for awareness and risk framing, not as a verification checklist.
5. Classify each finding by exploit preconditions, impact, likelihood, evidence, and remediation priority.
6. Identify missing tests, logging, rate limits, failure behavior, secret handling, and deployment controls.
7. Separate code findings from provider configuration and unobserved runtime risk.

## Boundaries

- Do not claim OWASP compliance, certification, or complete coverage from this review.
- Do not run exploit payloads against systems without explicit authorization and a safe test boundary.
- Use skill-security-review for agent skills and plugins; this skill evaluates applications and services.

## Output

Return Threat scope, Verified controls, Findings, Evidence gaps, Risk priority, Recommended verification, and Claim limits. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. No change is pinned in this review, so do not assign a finding state.

