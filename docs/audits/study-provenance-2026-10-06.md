# Study preparation provenance audit

Observed 2026-10-06 against source
`a155250d65112a18e3d633403c4c99be881be433`.
This is an audit and disposition, not a repin or release decision.

## Current drift evidence

`python3 scripts/check_upstream_freshness.py --online --output REPORT_JSON`
returned 42 matching markers, 13 changed markers, and zero retrieval failures
across 55 sources. The complete public marker readback and OWASP resamples are in
[the audit receipt](study-provenance-2026-10-06.json). Report paths and raw local
inventories are omitted. Markers record a retrieval observation, not page history.

All 13 changed authorities were opened and their relevant guidance compared with
the affected skills and prior review statements. The table records the bounded
current-content readback. Without stored old bodies, it does not establish which
bytes changed or that every difference is cosmetic. No instructions changed.

| Changed authority | Current-content readback and disposition |
| --- | --- |
| [Terraform language](https://developer.hashicorp.com/terraform/language) | Declarative resources and dependencies remain supported. No upgrade or infrastructure-write authority follows. Hold changed marker pending explicit pin review. |
| [Data Agent Kit](https://docs.cloud.google.com/data-agent-kit/overview) | AlloyDB IAM-only database auth, Cloud SQL auth choices, and GitHub Actions orchestration limits remain stated. Keep interface/authority distinctions; hold marker. |
| [Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview) | Sessions and Memory Bank remain distinct components. Product availability does not establish package interoperability; hold marker. |
| [Git merge](https://git-scm.com/docs/git-merge) | Abort may fail to reconstruct preexisting uncommitted changes. Keep clean-state and scope safeguards; hold marker. |
| [Git worktree](https://git-scm.com/docs/git-worktree) | Shared refs and per-worktree state remain distinct. Keep isolation and bounded removal requirements; hold marker. |
| [OpenAI subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Parent permissions/runtime controls matter; max_concurrent_threads_per_session is current with max_threads a legacy alias. Keep effective-configuration checks; hold marker. |
| [Next.js AI agents](https://nextjs.org/docs/app/guides/ai-agents) | Installed-version bundled docs remain the authority; earlier versions differ in bundling and generated AGENTS guidance. Keep installed-version checks; hold marker. |
| [Next.js authentication](https://nextjs.org/docs/app/guides/authentication) | DAL checks near data remain required beyond optimistic Proxy checks. Keep authorization-boundary review; hold marker. |
| [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) | Traces, metrics, logs, and baggage are listed; events/profiles remain under development/proposal on this page. Signal support does not prove instrumentation coverage; hold marker. |
| [Salesforce Apex](https://trailhead.salesforce.com/content/learn/modules/apex_database/apex_database_intro) | Hosted, strongly typed, multitenant-aware behavior and enforced limits remain stated. Local checks do not establish live-org operations; hold marker. |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | The URL now redirects to /projects/asvs; page still identifies 5.0.0 and version-qualified requirements. Three observed markers matched each other but differ from the pin. Retain the hold; do not call it daily volatility. |
| [OWASP agentic initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/) | Agentic Top 10 2026 and related resources remain available. Initial and subsequent normalized markers differed. Retain unstable-source hold. |
| [OWASP LLM08](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) | Access restrictions and leakage risks remain supported. Initial and subsequent normalized markers differed. Retain unstable-source hold. |

The latest scheduled failure was on 2026-10-05 at source
`70182b250beb70bfb210e658387416b891918df1`, before the later source review.
It cannot establish today's changed-source count. A failing drift alarm must be
reviewed, but this audit does not disable it or make a semantic hold a green pin.

## Review-age and originality holds

The pin review date remains 2026-10-05 with a 90-day maximum. The existing strict
`age > maximum` check passes 2027-01-03 and first fails 2027-01-04. Deterministic
regression tests retain that boundary. No broad normalization or date refresh.

The originality checker detects two forms of external skill attribution. Its
passing result does not compare text against an external corpus or establish
comprehensive independent authorship. The historical corpus qualification remains
unresolved. Primary-source research and original fixtures do not close that hold.
Do not download or track third-party skill collections to manufacture a pass;
follow the existing clean-room policy and separately reviewed evidence.

The `v0.16.0` tag exists. The GitHub Release listing returned no entries at this
readback. A candidate manifest, tag, GitHub Release, installed client, and measured
behavior are different facts. No source repin, branch deletion, release, or client
installation was performed for this audit.
