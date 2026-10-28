---
name: agent-protocol-interoperability-review
description: "Reviews MCP, A2A, and agent protocol integration when tools fail discovery or delegation, streaming, retries, or cancellation cross services; ordinary API changes use API compatibility review."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Agent Protocol Interoperability Review

Review whether independently operated agent components can communicate without losing identity, authority, compatibility, or failure semantics. Read [the protocol boundaries reference](#protocol-boundaries) when comparing two or more protocol surfaces.

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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Decision`, `Participants and trust zones`, `Exact versions`, `Discovery and capabilities`, `Schemas and content`, `Identity and delegated authority`, `Lifecycle and streaming`, `Failure semantics`, `Security findings`, `Observed compatibility`, `Unknowns`, and `Required tests`.

## Protocol Boundaries

Record each protocol hop separately.

| Boundary | Questions |
| --- | --- |
| Version | Which specification and implementation versions are in use? |
| Normative source | Which versioned schema is authoritative, and which rendered or generated artifacts are only projections? |
| Discovery | Who publishes capabilities, how is the record signed or authenticated, and how are caches refreshed or revoked? |
| Binding | Do each advertised transport and protocol binding preserve operations, results, errors, and authentication? |
| Identity | Which user, service, agent, and tenant identities cross the boundary? |
| Authority | What is delegated, for how long, and how is scope enforced? Does an authorization-required state remain only a request until an external decision grants a defined scope? |
| Schema | How are inputs, outputs, extensions, and content types validated? |
| Lifecycle | How are tasks, requests, streams, artifacts, cancellation, and completion represented? |
| Failure | What happens on timeout, retry, duplication, partial delivery, or version mismatch? |
| Security | Can untrusted content influence tools, URLs, credentials, rendering, or another agent? |
| Revocation | How are credentials, capabilities, tasks, and compromised endpoints disabled? |

### Primary resources

- [A2A Protocol specification 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest)
- [Google ADK A2A documentation](https://adk-labs.github.io/adk-docs/a2a/)

Protocol support is not interoperability proof. Record the exact implementation pair and the tests that were observed.

## Example

Synthetic example; not an observed client result.

Input: The client retries a delegated task after losing the response.

Output: The retry contract is unresolved: inspect task identity and duplicate handling at both ends before calling retries safe.
