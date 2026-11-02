# Focused checks

Primary documentation: [official Drupal developer documentation](https://www.drupal.org/docs/develop). Use the [official PHP manual](https://www.php.net/manual/en/) for language, runtime, and security behavior.

## Discovery

Inspect `composer.json`, `composer.lock`, PHP constraints, Drupal core and extension versions, custom module and theme metadata, services, routes, configuration synchronization, update hooks, patches, frontend manifests, local-environment definitions, and CI scripts.

## Judgment focus

Review type coercion, loose comparison, input validation, output encoding, deserialization, filesystem and session behavior, access checks, entity-query access, render arrays, cache tags and contexts, configuration versus state versus content, dependency injection, plugin discovery, updates, queues, and deprecations.

## Gate families

Consider repository formatting, coding standards, static analysis, Composer validation, unit, kernel, functional, browser, frontend, dependency, and build checks when configured. Dependency changes, configuration imports, database updates, content writes, and deployment remain separately authorized.

## Compatibility

Check PHP and Drupal core versions, Composer constraints, contributed extensions, database drivers, configuration schema, cache semantics, API deprecations, update ordering, and frontend targets. Record unavailable tools and environments explicitly; never manufacture a passing result.
