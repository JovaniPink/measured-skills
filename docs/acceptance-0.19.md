# 0.19 acceptance: finding and finishing work

Status: prepared, not run. These are chosen product targets, not measured benefits.
The first exercise has no model calls. Give the user one initial orientation, then
present the following fictional task cards without coaching. Record elapsed seconds,
selected route/scope, wrong selections, help requests, prompt intent, expected output
and stopping point. Unknown results stay unknown; do not fill them from inspection.

| Card | Task | Suitable route |
| --- | --- | --- |
| 1 | Recover a half-finished draft and list what remains | Finish / assess |
| 2 | Repair the agreed retry bug locally without pushing | Finish / repair |
| 3 | CI is red and the cause is unknown | Diagnose |
| 4 | Evaluate a reviewer's disputed claim before editing | Review or finish / assess |
| 5 | Plan a new filter that must preserve existing sorting | Plan |
| 6 | Check whether a request accidentally permits deployment | Prompt review |
| 7 | Design an optional interactive explanation | Motion |
| 8 | Compare an old plan with today's implementation | Reconcile |
| 9 | Update an existing draft and follow its checks | Maintain draft |
| 10 | Explain the save path before changing it | Understand |

Targets: at least nine suitable routes and prompts without coaching; median
selection time at most 60 seconds after orientation; zero misleading authorization;
and successful rediscovery from a bookmark in a later session. If selection is
still hard, simplify words and navigation before adding more capabilities.

## Later real-work trial: separate authorization required

Freeze two bounded tasks per client (Codex CLI, Claude Code, Antigravity CLI):
one review-finding or defect repair, and one unfinished-work recovery. Permit one
continuation follow-up per client. Ceiling: six sessions and three follow-ups,
not an automatically renewable budget. No trial ran as part of implementation.

Before each lane: verify source, machine, account, isolation, permissions, included
allowance and absence of paid fallback. Stop unavailable lanes; never substitute an
API, proxy, account or billing route. Record model/client versions, exact source,
loaded skill/reference evidence, outcome, failed checks, retained blockers, repeated
instructions and unnecessary ceremony. Keep failures and client results separate.
Desktop, web accounts and the second Mac need their own later observations.

A small trial cannot establish financial benefit, statistical reliability,
defect-detection accuracy, or cross-client parity. Release approval stays separate.
