---
name: nextjs-cache-auth-boundary-review
description: Review Next.js authorization and cache boundaries across reads, server mutations, cookies, invalidation, and user-specific data. Read-only; do not trigger for unrelated UI, installing authentication, or enabling Cache Components without a requirement.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-nextjs-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Next.js Cache and Auth Boundary Review

Read [authorization and cache tracing](references/boundaries.md) only when its checks apply to the task. Project-local copies include a project contract; compare it with current repository settings before relying on it.

## Workflow

1. Discover installed framework/version, cache configuration, auth capabilities, route handlers, server actions, and repository authority. Read version-matched docs rather than assuming canary behavior.
2. Map each relevant read and mutation to its principal, authorization check, data owner, cache key/scope, and invalidation behavior.
3. Check authorization at the actual server-side boundary; a hidden UI control or optimistic proxy check alone does not authorize a mutation. Review user-specific data for cross-principal cache reuse.
4. Inspect version-specific cookie/header and cache semantics, errors, revalidation, logout/revocation behavior, and evidence for isolation. Do not recommend enabling unused cache/auth features merely to complete the checklist.
5. Return findings with exact boundaries and executable isolation tests proposed. If neither relevant caching nor authorization exists, return Not Needed. Do not edit code or contact providers.

## Boundaries

Do not install an identity provider, turn on cache configuration, change authorization policy, or make live account requests. Separate documented semantics from observed application behavior.

## Evidence and output

Report the authorized scope, applicable settings, observed evidence, result, missing evidence, and next bounded check. Use Not Needed when no applicable authorized work exists and Blocked when a required precondition is missing. Do not substitute required headings for semantic compliance or invent executed checks.
