---
name: agent-context-state-memory-design
description: Design or review how an agent separates prompt context, session events, scoped state, long-term memory, and artifacts. Use when identity, authority, freshness, retention, provenance, tenant isolation, poisoning, or deletion behavior could change what an agent knows or does; use context-reliability-review for a supplied context packet rather than the hosting architecture.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Agent Context, State, and Memory Design

Design the information lifecycle an agent can observe and retain. Read [the state and memory lifecycle reference](references/state-memory-lifecycle.md) when mapping scopes, authority, retention, or poisoning controls.

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

- Use `context-reliability-review` to assess the reliability of assertions already supplied to a model.
- Use `authority-boundary-review` to map system-of-record writers, readers, and projections beyond agent memory.
- Use `retrieval-grounding-quality-review` for corpus, retrieval, and evidence-support quality.
- Use `agentic-system-security-review` for the system-wide threat model.

## Output

Return `Decision`, `Information classes`, `Scope and identity`, `Authority and provenance`, `Write and read paths`, `Freshness and retention`, `Isolation`, `Poisoning controls`, `Privacy and deletion`, `Confirmed evidence`, `Proposals`, `Gaps`, and `Required tests`.
