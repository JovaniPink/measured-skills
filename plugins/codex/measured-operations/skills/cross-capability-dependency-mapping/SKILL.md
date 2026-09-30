---
name: cross-capability-dependency-mapping
description: Map dependencies across products, teams, data, platforms, decisions, and operating capabilities. Use when delivery or outcomes depend on multiple owners and hidden sequencing, authority, or failure paths must be made explicit.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Cross-Capability Dependency Mapping

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Define the outcome and capability boundary being mapped.
2. Inventory capabilities, owners, inputs, outputs, contracts, data authority, platforms, and decision rights.
3. Classify dependencies as data, technical, process, policy, people, funding, vendor, or decision dependencies.
4. Record direction, criticality, lead time, confidence, failure effect, fallback, and evidence.
5. Identify cycles, single points of failure, shared bottlenecks, contested ownership, and unratified contracts.
6. Build a critical path and identify which dependencies can proceed in parallel.
7. Assign validation, escalation, and change-notification obligations to named owners.

## Boundaries

- Do not infer ownership from who last edited or operates a downstream copy.
- Do not publish private topology, identity, or contractual details in a public artifact.
- Do not treat a dependency map as authority to change another owner's system.

## Output

Return Capability map, Dependency register, Critical path, Ownership gaps, Failure paths, Parallel work, and Decisions needed.
