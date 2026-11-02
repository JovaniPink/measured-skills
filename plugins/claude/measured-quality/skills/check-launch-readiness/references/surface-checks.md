# Surface checks

Select checks that match the launch surface and its actual risks.

## Web

- routes, navigation, forms, metadata, assets, responsive behavior, accessibility
- privacy and terms accuracy, consent behavior, storage, analytics, third parties
- domain, TLS, redirects, caching, environment variables, error pages
- real-browser smoke checks and user-visible production behavior

## Service or data system

- API and schema compatibility, authentication and authorization, limits
- migrations, backfills, writer cutover, reconciliation, data-quality checks
- logs, metrics, alerts, error budgets, retry and idempotency behavior
- rollback, replay, disaster recovery, ownership, and operational runbooks

## Application

- supported OS and device matrix, permissions, offline and upgrade behavior
- signing, entitlements, store metadata, privacy declarations, review state
- crash reporting, analytics consent, deep links, notifications, data deletion
- archive or release build plus device-level smoke evidence

## Every surface

- exact release revision and artifact
- known issues and explicit waivers
- support and incident ownership
- backup or rollback path tested at the appropriate level
- public copy limited to capabilities supported by current evidence
