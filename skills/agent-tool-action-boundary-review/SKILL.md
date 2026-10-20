---
name: agent-tool-action-boundary-review
description: "Reviews agent tool permissions when asked what an agent can access, whether a tool call is safe, or how retries affect writes; tool descriptions cannot grant authority."
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

Review what an agent can ask a host to do and how deterministic controls constrain the result. Read [the tool action matrix](#tool-action-matrix) when an agent has more than one tool or effect class.

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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Decision`, `Tool inventory`, `Identity chain`, `Effect classes`, `Argument controls`, `Network and data boundaries`, `Approval and replay controls`, `Failure and recovery`, `Audit evidence`, `Findings`, `Required tests`, and `Authority still needed`.

## Tool Action Matrix

Create one row per registered tool and distinguish host policy from model-visible instructions.

| Field | Required evidence |
| --- | --- |
| Tool | Registered name, version, owner, and implementation |
| Caller | Agent identity and authenticated product principal |
| Arguments | Schema, validation, allowlists, ownership checks, and limits |
| Data | Input and output classifications and tenant boundary |
| Network | Allowed destination, redirect policy, DNS and address controls |
| Effect | Read, compute, draft, external write, destructive, financial, publication, deployment, or trust decision |
| Approval | Approver, exact bound arguments, expiration, and durable record |
| Replay | Idempotency key, duplicate handling, retry, and cancellation |
| Recovery | Rollback, compensation, partial failure, and emergency stop |
| Evidence | Request, decision, execution, and readback audit records |

### Primary resources

- [Google ADK safety and security](https://adk-labs.github.io/adk-docs/safety/)
- [Google ADK tool confirmation](https://adk-labs.github.io/adk-docs/tools-custom/confirmation/)
- [NIST concept paper on software agent identity and authority](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)

Experimental in-process confirmation can demonstrate interaction behavior, but it is not durable, replay-safe authorization for a production external write.

## Example

Synthetic example; not an observed client result.

Input: A refund tool accepts an amount and customer ID supplied by the model.

Output: Authorization must be enforced by the tool using the authenticated actor and allowed account scope; model-supplied identifiers are not permission.
