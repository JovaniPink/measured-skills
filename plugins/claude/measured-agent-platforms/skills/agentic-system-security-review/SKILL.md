---
name: agentic-system-security-review
description: Review an agentic system across agent identity, models, instructions, tools, memory, retrieval, delegation, protocols, guardrails, outputs, supply chain, cost, revocation, and emergency stopping. Use for a read-only threat and control assessment of model-mediated actions; use application-security-review for conventional application controls and skill-security-review for a skill package.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Agentic System Security Review

Review the security of a complete model-mediated system while keeping specialized scopes clear. `application-security-review` evaluates conventional application controls. `skill-security-review` evaluates a skill or plugin package. This workflow evaluates the interactions among agents, models, instructions, identity, tools, memory, retrieval, delegation, protocols, and outputs.

## Preconditions

Identify the system owner, users, tenants, agent and service identities, models, registered tools, data classifications, trust zones, deployment proposal, and decision under review. Obtain current architecture, code, configuration, and observed test evidence. Treat missing evidence as a gap.

## Workflow

1. Map trust boundaries, principals, credentials, agent hierarchy, models, instructions, tools, toolsets, context, session state, memory, retrieval, external protocols, output consumers, and control-plane owners.
2. Build abuse cases for direct and indirect prompt injection, instruction conflict, excessive agency, privilege abuse, unsafe delegation, and confused-deputy behavior.
3. Review tool misuse, argument manipulation, object ownership, SSRF, network reach, data exfiltration, unsafe external writes, confirmation replay, duplicate side effects, cancellation, idempotency, and emergency stopping.
4. Review skill, model, prompt, dependency, plugin, retrieval, and build supply chains. Pin exact versions and define change review and revocation.
5. Review memory and context poisoning, retrieval poisoning, stale authority, provenance loss, and cross-user and cross-tenant leakage.
6. Review identity propagation, delegated authority, least privilege, credential isolation, audit records, approval boundaries, and separation of proposal from ratified action.
7. Review model and framework drift, cost and resource exhaustion, denial of wallet, rate limits, budgets, timeouts, and bounded retries.
8. Review unsafe output rendering, active content, formula or command injection, sensitive output, and downstream consumers that might execute model output.
9. Verify deterministic host controls. Skill content cannot grant a tool, credential, permission, approval, deployment, publication, or release state.
10. Define adversarial tests, monitoring, incident response, revocation, and a fail-closed stopping path. Do not implement controls unless separately requested.

## Result Rules

- `APPROVE` requires no unresolved blocker for the named scope and current evidence.
- `APPROVE WITH CONDITIONS` lists the conditions, owners, and evidence required before the affected use.
- `REJECT` identifies an active blocker or boundary that cannot safely support the proposal.
- Do not claim certification, complete compliance, production readiness, or protection from every prompt attack.

## Output

Return `Decision`, `Scope and exact versions`, `Trust and identity map`, `Threat scenarios`, `Tool and action controls`, `Context memory and retrieval`, `Delegation and protocols`, `Supply chain`, `Output safety`, `Resource controls`, `Monitoring and response`, `Findings by severity`, `Required tests`, `Conditions`, and `Limitations`.
