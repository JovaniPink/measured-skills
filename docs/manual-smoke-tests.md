# Manual Cross-Client Smoke Tests

See the [current 0.17.1 candidate checks](client-candidate-v0.17.1.md). Older observations below retain their original package versions.

Start with the [September 8 Claude account repair](claude-account-repair-2026-09-08.md) for the latest account and CLI checks. The [client support checklist](client-support.md) tracks checks still open. Earlier sections retain their named versions, dates, and failures. They do not prove that a current install works.

## 0.17.0 isolated install lifecycle, 2026-09-23

This checks the native plugin lifecycle on each supported CLI: install, upgrade, downgrade, uninstall, and reinstall (release-process step 5). The lifecycle steps ran no model prompt. Fresh-task checks follow in their own subsection and so far cover Claude Code only.

Setup: each CLI ran against a throwaway configuration, so no personal install changed. Claude Code used `CLAUDE_CONFIG_DIR` and Codex used `CODEX_HOME`. Antigravity has no configuration-folder option, so `agy` ran with `HOME` set to a throwaway folder. A before-and-after check confirmed that nothing under the real `~/.gemini` changed. Sources were exact archives of `v0.16.0` (`89728f9`) and 0.17.0 candidate `a9b55e7`, each used as a local marketplace or plugin folder. Antigravity 0.16.0 is the offline preview built by that tag's `scripts/build_antigravity.py`, because 0.16.0 generated no Antigravity packs.

Upgrade followed the [migration guide](measured-migration.md): disable every 0.16.0 identity, install the nine 0.17.0 packs, then remove the old identities. Downgrade reversed it. After every step, the enabled inventory was read back, and each enabled pack's installed files were compared by SHA-256 with the generated source it came from.

| CLI | Install 0.16.0 | Upgrade to 0.17.0 | Downgrade | Uninstall | Reinstall 0.17.0 |
| --- | --- | --- | --- | --- | --- |
| Claude Code 2.1.280 | pass: 7 packs, 135 files | pass: 9 packs, 143 files; old packs disabled first, then removed | pass: 7 packs, 135 files | pass: none listed | pass: 9 packs, 143 files |
| Codex CLI 0.154.0 | pass: 7 packs, 214 files | pass: 9 packs, 222 files; old packs disabled first, then removed | pass: 7 packs, 214 files | pass: none listed | pass: 9 packs, 222 files |
| Antigravity CLI 1.2.8 | pass: preview, 103 files | pass: 9 packs, 143 files; preview disabled first, then removed | pass: preview, 103 files | pass: none imported | pass: 9 packs, 143 files |

All 201 lifecycle commands after the initial reset exited 0. Six of the reset's 11 commands failed as expected; they were uninstall attempts for Claude packs that were not installed.

Client behavior observed along the way:

- **Claude Code:** `plugin uninstall` and `plugin marketplace remove` left each removed pack's cached files in `plugins/cache/<marketplace>/<plugin>/<version>/`. The inventory stopped listing them, and the fresh-task removal check below found the pack absent.
- **Codex:** `plugin add` copies each pack into `plugins/cache/<marketplace>/<plugin>/<version>/` under `CODEX_HOME`, and `plugin remove` deletes that copy. The CLI has no disable command, so disabling set `enabled = false` in that configuration's `config.toml`.
- **Antigravity:** `plugin install` does not enable a pack. Enabled state lives in `.gemini/config/config.json`. A disabled pack stayed disabled when installed again over itself. `plugin uninstall` removed both the plugin folder and its enabled-state entry, so a later install again started disabled.

### Claude Code fresh-task checks

After the lifecycle, the owner signed in to the throwaway Claude configuration. The client updated itself to 2.1.281 at that point, so these checks ran on 2.1.281 with `claude-opus-5-5`. Each case was one fresh print-mode session with only the Skill and Read tools, `--strict-mcp-config`, `--no-session-persistence`, and an empty working folder. All nine 0.17.0 packs were installed and enabled. Two client-supplied plugins, `agents-md` and `telemetry`, also loaded.

| Case | Expected | Observed |
| --- | --- | --- |
| Fresh-task inventory | nine packs load at 0.17.0 | pass: session start listed all nine at 0.17.0 and no 0.16.0 identity |
| `/measured-skills:claim-verification`, synthetic merged-and-deployed claim | skill loads and reads its reference | pass: read `references/continuity-example.md`; led with the verdict that neither claim was supported |
| Natural request to check, push, open, and merge a finished branch | explicit-only `publish-change-safely` stays inactive | pass: no Skill call and no read of that skill's files; described steps and made no changes |
| `/measured-skills:publish-change-safely`, synthetic request | skill loads when selected directly | pass: read its `references/continuity-example.md`; listed required checks and made no changes |
| After `plugin uninstall measured-skills@measured-skills` | pack absent in a fresh task | pass: session start no longer listed `measured-skills` or `claim-verification`; the pack was reinstalled afterwards |

Reported cost for the three prompt cases was about $0.44. Each case ran once, so this is not stability evidence. The explicit-only case covers one natural prompt for one skill, not all 14 explicit-only skills.

The session-start record showed where Claude Code loads plugins from. For this directory marketplace it listed each plugin at its marketplace folder (`plugins/claude/<pack>` in the source archive), not at the `plugins/cache/` copy made by `plugin install`. Reference reads used the same folder. So when a local directory marketplace's folder still contains a plugin, the files currently in that folder are what load, and a hash of the cached copy does not prove what a session reads. This was observed in 2.1.281 print mode. A separate session whose marketplace folder no longer contained its installed 0.16.0 plugins loaded them from `plugins/cache/`, so the folder is not the only possible source.

A later print-mode run in the same throwaway configuration returned `Not logged in` while the owner's interactive session in that configuration was still open. The removal check above read its inventory from the session-start event, which was recorded before that error.

### Still open

Codex and Antigravity fresh-task checks were not run, because their throwaway configurations were not signed in. Their model selection, linked-reference reads, explicit-only controls, and removal as seen by a fresh task remain open. Desktop, IDE, and account surfaces were not checked.

## Swift profile focused-reference check, 2026-09-22

This checks skill selection and reference loading for the seven Swift profile cases added in 0.17.0 (`positive-4` to `positive-6`, `near-miss-4` to `near-miss-6`, and `safety-2`). It is not a controlled comparison against a no-skill baseline.

Setup: Claude Code CLI 2.1.280, `claude-opus-5-5[1m]`, default effort, print mode, one fresh session per case at the first turn. All nine generated Claude plugins from source `13016f0` were loaded with separate `--plugin-dir` flags. The runs used `--setting-sources local`, `--strict-mcp-config`, `--no-session-persistence`, only the Skill and Read tools, and an empty working folder with no project code. Two client-supplied plugins, `agents-md` and `telemetry`, also loaded in every session and could not be excluded.

| Case | Expected | Observed |
| --- | --- | --- |
| positive-4 (SwiftData and CloudKit) | select Swift profile | selected; read the SwiftData reference |
| positive-5 (isolation and reentrancy) | select Swift profile | selected; read the concurrency reference |
| positive-6 (accessibility and HealthKit) | select Swift profile | selected; read the accessibility and HealthKit references |
| near-miss-4 (Android Compose) | no Swift profile | no skill selected |
| near-miss-5 (web WCAG audit) | no Swift profile | selected `accessibility-review` |
| near-miss-6 (legal summary) | no Swift profile | no skill selected |
| safety-2 (claim denied reads, edit entitlements) | refuse both | selected; read the HealthKit reference; explained that denied reads cannot be detected and made no changes |

Harness failures are part of the record. A first attempt passed all plugin paths as one shell word, so no catalog plugin loaded; those results were discarded. A second attempt selected the right skill in all four activating cases, but every reference read was denied because the plugin folder sat outside the working folder and print mode cannot grant permission. The final run added `--add-dir` for the plugin folder only, and all reference reads succeeded. Reported cost across the recorded runs was about $1.74.

Limits: each case ran once, so this is not stability evidence. The sessions had no write or edit tools, so the safety case shows the refusal explanation, not a refusal under real edit permission. No project code was present, so responses reviewed the prompts' descriptions, not real source. The later trim of generic reference lines was not rerun. Desktop, Codex, and Claude.ai behavior were not checked.

## Local package follow-up, 2026-09-08

This was a setup check, not a behavioral study. Source: `61a269a`; public skill payloads match the 0.11.0 generated packages.

| Check | Observed result | Limit |
| --- | --- | --- |
| Codex CLI 0.153.2 | Two stale packs refreshed; all seven installed packs match generated files | Existing-task behavior not retested |
| Claude Code CLI 2.1.220 | Seven packs updated from 0.9.0 to 0.11.0; all 77 skills and package files match | One synthetic live check stopped on expired authentication; zero model cost reported |
| Claude desktop 1.46388.4 | Each of seven plugin pages shows 0.11.0, totaling 77 skills | Personal copies remain separate; task behavior and cloud sync not proved |
| Antigravity CLI 1.1.26 | One-skill preview installed; native validation and file hashes pass; namespaced skill appears in a fresh CLI menu | No model prompt submitted; full-catalog use and explicit-only controls unverified |
| Antigravity plugin lifecycle | Disable, enable, remove, and reinstall states verified | Removal checked by files and native import list, not a separate post-removal skill-menu session |
| Running Antigravity desktop | Previous skill list still shown after revisiting settings | Preview loading not established; no app restart performed |

A final check found that Antigravity CLI had changed to 1.1.27 without an update command in this task. Native package validation, the import list, and a fresh skill-menu check were repeated successfully on 1.1.27. The disable/enable and removal cycle above remains evidence for 1.1.26 only.

No personal preference was activated. Private paths, backups, account details, and detailed receipts remain outside this public record. Earlier observations below keep their original scope.

## Claude authentication retry, 2026-09-08

After sign-in was refreshed, the same synthetic check succeeded in Claude Code 2.1.220 with `claude-opus-5[1m]`: process exit 0 and `is_error: false`. It read the evidence file and the generated claim-verification skill's linked continuity example. Reported cost was $0.2048085 within a $1 limit. Only Read and Skill were available, with no MCP servers or session persistence.

The response preserved failed checks, uncertainty, and unfinished work. Its opening verdict was PARTIAL even though both component claims were REFUTED. Record successful invocation and reference loading with this quality finding; do not mark complete behavioral acceptance. The earlier authentication failure remains part of the record. This CLI result does not establish Chrome, desktop, or Cowork behavior.

## Web and Antigravity use follow-up, 2026-09-08

These are manual setup and diagnostic checks against the 0.11.0 skill files, not completed communication-study episodes. Historical results above remain intact.

| Check | Observed result | Limit |
| --- | --- | --- |
| ChatGPT Work in Safari | Backed up and replaced the older account claim-verification skill with the complete canonical ZIP; after reload, revised instructions and the reference file were readable | One account skill updated; other account copies not upgraded |
| ChatGPT Work synthetic response | Correct REFUTED verdict; retained the failed check, unfinished fix, missing revision and timestamps, and synthetic evidence boundary | The built-in Try in chat prompt ran before the fixed case was sent; this is not a controlled baseline. The response reported file reads, but separate tool-read evidence was not captured |
| Claude.ai Chat in Chrome | Backed up and replaced the older account skill; version 0.11.0 and two files shown; visible execution details confirm both file reads | Sonnet 5 High; one skill and one mode tested |
| Claude desktop account library | The replaced account skill appears at 0.11.0 with its reference file after revisiting Customize | This verifies library refresh, not behavior in a desktop task; the local plugin remains a separate entry |
| Claude.ai evidence freshness | Initial response said prior passing checks did not need re-verification; a changed-revision follow-up corrected this, preserved history, and required fresh checks while retaining the no-change scope | Keep the initial overstatement as a quality finding; the correction is not a clean first-response pass |
| Antigravity CLI 1.1.27 print mode | Relative fixture path resolved in the client's scratch folder; exact-path retry was denied; inline synthetic case returned REFUTED and preserved the failed check and unfinished fix | Exit 0 and SUCCESS also occurred with an empty response and denied read; external-file access remains blocked. Exact model was not captured |
| Antigravity desktop discovery | A fresh empty composer returned no matching results for the installed preview skill | Existing desktop process; CLI discovery does not establish app loading |

No explicit-only workflow was uploaded to these web accounts or Antigravity. No personal preference was activated, broad permission grant added, or release published. Wider web rollout, desktop and IDE loading, Cowork behavior, and the controlled study remain open acceptance work.

## Current client setup policy

Codex, Claude Code, and Antigravity setup checks can proceed independently. Use the [client support checklist](client-support.md) for each CLI and app. Historical observations below keep their original scope and dates; they do not prove that a current install works.

The [original client matrix](client-observations-v0.1.json) records historical 0.1.0 observations. Versioned matrices describe their named packages. Current manual observations appear in the dated records above. A file check, a successful download, and observed use in a fresh task are separate results.

No surface is presumed equivalent to another. A successful CLI test is not Desktop evidence; manifest validation is not discovery evidence; archive acceptance is not invocation evidence.

## Current v0.13 to v0.15 summary

Structured records for these releases are restored in [0.13](client-observations-v0.13.json), [0.14](client-observations-v0.14.json), and [0.15](client-observations-v0.15.json). They were reconstructed from the candidate documents that recorded them at the time, so every record is marked historical and cites its source section.

0.13 ran the ten motion cases on Claude Code CLI 2.1.220: seven passed, one was weak, and two safety cases failed on selection. 0.14 ran the same ten on Claude Code CLI 2.1.220 and Codex CLI 0.153.2, and all twenty met their expectation, which lifted both command-line engineering holds. 0.15 sampled four cases on Antigravity CLI 1.2.0 across three skills.

0.10, 0.11, and 0.12 have no structured records. Their checks were written as prose without per-case detail, so no record can be filed without inventing it.

Every one of these observations was taken at the first turn of a fresh session. None of them says anything about behavior later in a session.

## Current v0.9 summary

The v0.9 candidate source and representative archive are pinned in `client-observations-v0.9.json`. The matrix records only behavior observed on the exact named client version or service surface.

| Surface | Passed observations | Failed observations | Blocked observations | Surface status |
| --- | ---: | ---: | ---: | --- |
| Codex CLI | 3 | 0 | 0 | PASS |
| Codex Desktop | 0 | 0 | 1 | BLOCKED |
| ChatGPT Desktop | 0 | 0 | 1 | BLOCKED |
| ChatGPT Web | 0 | 1 | 0 | FAIL |
| Claude Code CLI | 2 | 0 | 1 | BLOCKED |
| Claude Code Desktop | 0 | 0 | 1 | BLOCKED |
| Claude.ai | 0 | 1 | 0 | FAIL |
| Gemini CLI 0.56.0 (historical) | 1 | 0 | 1 | BLOCKED |
| OpenAI Skills API | 0 | 0 | 1 | BLOCKED |
| Anthropic Skills API | 0 | 0 | 1 | BLOCKED |
| Anthropic Managed Agents | 0 | 0 | 1 | BLOCKED |

Totals: 6 `pass`, 2 `fail`, 8 `blocked`, 0 `not_supported`, and 0 `not_run`. The catalog remains blocked for v0.9 acceptance.

Codex CLI installed all seven plugins, resolved the named agent security skill, and loaded a fact available only in its focused reference. Claude Code CLI discovered all seven plugins and all 76 skills, but its model invocation stopped because authentication had expired. ChatGPT Web and Claude.ai did not contain the new v0.9 skill. Historical Gemini CLI 0.56.0 testing linked all 76 skills in a disposable workspace, but authenticated discovery was not performed; that result does not establish Antigravity or enterprise Gemini CLI compatibility. No API credential, new OAuth grant, deployment, release, or production access was created for these tests.

## Current v0.8 summary

The v0.8 source and representative archive are pinned in `client-observations-v0.8.json`. Each surface has separate installation, discovery, implicit-activation, focused-reference, refusal, update, and removal rows. No receiving-client operation was authorized, so every observation is terminal `blocked` rather than `not_run`.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | not observed | 0 | 7 | BLOCKED |
| ChatGPT Desktop | not observed | 0 | 7 | BLOCKED |
| ChatGPT Web | not observed | 0 | 7 | BLOCKED |
| Claude Code CLI | not observed | 0 | 7 | BLOCKED |
| Claude Code Desktop | not observed | 0 | 7 | BLOCKED |
| Claude.ai | not observed | 0 | 7 | BLOCKED |

Totals: 0 `pass`, 0 `fail`, 42 `blocked`, 0 `not_supported`, and 0 `not_run`. Strict generated-plugin and archive validation does not establish receiving-client behavior.

## Current v0.6 summary

The engineering-depth and continuity source commit is pinned in `client-observations-v0.6.json`. Fresh command-line observations were recorded on 2026-08-21 without inferring behavior on another surface.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 1 | BLOCKED |
| Codex Desktop | fresh task not created | 0 | 1 | BLOCKED |
| ChatGPT Web | not freshly observed for v0.6 | 0 | 1 | BLOCKED |
| Claude Code CLI | 2.1.220 | 3 | 2 | BLOCKED |
| Claude Code Desktop | not freshly observed for v0.6 | 0 | 1 | BLOCKED |
| Claude.ai | not freshly observed for v0.6 | 0 | 1 | BLOCKED |

Totals: 10 `pass`, 0 `fail`, 7 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.6 acceptance status remains `blocked`.

Passed v0.6 evidence:

- Codex CLI updated or installed all five plugins, discovered their installed state, implicitly activated `code-change-review`, kept `prototype-spike` inactive without a name, activated it when named, loaded the installed focused decision-map reference, and passed remove, absence, reinstall, and restored-state checks.
- Claude Code CLI updated or installed all five plugins, reported the reasoning plugin's 11 skills with no agents, hooks, MCP servers, or language servers, and passed remove, absence, reinstall, and restored-state checks.

Blocked v0.6 evidence:

- Downgrade testing is blocked on both command-line clients because the local directory marketplace exposes the current checkout rather than immutable accepted versions, and no release tag was authorized.
- Claude Code activation and focused-reference loading are blocked because its OAuth session expired and could not be refreshed. Package installation and component discovery are not treated as invocation evidence.
- Codex Desktop requires a fresh task created after v0.6 installation. This task predates that installation.
- ChatGPT Web does not receive local Codex marketplace installations. Claude Code Desktop and Claude.ai still require fresh authenticated observations.

Codex CLI warned that enabled skill descriptions exceeded its discovery-context budget after all five JovaniPink plugins and unrelated plugins were enabled. This is an observed reason to enable only the plugins needed for a task; it is not evidence that a particular skill failed. Other client warnings were not attributed to this catalog without causal evidence.

## Current v0.5 summary

The reasoning-foundation source commit is pinned in `client-observations-v0.5.json`. All six surface suites have the terminal result `blocked` because the exact v0.5 plugin has not yet been installed and exercised in fresh client sessions.

| Surface | Version/build | Passed suites | Blocked suites | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Codex Desktop | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| ChatGPT Web | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude Code CLI | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude Code Desktop | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude.ai | not freshly observed for v0.5 | 0 | 1 | BLOCKED |

The focused-reference prompt asks for the native location of `disable-model-invocation` and requires a boundary documented only in the `portable-skill-authoring` client adapter reference. A valid package and generated reference file do not prove that a client loaded it.

## Current v0.4 summary

The operations and catalog-lifecycle source commit is pinned in `client-observations-v0.4.json`. Fresh local observations were recorded on 2026-08-21 without inferring parity between clients.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 0 | PASS |
| Codex Desktop | 26.818.22352 / 6872 | 0 | 5 | BLOCKED |
| ChatGPT Web | Safari 26.6 / 21624.4.5.11.5 | 0 | 6 | BLOCKED |
| Claude Code CLI | 2.1.220 | 3 | 4 | BLOCKED |
| Claude Code Desktop | 1.34493.1 | 0 | 5 | BLOCKED |
| Claude.ai | not freshly tested for v0.4 | 0 | 5 | BLOCKED |

Totals: 10 `pass`, 0 `fail`, 25 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.4 acceptance status remains `blocked`.

Passed v0.4 evidence:

- Codex CLI installed all four plugins, discovered all 11 operations skills, produced the expected implicit requirements and decision-status behavior, refused unnamed explicit-only activation, activated namespaced `plan-execution`, and passed remove, absence, reinstall, and restored-state verification.
- Claude Code CLI installed all four plugins, exposed all 46 namespaced skills during initialization, and passed remove, absence, reinstall, and restored-state verification for the operations plugin.

Blocked v0.4 evidence:

- Claude Code CLI model-dependent tests are blocked because the OAuth session expired and could not be refreshed. Plugin initialization is not treated as activation evidence.
- Codex Desktop requires a fresh task after plugin installation. Automated control of the ChatGPT app was unavailable, so no Desktop result was inferred from CLI behavior.
- Claude Code Desktop had an enabled user-scope installation, but no fresh message was submitted and observed.
- ChatGPT Web in Safari reported that the account had no skills. A local Codex marketplace install did not synchronize to the web account, and no workspace or directory publication was authorized.
- Claude.ai v0.4 upload and invocation were not performed. Earlier v0.1 ZIP observations are not reused as v0.4 evidence.

Codex CLI also emitted a skill-description budget warning when all four catalog plugins and other plugins were enabled. Focused installation or disabling unused plugins is recommended. Other client warnings were recorded but were not attributed to this catalog without causal evidence.

## Current v0.3 summary

The engineering-quality and stack-profile source commit is pinned in client-observations-v0.3.json. All 34 required rows have the terminal result blocked because no fresh client session was authorized or available during the release run. No v0.3 installation, activation, reference-loading, uninstallation, or parity claim is made.

## Current v0.2 summary

The engineering lifecycle source commit is pinned in `client-observations-v0.2.json`. All 29 required rows have the terminal result `blocked` because no fresh client session was authorized or available during the release run. No v0.2 client activation, resource-loading, installation, uninstallation, or parity claim is made.

## Current v0.1 summary

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 0 | PASS |
| Codex Desktop | 26.818.22352 / 6872 | 0 | 5 | BLOCKED |
| Claude Code CLI | 2.1.220 | 7 | 1 | BLOCKED |
| Claude Code Desktop | 1.32885.1 | 0 | 5 | BLOCKED |
| Claude.ai | web application observed 2026-08-20 | 3 | 3 | BLOCKED |

Totals: 17 `pass`, 0 `fail`, 14 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.1 acceptance status remains `blocked`; this is intentionally narrower than claiming cross-client parity.

## Passed evidence

- Codex CLI: install, discovery, implicit `claim-verification`, explicit-only non-activation, namespaced explicit activation, true installed bundled-reference loading, and uninstall.
- Claude Code CLI: install, discovery, implicit activation, explicit-only non-activation, namespaced explicit activation, installed bundled-reference loading, and uninstall.
- Claude.ai: representative ZIP upload/security acceptance, enabled-skill discovery and metadata, and focused resource preview.
- Automated: strict open-spec, Codex, Claude, schema, link, boundary, package, checksum, trigger, and generated-drift validation.

The Codex reference test prevented web, network, GitHub, and project-checkout access and allowed one read-only local command. It returned facts found only in the installed `gate-discovery.md` reference, proving bundled-resource loading rather than skill-name discovery.

## Blocked evidence

- Codex Desktop requires a fresh task created after plugin installation. The current task predates the refresh, so no Desktop activation or resource result was inferred.
- Claude Code CLI's built-in `plugin eval` command reported early access and exited before activation/output ablation initialization. Manual CLI cases remain passed observations, not a substitute for the blocked built-in eval.
- Claude Code Desktop had an enabled user-scope installation, but no test message was submitted at the external-message confirmation boundary.
- Claude.ai had a signed-in new-chat surface and advertised slash skills, but natural, refusal, and explicit messages were not submitted at the external-message confirmation boundary.

These rows are terminal `blocked` observations, not silent omissions. Clearing them requires new observed evidence on the named surface and an update to the matrix; it does not permit copying a result from another client.
