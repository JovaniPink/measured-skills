---
name: design-agent-memory
description: "Designs agent context and memory boundaries when asked where session state belongs, how memory expires, or how tenants stay isolated; distinguishes architecture from a context-packet audit."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Agent Context, State, and Memory Design

Design the information lifecycle an agent can observe and retain. Read [the state and memory lifecycle reference](#state-and-memory-lifecycle) when mapping scopes, authority, retention, or poisoning controls.

## Preconditions

Identify the user population, tenant model, agent identities, session boundary, data authorities, privacy obligations, persistence services, and decision the design must support. Mark proposed stores and policies as proposed.

## Workflow

1. Inventory prompt instructions, conversation or event history, request context, session state, user state, application state, long-term memory, retrieved knowledge, tool results, and artifacts.
2. For each item, record the authoritative source, subject identity, tenant, writer, reader, purpose, effective time, freshness rule, retention, deletion path, and audit evidence.
3. Distinguish durable product truth from convenience memory. A summary, embedding, model inference, or repeated statement is not automatically authoritative.
4. Trace write paths, conflict resolution, supersession, revocation, compaction, and readback. Identify where stale or poisoned material could remain influential.
5. Test isolation across requests, sessions, users, tenants, agents, and evaluation cases. Include attempted cross-scope reads and writes.
6. Review sensitive-data minimization, access control, encryption boundaries, export, deletion, legal retention, and incident response.
7. Define how untrusted user input, retrieved content, tool responses, and prior agent output are labeled and prevented from becoming higher-authority instructions.
8. Separate design review from migration, deletion, data access, or production configuration. Those actions require separate authority.

## Routing Boundaries

- Use `review-context-evidence` to assess the reliability of assertions already supplied to a model.
- Use `review-data-authority` to map system-of-record writers, readers, and projections beyond agent memory.
- Use `review-retrieval-grounding` for corpus, retrieval, and evidence-support quality.
- Use `review-agent-security` for the system-wide threat model.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Decision`, `Information classes`, `Scope and identity`, `Authority and provenance`, `Write and read paths`, `Freshness and retention`, `Isolation`, `Poisoning controls`, `Privacy and deletion`, `Confirmed evidence`, `Proposals`, `Gaps`, and `Required tests`.

## State and Memory Lifecycle

Use one row per material information class.

| Field | Question |
| --- | --- |
| Class | Is this instruction, request context, event history, scoped state, memory, retrieval, tool output, or artifact? |
| Subject | Which user, tenant, case, agent, or system does it concern? |
| Authority | What store or decision owner can establish or change it? |
| Provenance | Where did it come from, and can that origin be verified? |
| Writer | Which authenticated principal may create or update it? |
| Reader | Which principal may observe it, and for what purpose? |
| Time | When was it effective, observed, recorded, and last checked? |
| Retention | How long does it remain, and what rule governs deletion? |
| Conflict | What happens when sources disagree? |
| Revocation | How is it made ineligible and removed from future context? |
| Isolation | Which request, session, user, tenant, and evaluation boundaries apply? |

### Primary resources

- [Google ADK sessions and state](https://adk-labs.github.io/adk-docs/sessions/)
- [Google ADK memory](https://adk-labs.github.io/adk-docs/sessions/memory/)
- [NIST concept paper on software agent identity and authority](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)

Treat framework namespaces as mechanisms. Product authority and privacy requirements must still be defined by the owning application.

## Example

Synthetic example; not an observed client result.

Input: Two tenants share one agent memory key.

Output: warning: the key does not distinguish tenants. Scope storage and retrieval by authorized tenant identity; existing isolation is not established.
