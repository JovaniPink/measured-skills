# November 2 receiving-client preflight and stopped retest

This is an owner observation, not independent grading or general client acceptance.
Skill source: reviewed draft revision `d85c7b5947adfe3f4e4c2a9fec9068559b975c3e`.
The original October 29 Haiku outputs and both earlier preparations are preserved.

## Controls and observed execution

Matching CLI/browser organization identities were observed for the selected
receiving account. The CLI reported first-party Pro authentication. Usage credits
and auto-reload were off in the matching browser before the task and remained off
afterward. No billing toggle or account switch was performed. Private identities,
balances and raw authentication/session records are omitted here.

The user explicitly authorized folder trust, the changed CLI-version comparison,
and one Haiku task session plus one continuation, at most ten minutes each, with
no replacement attempts. Native preflight on Claude Code 2.1.312 showed Haiku 5.5
low effort, exactly nine staged skills, command-line settings only, no MCP servers,
no ambient memory-file category, disabled hooks, and restricted/manual permissions.
These observations did not establish that every required file was readable.

Exactly one task request was submitted. The owner stopped it after a required
reference failure and canceled the pending edits. No continuation or replacement
ran. All 51 frozen input files matched afterward; no workspace file was created.
The trace contains 14 unique tool request IDs: one Skill, one Glob, ten Read and
two Edit requests. Deduplicated IDs prevent counting repeated transcript entries
as new actions. Tool requests are not model-inference-call or billing counts.

| Observation | Result and limit |
| --- | --- |
| Selected skill | Skill tool reported successful loading; this does not establish implicit activation or native-parser routing |
| Workspace instructions and evidence index | Read successfully |
| Required planning references | Reads denied: restricted roots included workspace and evidence, but omitted the staged plugin |
| Manifest | Read successfully |
| Full discovery export | Read failed at the client's 256 KB limit; no bounded recovery was observed before the stop |
| Proposed edits | Both canceled before writing; completion and continuation were not observed |
| Overall outcome | Blocked setup; not a skill-wording acceptance result |

The blocked reads demonstrate an overly narrow launch boundary. They do not prove
that the reference files were missing from the self-contained export. A native
skill list and successful entrypoint load are insufficient reference-access checks.

The running process stayed on 2.1.312. The client announced an installed update
awaiting restart; after exit, a new version readback reported 2.1.316. No owner
update or restart command was issued. Installed-cache immutability was not
established, and the 2.1.312 observations do not qualify a later process.

## Corrected preparation, not another execution

A separate private packet preserves this failed attempt and proposes:

- Add evidence and plugin as separate restricted read roots; exclude the common
  preparation parent, owner rubric, starting copies and owner logs.
- Check required reference containment before inference. Deny both Edit and Write
  on the read-only evidence, plugin and workspace instructions; retain manual
  approval limited to the two task documents.
- Provide a small exact-field discovery identity extract with the original file
  hash and keep the full export unchanged for bounded reads when needed.
- Recheck the actual runtime version. An authorized future trial can use the
  documented process-only `DISABLE_AUTOUPDATER=1` control; it has not been applied
  globally or used for another task. See [official environment controls](https://code.claude.com/docs/en/env-vars).

Static containment, read-size, source-extract and preservation checks pass for
that preparation. They do not establish future client enforcement or behavior.
A new task needs a new explicit decision and fresh controls; the consumed session
is not reset. No canonical skill was changed to compensate for this setup error.

## Release implications

The [fresh online source check](upstream-freshness-2026-11-02.json) has 43 matching
sources, 26 changed and none unavailable. Each change still needs individual
review before any justified pin update. No pin, fingerprint or freshness policy
changed in this pass; changed fingerprints are not confirmed skill defects.

Human chooser results remain unscored. Codex billing controls, Antigravity
isolation, other apps and the second Mac retain their own qualification work.
See [release status](../release-status.md) for the remaining boundaries. No merge,
tag, release, installed-skill change or cross-client acceptance follows here.
