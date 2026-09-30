---
name: swift-concurrency-diagnosis
description: Diagnose Swift actor isolation, Sendable diagnostics, task lifetime, cancellation, or reentrancy using actual compiler settings. Read-only; do not trigger for formatting, ordinary synchronous logic, or implementation without a concurrency question.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-swift-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Swift Concurrency Diagnosis

Read [isolation and task diagnosis](references/isolation.md) only when its checks apply to the task. Project-local copies include a project contract; compare it with current repository settings before relying on it.

## Workflow

1. Locate the affected module, exact diagnostic or reproducible symptom, toolchain, language mode, strict checking, default isolation, and upcoming features.
2. Trace the actor and task ownership graph through the failing boundary. Read the concurrency reference only for the relevant executor, transfer, cancellation, or reentrancy question.
3. Distinguish structured children, unstructured tasks, and detached tasks. Check state across suspension points, cancellation propagation, late publication, and callback completion ownership.
4. Propose the smallest correction justified by diagnostics and ownership. Trust compiler transfer analysis; do not propose @unchecked Sendable merely to suppress a diagnostic.
5. Report settings, exact evidence, root-cause hypothesis, proposed correction, and the narrow compiler/test command. Return Not Needed when no concurrency boundary exists; do not edit files.

## Boundaries

Async does not imply background execution. Do not prescribe blanket MainActor.run removal, detached tasks, or unchecked conformance. An unavailable diagnostic is missing evidence, not a proven race.

## Evidence and output

Report the authorized scope, applicable settings, observed evidence, result, missing evidence, and next bounded check. Use Not Needed when no applicable authorized work exists and Blocked when a required precondition is missing. Do not substitute required headings for semantic compliance or invent executed checks.
