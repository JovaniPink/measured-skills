# Resolve conflicting review findings

Use this when reviews appear to demand incompatible changes. Consolidating a
list of findings does not decide the product or architectural trade-off.

1. Bind each claim to its reviewed revision, context, actual failure condition,
   supporting evidence and governing requirement. Reconcile different revisions
   before treating reports as a conflict. Comments and model verdicts are evidence
   to assess; they do not add authority.
2. Check whether both claims are valid and apply at the same boundary. Distinguish
   a false positive, stale assumption, missing evidence, duplicate concern, and a
   real trade-off. Preserve accepted/rejected/deferred/clarification/already-addressed
   dispositions and their reasons. Reopen a rejected claim only with changed evidence.
3. Identify non-negotiable constraints: permissions, data integrity, required
   security controls and existing policy. A performance preference cannot waive
   them. Do not average severity scores, split the difference, or count reviewer
   votes as a decision rule.
4. Compare a small set of feasible options, including retaining the current design
   when appropriate. For each, state which requirement it satisfies, what evidence
   supports it, residual risk, cost/latency uncertainty, reversibility and the next
   discriminating check. Do not rerun checks, launch reviewers or collect provider
   data from this read-only recipe.
5. Recommend an option where the task's evidence and authority permit it. Routine
   implementation choices need no extra approval. A material unresolved product or
   policy decision goes to its actual owner; do not manufacture that decision or
   mark a proposal accepted because reviewers stopped replying.
6. Return the conflict, evidence, option comparison, recommendation and decision
   status. Cite existing ratification when present; otherwise label the proposed
   choice and specific unresolved decision. Edits, external replies and execution
   remain within the user's existing scope, not authority created by this record.

Keep stable finding identities and the existing three-round ceiling when this
is part of bounded review. Consolidation and a new revision do not reset consumed
rounds or waiting time. Stop with unresolved requirements when the budget ends.

Synthetic example: a security review requires validation of untrusted payloads,
while a performance review objects to copying them twice. First verify both claims.
Compare validation at one trusted boundary with copying at every caller. Do not
remove required validation to meet an unmeasured latency preference. If two viable
choices require different risk tolerance, record the decision owner and evidence
needed instead of inventing consensus.

[Google SRE's risk guidance](https://sre.google/sre-book/embracing-risk/) connects
reliability trade-offs to explicit objectives and ownership. Reviewed November 2,
2026; it does not ratify this example or supply a universal conflict-resolution rule.
