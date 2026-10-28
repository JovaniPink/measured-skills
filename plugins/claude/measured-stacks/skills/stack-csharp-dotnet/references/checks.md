# Focused checks

Primary documentation: [official .NET documentation](https://learn.microsoft.com/en-us/dotnet/). Verify version-sensitive behavior against the repository's pinned SDK and target frameworks.

## Discovery

Inspect solution and project files, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, central package management, NuGet configuration, package lockfiles, target frameworks, runtime identifiers, and CI scripts. Resolve generated sources and nested solutions before selecting gates.

## Judgment focus

Review cancellation and task lifetime, sync-over-async, `async void`, `IDisposable` and `IAsyncDisposable`, nullable-reference contracts, dependency-injection lifetimes, deferred LINQ execution, serialization boundaries, and configuration precedence. For Entity Framework Core, inspect query shape, tracking, concurrency, transactions, migrations, and provider-specific behavior.

## Gate families

Consider repository formatting and analyzers, compilation, unit and integration tests, API or package compatibility, packaging, dependency review, and builds when configured. Restore, tool installation, database updates, and external feeds remain separately authorized.

## Compatibility

Check SDK selection, target frameworks, runtime identifiers, package graphs, public API surface, trimming or native AOT assumptions, operating systems, database providers, and migration order. Record unavailable tools and environments explicitly; never manufacture a passing result.
