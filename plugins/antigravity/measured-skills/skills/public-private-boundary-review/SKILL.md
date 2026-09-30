---
name: public-private-boundary-review
description: Review code, documentation, examples, articles, or release artifacts before public exposure to find secrets, internal identifiers, private operational details, proprietary material, and claims unsupported by public evidence. Use before open-sourcing or publishing work derived from mixed public and private contexts.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Public-Private Boundary Review

Review both content and provenance. Renaming an internal identifier does not make proprietary logic, data, or operational knowledge public.

## Workflow

1. Define the intended public artifact, audience, license, and source repositories.
2. Inventory copied, adapted, generated, and independently authored material.
3. Check license and authorization for every non-original source. Treat absent permission as a blocker, not an invitation to sanitize.
4. Scan content and history in scope for:
   - credentials, tokens, keys, cookies, connection strings, and personal data
   - private repository URLs, absolute local paths, account IDs, project IDs, hostnames, emails, and internal ticket references
   - client names, proprietary schemas, business rules, architecture contracts, incidents, logs, screenshots, and production configuration
   - claims that confuse repository code with testing, deployment, availability, or outcomes
5. Replace only ordinary incidental identifiers. For proprietary substance, remove it and independently author from public sources or keep it in a private overlay.
6. Re-run tests and documentation checks after redaction so safety edits do not leave broken artifacts.
7. Report blockers, safe-to-publish items, and facts requiring owner or counsel confirmation.

## Output

Use `BLOCK`, `REVIEW`, or `CLEAR` per finding, with location, risk, evidence, and disposition. A `CLEAR` verdict means no issue was found in the reviewed scope; it is not a legal opinion or proof that unreviewed history is safe.
