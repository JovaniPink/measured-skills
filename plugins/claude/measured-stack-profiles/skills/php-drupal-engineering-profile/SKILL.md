---
name: php-drupal-engineering-profile
description: Apply focused PHP and Drupal engineering judgment after repository gate discovery. Use for Composer projects, Drupal modules or themes, entity and configuration APIs, caching, security, tests, compatibility, and builds; defer exact commands to repository evidence.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# PHP and Drupal Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when PHP- or Drupal-specific gates or hazards determine the result.

## Workflow

1. Discover Composer metadata and lockfiles, PHP constraints, Drupal core version, custom modules or themes, configuration synchronization paths, service definitions, routes, update hooks, frontend manifests, and repository scripts.
2. Follow repository-defined commands, local development tooling, and pinned PHP, Composer, and Drupal versions before suggesting defaults.
3. Review material PHP hazards, especially type coercion, loose comparisons, nullability, error handling, user-controlled input, output encoding, deserialization, filesystem access, sessions, and environment-specific configuration.
4. Review Drupal-specific boundaries: access checks, entity queries, render arrays, cache tags and contexts, configuration versus state versus content, service lifetimes, plugins, update paths, queues, and request-scoped behavior.
5. Select proportionate gates from repository formatting, static analysis, coding standards, unit, kernel, functional, browser, frontend, dependency, and build checks.
6. Review compatibility across PHP and Drupal core versions, Composer constraints, contributed modules, database drivers, configuration schema, cache behavior, API deprecations, and content update order.
7. Report every missing tool, skipped command, unavailable database, or unsupported runtime as incomplete rather than passing.

## Boundaries

- Do not assume a global Composer, Drush, PHP, database, or local-environment command when the repository defines its own tooling.
- Do not install modules, update the lockfile, import configuration, run update hooks, alter content, deploy, or mutate shared state merely to run a gate.
- Separate static review, executed checks, local-site behavior, configuration import evidence, deployment, and live behavior.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.
