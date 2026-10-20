---
name: csharp-dotnet-engineering-profile
description: "Reviews C# and .NET changes when ASP.NET, Entity Framework, async code, packages, or target frameworks need focused checks; follows repository SDK and build contracts."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# C# and .NET Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when .NET-specific gates or hazards determine the result.

## Workflow

1. Discover solution and project files, `global.json`, central package configuration, NuGet settings, lockfiles, target frameworks, runtime identifiers, and repository scripts.
2. Follow repository-defined commands and pinned SDK or tool versions before suggesting defaults.
3. Review material hazards, especially sync-over-async, lost cancellation, `async void`, disposal and lifetime errors, nullable-reference gaps, dependency-injection scope mismatches, deferred LINQ behavior, and unsafe serialization.
4. When data access is present, review Entity Framework tracking, query shape, client evaluation, concurrency, transactions, provider behavior, and migration authority.
5. Select proportionate gates from repository formatting, analyzers, compilation, tests, package validation, builds, and dependency review.
6. Review compatibility across target frameworks, SDK selection, package graphs, public APIs, trimming or native AOT, operating systems, and database providers.
7. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal `dotnet` command or replace repository policy with generic preferences.
- Do not restore from an unapproved feed, install tools, update packages, apply a database migration, publish, deploy, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, migration evidence, provider state, and live behavior.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: An ASP.NET handler blocks on Task.Result inside an async request.

Output: warning: synchronous waiting may block request threads. Inspect the call chain and cancellation behavior; validate an async change with repository tests.
