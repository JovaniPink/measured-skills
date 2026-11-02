# Focused checks

Primary documentation: [official Adobe Experience Manager documentation](https://experienceleague.adobe.com/en/docs/experience-manager). Confirm the product generation first; AEM as a Cloud Service, AEM 6.5 LTS, and earlier deployments have different contracts.

## Discovery

Inspect Maven modules and dependency management, content packages, FileVault filters, OSGi configuration, Sling models and servlets, HTL, Dispatcher or web-tier configuration, frontend manifests, test modules, and CI or Cloud Manager configuration. Resolve generated content, run-mode ownership, and author-versus-publish scope before selecting gates.

## Judgment focus

Review service-user permissions, repository paths, Sling resolution, OSGi lifecycle, HTL display context, untrusted input, background jobs, content-package filters, mutable content versus code, configuration ownership, Dispatcher filters, caching and invalidation, CDN interactions, redirects, and security headers.

## Gate families

Consider repository Java and frontend checks, unit and integration tests, bundle metadata, FileVault package validation, content validation, Dispatcher or web-tier validation, and builds. Shared SDK startup, package upload, activation, Cloud Manager pipelines, and deployment require separate authority.

## Compatibility

Check AEM product generation, SDK and API baselines, Java version, Core Components, content-package dependencies, Dispatcher tools, browser targets, Cloud Manager rules, and deprecations. Record unavailable tools and environments explicitly; never manufacture a passing result.
