---
name: application-security-review
description: "Reviews application security when asked to check authentication, authorization, input handling, sessions, or exposed data; returns evidence-based findings without changing controls."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Threat scope, Verified controls, Findings, Evidence gaps, Risk priority, Recommended verification, and Claim limits. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. No change is pinned in this review, so do not assign a finding state.

## Example

Synthetic example; not an observed client result.

Input: The supplied download handler at `api/download.py:24` trusts an object ID without checking tenant ownership. No live attack or access-control test is authorized.

Output: error: object access lacks a tenant authorization check at `api/download.py:24`. The supplied handler is the evidence; no equivalent control was verified in the reviewed scope. A valid identifier could expose another tenant's object, so this access boundary blocks acceptance. Recommended verification: an isolated cross-tenant rejection test and a trace of upstream authorization. Upstream controls and live exploitability remain evidence gaps. This is a static handler review, not a penetration-test result.

## Standard authority

The reviewed [official ASVS 5.0.0 requirement data](https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.json) supports version-qualified mappings. Confirm the project's standard version before mapping; this reference does not establish the latest standard, complete coverage, or compliance.
