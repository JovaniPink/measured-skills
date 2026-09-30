---
name: agent-protocol-interoperability-review
description: Review interoperability across agent, tool, and service protocols using exact versions, discovery records, schemas, identity, authorization, delegation, streaming, errors, retries, idempotency, cancellation, and trust zones. Use for A2A, MCP, or another agent-facing protocol boundary; use api-contract-compatibility-review for an ordinary API change without agent delegation semantics.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Agent Protocol Interoperability Review

Review whether independently operated agent components can communicate without losing identity, authority, compatibility, or failure semantics. Read [the protocol boundaries reference](references/protocol-boundaries.md) when comparing two or more protocol surfaces.

## Preconditions

Identify the protocols, exact versions, roles, owners, trust zones, transports, discovery mechanisms, authentication, authorization, and decision under review. Obtain schemas and security requirements from current primary specifications and implementation evidence.

## Workflow

1. Map each participant as client, server, agent, tool host, remote agent, gateway, or application. Record which party controls discovery and trust.
2. Pin protocol and implementation versions. Distinguish required specification behavior, optional behavior, extensions, implementation-specific behavior, and normative schemas from rendered or generated convenience artifacts.
3. Trace discovery documents, signature verification, caching and refresh, capability advertisement, schema negotiation, protocol binding selection, content types, task or request identifiers, streaming, artifacts, errors, cancellation, and completion.
4. Trace end-user identity, service identity, delegated authority, credentials, consent, and tenant context across every hop. Reject ambient or silently expanded authority.
5. Review argument and output validation, content injection, URL fetching, redirects, SSRF, data exfiltration, and unsafe rendering.
6. Define retries, timeouts, duplicate delivery, idempotency, ordering, partial results, recovery, and revocation.
7. Test supported version and binding pairs, functional equivalence, downgrade or mismatch behavior, breaking migrations, malicious or stale discovery data, invalid schemas, lost cancellation, duplicate actions, and unauthorized capability claims. An authorization-required state is a request for authorization, not authorization by itself.
8. Report compatibility as observed for the exact combination. Do not create connectivity, credentials, infrastructure, or deployment by implication.

## Routing Boundaries

- Use `api-contract-compatibility-review` for ordinary API, event, or schema compatibility.
- Use `agent-tool-action-boundary-review` when the core question is whether a local tool action is authorized.
- Use `agentic-system-security-review` for the full agent threat model.

## Output

Return `Decision`, `Participants and trust zones`, `Exact versions`, `Discovery and capabilities`, `Schemas and content`, `Identity and delegated authority`, `Lifecycle and streaming`, `Failure semantics`, `Security findings`, `Observed compatibility`, `Unknowns`, and `Required tests`.
