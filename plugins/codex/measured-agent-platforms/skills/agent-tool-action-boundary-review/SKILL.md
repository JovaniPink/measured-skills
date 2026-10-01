---
name: agent-tool-action-boundary-review
description: Review the boundary between an agent and its registered tools or actions, including identity, permissions, schemas, argument controls, network reach, confirmation, idempotency, replay protection, rollback, and audit evidence. Use before an agent can read sensitive data or cause an external effect; use application-security-review for broader application controls.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Agent Tool and Action Boundary Review

Review what an agent can ask a host to do and how deterministic controls constrain the result. Read [the tool action matrix](references/tool-action-matrix.md) when an agent has more than one tool or effect class.

## Preconditions

Identify the agent, product user, service identity, registered tool inventory, data classifications, trust zones, and proposed effects. Obtain tool schemas and host policy from code or authoritative configuration rather than from model-visible prose alone.

## Workflow

1. Inventory every registered tool and action. Record owner, purpose, arguments, outputs, side effects, network destinations, data classes, credentials, and failure behavior.
2. Trace authentication and authorization from the human or system principal through the host to the downstream service. Do not treat the model as an approval authority.
3. Review schema constraints, canonicalization, allowlists, resource identifiers, object ownership, query limits, and server-side validation. Assume arguments can be manipulated.
4. Map read, compute, draft, external write, destructive, financial, publication, deployment, and trust-decision effects.
5. Review SSRF, confused-deputy, data-exfiltration, privilege-escalation, cross-tenant, and indirect prompt-injection paths.
6. For consequential effects, require durable external approval where appropriate, authenticated approvers, binding of approval to exact arguments, expiration, idempotency keys, replay protection, and auditable result readback.
7. Define cancellation, retry, timeout, duplicate delivery, partial failure, rollback, and emergency stop behavior.
8. Test that unregistered tools remain unavailable and that skill text or retrieved content cannot expand the host tool registry or policy.
9. Report findings without enabling, invoking, publishing, deploying, or changing a tool.

## Routing Boundaries

- Use `application-security-review` for conventional authentication, authorization, input handling, and data protection across the application.
- Use `agentic-system-security-review` for the broader model, memory, retrieval, delegation, and supply-chain threat model.
- Use `api-contract-compatibility-review` for producer and consumer compatibility rather than action authority.

## Output

Return `Decision`, `Tool inventory`, `Identity chain`, `Effect classes`, `Argument controls`, `Network and data boundaries`, `Approval and replay controls`, `Failure and recovery`, `Audit evidence`, `Findings`, `Required tests`, and `Authority still needed`.
