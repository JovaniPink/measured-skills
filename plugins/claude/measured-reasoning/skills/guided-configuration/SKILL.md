---
name: guided-configuration
description: "Guide a person through configuration steps that require their account, device, approval, credential, or external interface while verifying each observable result. Invoke explicitly when the agent cannot or should not perform the protected step itself."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
disable-model-invocation: true
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

During a step, return `Current step`, `Expected result`, and relevant `Recovery` or `Security boundary`. At a checkpoint or completion, lead with the observed result and anything the user must do next. Then reconcile `Goal`, `Authoritative source`, `Observed result`, `Changes applied`, and `Remaining steps`, preserving failed and unverified work. `Changes applied` lists every configuration change made, including reversed ones.

## Continuity and evidence

During configuration, present the current human step, expected result, and relevant recovery or security boundary. Keep the complete state reconciliation for a checkpoint or final response. Preserve failed and unverified steps, and reuse observed completion when it remains current.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
