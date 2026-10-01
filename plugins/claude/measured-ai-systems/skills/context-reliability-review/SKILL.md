---
name: context-reliability-review
description: Review the reliability of context assertions supplied to an AI system by tracing provenance, authority, freshness, effective and recorded time, permissions, conflicts, supersession, and revocation. Use when agent behavior depends on whether contextual claims are current and allowed; use authority-boundary-review for system-of-record architecture rather than assertion-level context.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-ai-systems"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Context Reliability Review

Evaluate context as a set of assertions with evidence and lifecycle, not as an undifferentiated prompt. Read [the assertion matrix reference](references/assertion-matrix.md) when assertions conflict or change over time.

## Preconditions

Identify the decision or behavior that consumes the context, the reviewed context boundary, the observation time, and the permitted evidence sources. Use synthetic placeholders in public output; do not reproduce private facts merely to make the matrix complete.

## Workflow

1. Decompose the context into atomic assertions. Separate observed facts, policies, permissions, preferences, inferences, instructions, and proposed state.
2. Record each assertion's provenance: source identity, citation or receipt, author or issuer, collection method, and transformation history.
3. Identify the authority for the assertion and the scope in which that authority applies. Distinguish an authoritative source from a convenient copy or summary.
4. Record effective time and recorded time separately. Add observation time, expiration, and the freshness rule required by the consuming decision.
5. Record subject, audience, environment, purpose, and permissions. An accurate assertion may still be unusable outside its authorized scope.
6. Find conflicts, missing qualifiers, ambiguous vocabulary, and assertions whose evidence cannot be recovered. Do not resolve a conflict by recency alone unless that rule is ratified.
7. Trace supersession and revocation. Identify the replacement, invalidation event, propagation path, caches, and consumers that may retain stale context.
8. Assess the effect of each unreliable assertion on routing, tool choice, output claims, safety, and user decisions.
9. Assign a status of `RELIABLE`, `QUALIFIED`, `STALE`, `CONFLICTED`, `REVOKED`, or `UNVERIFIED`, with the evidence that justifies it.
10. Recommend the smallest correction: refresh, qualify, remove, reconcile, restrict, or request a decision from the authority owner.

## Routing Boundaries

- Use `authority-boundary-review` for stores, writers, readers, projections, and reconciliation across a system architecture.
- Use `decision-evidence-trace` for a durable decision log rather than a context assertion audit.
- Use `public-private-boundary-review` before publishing context or examples.
- A product-specific model review belongs to its product catalog unless the question concerns assertion provenance and lifecycle.

## Output

Return `Review scope`, an assertion matrix with `ID`, `Assertion`, `Type`, `Source`, `Authority`, `Effective time`, `Recorded time`, `Observed time`, `Freshness rule`, `Permissions`, `Conflict or supersession`, `Status`, and `Impact`, followed by `Corrections`, `Private-output boundary`, and `Unresolved authority decisions`.
