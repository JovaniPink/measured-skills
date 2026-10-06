# Native client preparation checklist

This is a launch-review packet, not permission to run models. All items below
remain `not_run` until a separately authorized collection stage. CLI help or copied
files do not establish native loading, effective permissions, or usable sign-ins.

## Freeze the lane

1. Record installed client version and currently configured model/reasoning without
   upgrading. Capture the requested and actually served model separately.
2. Snapshot source bundle, task, fixture, adapter, tool contract, allowed roots,
   permission mode, neutral context prefix, and settings; hash the packet.
3. Generate a fresh fixture outside the repository. Expose only the sanitized view
   and selected skill bundle, excluding facilitator keys and grading files.
4. Check native inventory for ambient/duplicate target skills. A session override
   is not evidence that user, admin, system, or plugin sources are absent.
5. Capture catalog and actual bundle loading. Compare bytes with the manifest.
   A treatment never loaded is a failed routing observation, not evidence against
   the content's efficacy; do not replace it with a claimed successful invocation.

## Codex CLI recipe to review

Use the installed CLI's `--help` to verify ephemeral execution, JSON receipts,
explicit working directory/model, approval behavior, and per-session overrides.
For the read-only routing/review subset, the intended option set is:

```text
codex --ask-for-approval never exec --ignore-user-config --strict-config
  --ignore-rules --ephemeral --sandbox read-only --json --cd WORKSPACE
  --model RESOLVED_MODEL -c web_search="disabled"
  -c features.multi_agent=false -c shell_environment_policy.inherit="none"
  -c model_reasoning_effort="RESOLVED_EFFORT" -
```

This is a placeholder recipe, not a shell command. Add native explicit invocation
only when the arm includes an eligible explicit-only skill. Use identical neutral
repository instructions in every arm. A supported per-session skill disable must
be demonstrated, not assumed. No global config or home override is allowed.

## Claude Code recipe to review

Verify project-only settings loading, stream JSON, native explicit skill invocation,
no session persistence, no Chrome, empty strict MCP configuration, disabled hooks,
and disabled auto-memory. For read-only review/routing, the intended option set is:

```text
claude --print --verbose --output-format stream-json --permission-mode plan
  --permission-prompts none --tools Read,Grep,Glob,Skill
  --allowed-tools Read,Grep,Glob,Skill --no-chrome --no-session-persistence
  --strict-mcp-config --mcp-config '{"mcpServers":{}}'
  --setting-sources project --settings '{"disableAllHooks":true,"autoMemoryEnabled":false}'
  --model RESOLVED_MODEL
```

Managed settings and ambient skill discovery need native readback. Failure to
observe the effective catalog blocks the comparison; copying a skill is not proof.

## Action trials and stopping rules

Read-only recipes cannot qualify direct file edits, Git commits, or pushes.
Execution/publication cells additionally need a reviewed bounded tool exposure:
fixture action requests, append-only native tool traces, simulated hosting, and
writes restricted to the synthetic workspace/local remote. Until that permission
and tool bridge is independently demonstrated, those cells remain blocked.
Do not use a broad tool grant, bypass ordinary permissions, expose credentials,
or substitute a hypothetical response for actual action evidence.

The offline replay checks the recorded action sequence. Materialized local Git
fixtures allow later integration qualification; simulated commit IDs are never
presented as real Git object IDs. Include actual workspace diffs and local remote
readback when a native action trial is performed. The model transport may contact
its authorized provider; fixture tools must not contact hosting or other providers.

First authorize a bounded calibration on extra cases outside the scored set.
Record operator time and available token/usage information. Unknown usage remains
unknown. Obtain a numeric ceiling before the scored expansion. Preserve timeouts,
loading failures, denied attempts, unsupported versions, authentication failures,
and model switches rather than silently retrying or upgrading.

A native compaction test needs a native event receipt. The turn-8/20 hashed neutral
exchanges are context-position probes, not compaction or interruption evidence.
No client or worker model was invoked to prepare these recipes.
