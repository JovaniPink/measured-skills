---
name: request-code-review
description: "Prepares a review packet when explicitly asked to request review of a change; states scope, tests, and risks, and sends it only when the destination and action are authorized."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "original"
  risk_class: "external-write"
disable-model-invocation: true
---

# Request Code Review

Give reviewers a precise packet that separates proposed code from checks, decisions, deployment, and merge authority. `publish-change-safely` owns the commit, the push, and the pull request record. This workflow owns the reviewer-facing content and its authorized delivery. When a request also asks to publish the change, route the commit and push to `publish-change-safely` and keep the packet here.

## Workflow

1. Verify repository identity, base and head branches, exact revision, diff scope, and unrelated changes.
2. Summarize the problem, chosen approach, user-visible or contract impact, and excluded work.
3. Record checks by exact command and result. Name tests or environments that were not run.
4. Identify security, data, compatibility, migration, operational, and rollback risks.
5. Provide a short review focus with concrete questions and high-risk files or paths.
6. Confirm whether the user authorized only preparing the packet or also sending it through a named external channel.
7. After an authorized send, read back the created request, URL, revision, reviewer state, and checks.

## Boundaries

- Explicit invocation does not by itself authorize push, PR creation, reviewer assignment, external messaging, merge, or deployment.
- Do not describe a check as passing from stale output or a different revision.
- A review request is proposed work, not approval or merge authority.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Scope`, `Approach`, `Evidence`, `Risks`, `Not tested`, `Review focus`, `Authority`, and, if sent, `External readback`.

## Example

Synthetic example; not an observed client result.

Input: Prepare a review request for a tested patch; sending it is not authorized.

Output: The packet states the patch scope, revision, tests, and open risks. It is prepared locally and has not been sent.
