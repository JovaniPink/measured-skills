---
name: salesforce-apex-engineering-profile
description: Apply focused Salesforce, Apex, and Lightning Web Components engineering judgment after repository gate discovery. Use for metadata projects, packages, governor limits, data access, tests, compatibility, and deployment readiness; preserve separate live-org authority.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Salesforce, Apex, and LWC Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when Salesforce-specific gates or hazards determine the result.

## Workflow

1. Discover project configuration, package directories and dependencies, API versions, metadata manifests, org-shape assumptions, Apex, Lightning Web Components, permission metadata, destructive-change manifests, and repository scripts.
2. Follow repository-defined commands and pinned Salesforce CLI, Node, and package versions before suggesting defaults.
3. Review Apex hazards, especially bulk behavior, governor limits, record sharing, object and field permissions, query and DML placement, transaction boundaries, callouts, asynchronous work, recursion, and test data isolation.
4. Review Lightning hazards, including client-server contracts, reactive state, wire and cache behavior, browser security, accessibility, and permission-aware data access.
5. Select proportionate local static, lint, unit, package, manifest, and build gates. Treat any org-backed validation as external state requiring exact target-org and credential authority.
6. Review compatibility across API versions, package dependencies, namespaces, org features, metadata availability, Apex contracts, LWC targets, permissions, and deployment order.
7. Report every missing tool, skipped command, unavailable org, or unverified feature as incomplete rather than passing.

## Boundaries

- Do not infer a default org, use credentials, create a scratch org, install a package, run an org-backed test, deploy, or apply destructive changes without separate authority.
- A local parse, lint, or generated deployment archive does not prove org acceptance or live behavior.
- Keep metadata review, local validation, org validation, deployment, permission assignment, and live verification as separate evidence states.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Org evidence boundary, Missing evidence, and Next safe gate.
