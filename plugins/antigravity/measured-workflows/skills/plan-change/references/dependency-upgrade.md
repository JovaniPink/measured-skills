# Plan a dependency or framework upgrade

Use the repository's exact installed and proposed versions. Read the corresponding
publisher migration guide, release notes, runtime requirements, peer constraints,
and support policy. A latest-version suggestion is not a reviewed upgrade path.
For example, [Next.js version 16 migration guidance](https://nextjs.org/docs/app/guides/upgrading/version-16)
includes API, runtime, and bundler changes; the applicable steps depend on the
project's starting version and configuration. Reviewed 2026-10-28.

## Assessment

- Inspect manifests, lockfiles, package-manager version, installation-script policy,
  build/runtime entrypoints, supported environments, and direct/transitive users.
- Trace changed APIs through real callers and configuration. Separate an advisory
  repair from a major upgrade; neither a version bump nor an audit score proves
  compatibility or eliminates all vulnerabilities.
- Review codemods before recommending execution: package/version, files touched,
  transformations, network use, lifecycle scripts, and reversibility. Do not copy
  an unpinned one-line installer from a guide into an execution plan.
- Propose coherent slices, before/after checks, representative runtime behavior,
  rollback limits, and a stopping point. Inspect generated code and lockfile churn.

## Authorized local implementation

This planning skill does not install or edit dependencies. A separate request may
permit the reviewed manifest/lockfile updates and necessary project-local install.
Use the repository's package manager and script policy; review installation scripts
and stop on unexpected execution, access, or spend. Do not use blanket force fixes,
install global tools, or silently change unrelated dependencies.

Compare contracts and affected journeys after each slice. Record tool/version,
command, exact inputs, result, and unavailable environments. Reverting a lockfile
may not undo generated assets, database migrations, caches, or external effects.

Synthetic example: a UI upgrade removes a synchronous request API. Find all
callers and boundary tests, migrate one route, and check its loading/error path.
Passing type checks alone does not verify the rendered route or a deployment.
