---
name: review-context-evidence
description: "Checks supplied agent context when asked whether a claim is stale, conflicting, authorized, or superseded; traces assertion provenance rather than redesigning the system of record."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Context Reliability Review

Evaluate context as a set of assertions with evidence and lifecycle, not as an undifferentiated prompt. Read [the assertion matrix reference](#assertion-matrix-reference) when assertions conflict or change over time.

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

- Use `review-data-authority` for stores, writers, readers, projections, and reconciliation across a system architecture.
- Use `trace-decisions` for a durable decision log rather than a context assertion audit.
- Use `review-public-boundary` before publishing context or examples.
- A product-specific model review belongs to its product catalog unless the question concerns assertion provenance and lifecycle.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Review scope`, an assertion matrix with `ID`, `Assertion`, `Type`, `Source`, `Authority`, `Effective time`, `Recorded time`, `Observed time`, `Freshness rule`, `Permissions`, `Conflict or supersession`, `Status`, and `Impact`, followed by `Corrections`, `Private-output boundary`, and `Unresolved authority decisions`.

## Assertion Matrix Reference

Use this reference for assertion-level context audits. The model follows provenance relationships described by [W3C PROV](https://www.w3.org/TR/prov-n/) while keeping the review language and status model specific to this catalog.

### Assertion Anatomy

An assertion is a claim used by the consuming agent or workflow. Record:

- the entity or subject the assertion describes;
- the source entity and the activity that collected or transformed it;
- the responsible issuer or authority;
- effective time, recorded time, observation time, and expiration;
- the permitted audience, purpose, environment, and actions;
- derivation, conflict, supersession, and revocation links;
- the behavior or decision affected when the assertion is wrong or unavailable.

### Status Rules

| Status | Meaning |
| --- | --- |
| `RELIABLE` | Current evidence supports the assertion within its authority and permission scope. |
| `QUALIFIED` | The assertion is usable only with an explicit limitation or narrower scope. |
| `STALE` | Its freshness rule is violated or currentness cannot be established. |
| `CONFLICTED` | Relevant sources disagree and no ratified resolution rule settles the conflict. |
| `REVOKED` | An authorized event invalidated the assertion for the reviewed use. |
| `UNVERIFIED` | The source, authority, or supporting evidence cannot be established. |

### Time Discipline

Effective time answers when the assertion was true in the modeled world. Recorded time answers when a system captured it. Observation time answers when the reviewer inspected it. Never substitute one for another. A later recording can describe an earlier effective fact, and a recently observed cache can still contain revoked context.

## Example

Synthetic example; not an observed client result.

Input: A context note says access is allowed, but a newer policy revokes it.

Output: The newer authoritative policy supersedes the note. Mark the access assertion stale and do not use it to authorize a request.
