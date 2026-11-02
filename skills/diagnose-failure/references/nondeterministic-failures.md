# Diagnose an intermittent failure

Use this procedure when the same check sometimes passes or depends on test order,
parallel execution, timing, or shared state. A flaky test is a symptom, not a cause.

1. Retain the first failure, revision, command, input, seed, test order, worker
   count, environment, and complete error. Record unknowns. Check whether repeated
   runs actually used the same inputs; dependency or configuration drift can explain
   different outcomes without a race.
2. Define competing explanations: leaked state or incomplete cleanup; task lifetime
   or a missing synchronization boundary; wall-clock/timer dependence; random input;
   resource contention; or an external service. A passing isolated run does not
   eliminate any of these by itself.
3. Set a bounded local investigation before repetition. Default to at most ten
   executions or five minutes of execution time, whichever ends first, within the
   task's authorized scope. Count attempts across interruptions. Preserve each
   outcome; do not repeat until green. Stop at uncertainty about provider spending,
   shared-state mutation, data exposure, or permitted execution. Use supplied traces
   when running the reproduction is unavailable or unsafe.
4. Change one discriminating condition at a time: isolation versus the suite,
   serial versus parallel, a recorded order/seed, or controlled scheduling. Replace
   arbitrary sleeps with an observed synchronization condition when designing a
   repair. Use a controlled clock only where the contract permits it; do not hide
   real ordering, cancellation, or timestamp semantics through normalization.
5. Trace the earliest divergence. Connect ownership, cleanup, scheduling and the
   assertion to the failure. Report supporting and disconfirming observations.
   Diagnose a product defect, test defect, environment dependency, or unresolved
   cause; several may coexist.
6. Propose the smallest repair and a regression that distinguishes it from the
   failing baseline. Diagnosis alone does not authorize edits, quarantine, retries
   in CI, weaker assertions, or publishing. If repair is already authorized, retain
   the failure evidence and compare the same conditions before and after the fix.
7. Report attempts used, conditions covered, causal evidence, and uncovered paths.
   Finite successful repetitions cannot prove that a race is absent. If quarantine
   is separately authorized, record the owner, reason, expiry/review date, coverage
   loss and repair task; it remains unfinished work rather than a passing check.

Synthetic example: a cache test passes alone but fails after an authentication
case. Replaying the recorded order exposes a shared cache key; isolating that state
is a useful experiment. Increasing retries would mask the interaction without
explaining it. A thread race remains unproven unless scheduling evidence supports it.

The [pytest flaky-test guide](https://docs.pytest.org/en/stable/explanation/flaky.html)
discusses state, ordering, threads and rerun/quarantine limitations. Reviewed
November 2, 2026. Discover the actual framework before choosing commands. The
attempt/time ceiling above is a workflow default, not a research-derived optimum.
