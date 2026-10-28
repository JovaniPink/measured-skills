# Gate discovery

Use only the rows matching the target repository. Repository instructions and CI remain authoritative.

| Stack signal | Common discovery surfaces | Candidate gates to confirm |
|---|---|---|
| Adobe AEM | Maven modules, content packages, Dispatcher or web-tier configuration, CI | repository Java and frontend checks, bundle and FileVault validation, Dispatcher validation, tests, build |
| C# / .NET | solution and project files, `global.json`, NuGet configuration, CI | repository analyzers, compile, test, package, compatibility, and build checks |
| Go | `go.mod`, `go.work`, CI | `go test`, `go vet`, project linters, build |
| Java / Spring | Maven or Gradle manifests and wrappers, toolchains, CI | wrapper-backed static analysis, compile, test, integration, package, and build checks |
| PHP / Drupal | Composer files, extension metadata, configuration paths, CI | repository coding standards, static analysis, unit, kernel, functional, frontend, and build checks |
| Python | `pyproject.toml`, lockfiles, `tox.ini`, CI | project test, type, lint, package, and migration checks |
| Salesforce / Apex | `sfdx-project.json`, package directories, metadata manifests, CI | local static, lint, unit, manifest, package, and build checks; org-backed validation remains separate |
| Swift | `Package.swift`, `.xcodeproj`, `.xcworkspace`, CI | SwiftPM tests or explicit `xcodebuild` scheme and destination |
| TypeScript / JavaScript | `package.json`, workspace files, CI | declared lint, typecheck, test, and build scripts using the committed package manager |
| SQL | migration config, model directories, warehouse docs, CI | formatter or parser, migration checks, engine-specific tests, data-quality queries |
| Terraform | `.terraform-version`, lockfile, modules, CI | format check, init without backend when appropriate, validate, lint, and plan |

## Selection checks

- Prefer commands already used by CI or documented for contributors.
- Inspect lockfiles before choosing a package manager or tool version.
- Confirm required services, credentials, simulators, or remote backends before running a gate.
- If a command can mutate tracked files or external state, use its check-only form or request authorization.
- When no gate exists, report the missing contract and suggest a gate; do not invent a passing substitute.
