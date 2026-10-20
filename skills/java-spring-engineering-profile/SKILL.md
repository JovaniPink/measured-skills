---
name: java-spring-engineering-profile
description: "Reviews Java and Spring changes when transactions, concurrency, services, dependencies, or JVM compatibility need focused checks; follows repository wrappers and toolchains."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Java and Spring Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when JVM- or Spring-specific gates or hazards determine the result.

## Workflow

1. Discover Maven or Gradle manifests and wrappers, toolchain settings, modules, dependency management, Spring configuration, runtime profiles, and repository scripts.
2. Follow repository-defined wrappers, commands, and pinned Java or framework versions before suggesting defaults.
3. Review material hazards, especially interruption and cancellation loss, unsafe shared state, blocking work, resource lifetime, serialization, reflection, nullability, exception boundaries, and classpath or module-path conflicts.
4. When Spring is present, review dependency-injection cycles, bean scope, configuration precedence, proxy boundaries, transaction demarcation, lazy loading, security configuration, and actuator exposure.
5. Select proportionate gates from repository formatting, static analysis, compilation, tests, integration checks, packaging, dependency review, and builds.
6. Review compatibility across Java release and bytecode targets, modules, build plugins, dependency platforms, Spring Boot generations, native-image assumptions, databases, and deployment packaging.
7. Report every missing tool, skipped command, unsupported runtime, or unavailable service as incomplete rather than passing.

## Boundaries

- Do not replace a repository wrapper with a system Maven or Gradle installation.
- Do not install a JDK, update dependencies, start unapproved services, publish, deploy, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, application startup, provider state, and live behavior.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: A transaction annotation is applied to an internal self-call.

Output: warning: confirm how this call reaches transaction interception in the configured Spring setup. Annotation presence alone does not prove a transaction boundary.
