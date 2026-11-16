# Follow-through decision checks

The twelve cases in [follow-through-scenarios.json](follow-through-scenarios.json)
extend the [completion cases](completion-contract-scenarios.json). They are
independently written synthetic tasks, not reproductions of private workflows.
Each of six modes has a failure opportunity and a counterexample. Expected and
forbidden responses are facilitator-only grading criteria.

For an authorized manual check, expose only each case's ID, prompt, and named
candidate skill text. Ask for the next action, completion verdict, evidence limit,
and decision owner. Do not expose answer keys. Keep native discovery tests separate
from explicit text exposure. Record client version, requested and served model
when observable, skill bytes, tools, settings/isolation limits, time, output, and
per-case grading. Unknown model or loading facts stay unknown. Compare each client
separately; passing these decision checks does not prove actual tool execution,
compaction recovery, installation, lifecycle, or general behavioral improvement.

Use existing sign-ins and models. No API, account, billing, or model fallback is
part of this protocol. Stop a client on unavailable access or quota; retain its
unfinished cases. Do not turn fixture expectations into observed results.

After candidate checks pass, observe ten consecutive eligible ordinary tasks
that use the revised guidance, including both clients. Preserve task identity,
client/configuration, scope and relevant guidance in the existing task record.
Do not create a shared queue, change board status automatically, or schedule runs.
If only one client appears in the cohort, report the other as unobserved.

Count avoidable continuation corrections (exclude new scope and explicit pauses),
omitted required outcomes, unsupported completion/authority claims, identical
access retries without changed state, check reruns without changed inputs or a
reason, and review findings lost at integration. Keep unfinished tasks and missing
records in the denominator; unknown is not zero. Report case-level evidence and
counts, not invented savings, model rankings, or statistical significance.

Candidate pack byte changes invalidate earlier acceptance for those changed packs.
Historical lifecycle and acceptance records remain historical. Do not install,
publish, or relabel this candidate as a qualified release from these cases alone.

The [November 16 decision smoke record](follow-through-observations-2026-11-16.json)
records explicit-text observations only. The prepared cases retain their original
status; the dated observation is separate and does not qualify installation.

## Native loading checks

Keep package lifecycle, native invocation, and behavioral grading separate. Compare
the files the client actually reads with the candidate. For an explicit-only Claude
command, submit its slash invocation as the command at the start of the request.
Absence from the model-callable Skill tool is not proof that the plugin is absent:
check native inventory and invocation policy before reporting a missing install.
Record inline-plugin loading separately from installed-cache lifecycle results.
For behavior checks, select the skills named by that case. A combined inventory-load
check is separate; do not stack every skill output contract into an ordinary task.

Ask for the complete continuation record the skill requires: requested outcome and
target; retained completed work, decisions and evidence; remaining authorized work;
blockers and decision owners; completion verdict and evidence limits. Do not impose
a short-answer cap that omits fields the rubric grades. Keep the case prompts and
expected criteria unchanged, and do not supply answer keys to the receiving client.

Preserve failed or incomplete observations. If the harness changes, name the change
and re-exercise only the affected cases. A corrected run does not retroactively turn
the earlier result into a pass or establish a causal improvement from the skill.
The [native observation](../docs/audits/follow-through-native-2026-11-16.md) records
the candidate's bounded checks and their limits.
