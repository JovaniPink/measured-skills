# Focused checks

Primary documentation: [official Spring Boot documentation](https://docs.spring.io/spring-boot/). Use the repository's selected Java release as the version authority; consult the [official JDK documentation](https://docs.oracle.com/en/java/) for language and runtime behavior.

## Discovery

Inspect `pom.xml`, Gradle settings and build files, wrappers, toolchain configuration, module descriptors, dependency platforms, Spring configuration, application profiles, container definitions, and CI scripts. Resolve multi-module ownership, generated sources, annotation processors, and test fixtures before selecting gates.

## Judgment focus

Review interruption and cancellation, synchronization and shared state, virtual-thread or reactive blocking, resource cleanup, serialization, reflection, exception boundaries, nullability, dependency-injection cycles and scopes, configuration precedence, proxies, transactions, lazy loading, security rules, and management endpoints.

## Gate families

Consider repository wrapper tasks for formatting, static analysis, compilation, unit and integration tests, packaging, dependency review, and reproducible builds. Starting shared services, changing dependencies, publishing artifacts, and deploying remain separately authorized.

## Compatibility

Check Java release and bytecode targets, module boundaries, build plugins, dependency platforms, Spring Boot generation, native-image assumptions, database drivers, test runtime, packaging, and deprecations. Record unavailable tools and environments explicitly; never manufacture a passing result.
