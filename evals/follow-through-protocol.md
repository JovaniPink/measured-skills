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
