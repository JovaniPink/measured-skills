---
name: guide-configuration
description: "Guides account or device setup when explicitly asked to help with a protected configuration step; verifies visible results without requesting secrets or claiming unseen completion."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Guided Configuration

Help a person complete protected configuration without pretending the agent performed or verified inaccessible work.

## Workflow

1. Confirm the desired outcome, authoritative product documentation, current state, target account or environment, and actions the user permits. Confirm the target by its identifier, not only its display name, because similar names can point to different accounts or environments.
2. Separate steps the agent can verify from steps only the user can perform or observe.
3. Present one material step at a time with its purpose, expected visible result, and safe recovery path.
4. Ask the user to perform protected authentication, approval, credential, billing, device, or administrative actions themselves.
5. After each step, verify the result through authorized readback or ask for the smallest non-sensitive observation needed.
6. Stop on an unexpected account, environment, permission request, destructive effect, cost, or security warning.
7. Summarize completed, unverified, failed, and reversed steps without claiming inaccessible success.

## Boundaries

- Never ask the user to paste secrets, recovery codes, private keys, or full tokens into chat.
- Do not generate commands that broaden privileges beyond the stated need.
- Do not bypass security prompts or describe a warning as harmless without evidence.
- Configuration does not authorize publication, deployment, billing, or data migration unless those actions were separately approved.

## Output

During a step, state the current human action, expected result, and relevant
recovery or security boundary. Reuse observed completion while it remains current.
At a checkpoint, lead with the observed result and anything the user must do
next; reconcile the goal, authoritative source, results, changes, and remaining
steps. List every reported or observed configuration change, including reversed
ones, and identify which were observed. Failed and unverified steps remain visible.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: The account is selected, but the permission screen is still pending.

Output: Complete the permission step in the account interface and verify its result. Account selection alone does not establish access.
