# Focused checks

Primary documentation: [official TypeScript and JavaScript Engineering Profile reference](https://www.typescriptlang.org/docs/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect `package.json`, the matching lockfile, workspace configuration, `tsconfig` files, runtime targets, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review implicit `any`, unsafe assertions, nullability, promise loss, module-system mismatches, environment boundaries, prototype pollution, serialization, and client-server contract drift.

## Gate families

Consider the selected package manager's repository scripts for formatting, linting, type checking, tests, builds, and dependency or vulnerability review. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check Node and browser targets, module format, package exports, TypeScript version, generated types, API schemas, bundlers, and lockfile changes. Record unavailable tools and environments explicitly; never manufacture a passing result.

