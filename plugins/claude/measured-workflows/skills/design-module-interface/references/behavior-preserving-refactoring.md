# Restructure while preserving observed behavior

[Refactoring changes internal structure while preserving observable behavior](https://martinfowler.com/bliki/DefinitionOfRefactoring.html).
Reviewed 2026-10-28. This definition does not imply that finite tests establish
universal equivalence or that every existing behavior is desirable.

1. Bound the seam, callers, supported inputs, and reason for restructuring. Identify
   observable outputs, errors, serialization, ordering, side effects, and timing
   only where timing is part of a contract. Separate intentional behavior changes.
2. Establish a baseline before moving code. Use existing tests plus focused
   characterization cases where behavior is undocumented. Capture realistic edge
   cases with synthetic or approved data, not private production snapshots.
3. Explain each oracle. Golden snapshots can preserve defects as well as useful
   behavior. Normalize only understood nondeterminism; never discard ordering,
   timestamps, IDs, or errors merely to obtain a green comparison.
4. Extract one seam, preserve callers, and compare the same inputs before and after.
   A structural refactor need not begin with an artificially failing behavior test.
   When fixing a known defect too, isolate that behavioral decision and regression.
5. Review affected callers and surrounding state ownership, not only moved lines.
   A process boundary, persistence change, or Strangler-style traffic cutover has
   additional distributed-state, compatibility, rollout, and recovery requirements.
6. Report preserved observations and uncovered behavior. Passing snapshots or unit
   tests do not establish all integrations, performance, or deployed behavior.

Planning remains read-only. An authorized implementation uses small reversible
slices; do not broadly refresh snapshots, run unreviewed codemods, or introduce a
new abstraction merely because the workflow is called refactoring.

Synthetic example: extract tax rounding from a checkout module while retaining
currency precision, negative adjustments, and serialized errors. Characterize
those outputs before extraction. If a legacy rounding bug is discovered, record
it separately instead of silently treating its correction as behavior preservation.
