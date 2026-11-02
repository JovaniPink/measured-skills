# Focused checks

Primary documentation: [official Go Engineering Profile reference](https://go.dev/doc/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect `go.mod`, `go.work`, Go source, toolchain directives, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review goroutine leaks, cancellation loss, races, nil interfaces, error wrapping, resource lifetime, map or slice aliasing, and unstable public APIs.

## Gate families

Consider repository scripts, `gofmt`, compilation, tests, vetting, race checks, fuzzing, vulnerability checks, and builds when configured and safe. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check module paths, minimum Go version, build tags, generated code, cgo, platform targets, and semantic import versioning. Record unavailable tools and environments explicitly; never manufacture a passing result.

