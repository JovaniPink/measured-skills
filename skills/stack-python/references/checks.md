# Focused checks

Primary documentation: [official Python Engineering Profile reference](https://docs.python.org/3/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect `pyproject.toml`, lockfiles, package layout, environment files, tox or nox configuration, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review mutable defaults, import cycles, dynamic typing gaps, async cancellation, context-manager cleanup, serialization, timezone handling, and environment drift.

## Gate families

Consider repository scripts, formatting, linting, static typing, unit and integration tests, package builds, and dependency or vulnerability checks when configured. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check supported Python versions, packaging metadata, public imports, typing behavior, platform wheels, database drivers, and deprecations. Record unavailable tools and environments explicitly; never manufacture a passing result.


Content binding: [official 3.15-branch documentation contents](https://raw.githubusercontent.com/python/cpython/3.15/Doc/contents.rst). This index does not bind all linked guides or establish the project's interpreter version. Use the installed version's specific documentation for API and compatibility decisions.
