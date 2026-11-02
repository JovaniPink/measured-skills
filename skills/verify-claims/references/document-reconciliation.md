# Compare documents with implementation

Select the documents and the behavior being checked; do not scan every historical
note as if it were a current requirement. Record repository/base/head, relevant
uncommitted inputs, document identity, and status: current contract, proposal,
superseded, or historical. Resolve conflicting authority before declaring drift.

For each material claim, connect the requirement to source symbols, callers,
tests, and any supplied execution evidence. A test's existence, its execution,
and its result are different facts. Static correspondence cannot prove a runtime
journey. This is a reasoned review, not an AST or deterministic architecture scanner.

Classify the discrepancy and recommend the correct next action:

| Discrepancy | Evidence and next decision |
| --- | --- |
| Missing implementation | Current accepted behavior has no supported implementation in the inspected scope; propose the repair. |
| Stale document | Authoritative decisions changed, but current guidance did not; identify the supporting decision before editing. |
| Intentional deviation | Identify who accepted it and which conditions changed; an agent summary alone is insufficient. |
| Ambiguous requirement | State the conflicting interpretations and the decision needed. |
| Unavailable evidence | Name what was not inspected or run; do not infer a pass or absence. |

Current code is not automatically correct. Never rewrite requirements merely to
match it. Keep useful historical observations intact and label them appropriately.
Return a concise claim-to-evidence record, the discrepancy, and a proposed
correction. Editing code or documents requires authority already present in the
task; this read-only review does not create that authority or withdraw an existing
grant.

Synthetic example: a current runbook promises retries preserve a request ID, but
a retry path creates a new one. The review traces the call and tests, then asks
whether the contract or implementation should change. It does not silently weaken
the runbook to make the mismatch disappear.
