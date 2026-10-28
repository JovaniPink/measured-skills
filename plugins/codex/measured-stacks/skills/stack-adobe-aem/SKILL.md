---
name: stack-adobe-aem
description: "Reviews AEM code, Sling, OSGi, Dispatcher, and content packages when an Adobe Experience Manager change needs stack-specific checks; follows discovered versions and Cloud Manager authority."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-stacks"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Adobe Experience Manager Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when AEM-specific gates or hazards determine the result.

## Workflow

1. Determine the exact AEM product generation and discover Maven modules, content packages, FileVault filters, OSGi configurations, Sling models or servlets, HTL, Dispatcher or web-tier configuration, frontend builds, and repository scripts.
2. Follow repository-defined commands, SDK versions, dependency management, and Cloud Manager contracts before suggesting defaults.
3. Review material hazards, especially service-user permissions, repository paths, request and resource resolution, OSGi lifecycle and configuration, HTL display context, untrusted input, serialization, background jobs, and author-publish assumptions.
4. Review content-package ownership and filters, mutable content versus code or configuration, run-mode behavior, Dispatcher filters, caching and invalidation, CDN interactions, redirects, and security headers.
5. Select proportionate repository gates for Java, frontend, unit and integration tests, bundle metadata, FileVault packages, content validation, Dispatcher configuration, and builds.
6. Review compatibility across AEM product generation, SDK and API baselines, Java version, Core Components, content-package dependencies, Dispatcher tools, browser targets, and Cloud Manager pipeline rules.
7. Report every missing tool, skipped command, unavailable SDK, or unobserved pipeline as incomplete rather than passing.

## Boundaries

- Do not copy proprietary project content, read Cloud Manager credentials, start a shared author or publish service, upload a package, activate content, run a pipeline, deploy, or mutate an environment without separate authority.
- A local Maven build or Dispatcher validation does not prove Cloud Manager acceptance, deployment, caching behavior, or production readiness.
- Keep source review, local validation, SDK behavior, pipeline validation, deployment, activation, and live delivery as separate evidence states.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Product generation, Discovery, Hazards, Commands selected, Results, Compatibility, Cloud evidence boundary, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: A Dispatcher rule caches a page containing a signed-in user's name.

Output: warning: the response contains user-specific content. Check cache eligibility and isolation before treating this as safe for shared caching.
