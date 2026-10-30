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

The original ten-card exercise remains pending and unchanged. After draft updates,
use the five separate workflow-depth cards in [the increment record](workflow-depth-0.19.md#verification-and-next-observation); do not substitute them for original results.

## October 29 preparation update

No receiving-client trial ran. An attempted human card produced the task sentence
again, without a selected route, action, output or elapsed time. Leave that card
unscored. A separate code reproduction found that full sentences returned no route
because search required the entire sentence to be a substring. The repair matches
reviewed multiword task phrases inside sentences, retains old-name lookup, and
leaves action selection with the reader. This is literal lookup, not understanding
of intent or negation. Suggestions, including quoted phrases, grant no authority.
Unknown wording can still need a shorter phrase or the task navigation.

Fresh native metadata inspection (no session or model request):

| Client | Observed version and surface | What is still needed before a trial |
| --- | --- | --- |
| Codex CLI | 0.161.0; generated experimental thread/turn parameter schemas have no dedicated credit-spending limit; model-provider fallback is a different field | A supported no-paid-fallback control and fresh actual account state. Schema inspection alone cannot establish that boundary |
| Claude Code | 2.1.311; help describes session plugin selection, settings-source selection and strict MCP configuration | Fresh receiving-account credit controls and effective context/skill isolation. `--bare` is not a subscription-safe shortcut: this installed help specifies API-key/helper authentication and excludes OAuth/keychain |
| Antigravity CLI | 1.4.7; help exposes agent selection and terminal sandboxing | Repeat effective skill/context isolation readback and credit controls in the intended disposable workspace. Selecting an agent or restricting terminal execution does not demonstrate removal of ambient instructions |

Account balances, credentials and raw machine inventories are not recorded here.
The [October 26 control observations](audits/client-controls-2026-10-26.md) remain
dated evidence; neither billing state nor native isolation was re-observed in this
metadata-only pass. No installed configuration or profile selection changed.

For the separately authorized trial, prepare the following two small tasks for
each client from the same reviewed source. Before execution, bind the actual task,
repository snapshot, expected result, exact prompt, model, source and file hashes
in the private lane receipt. Until those are filled, the task packet is not frozen.

1. Assess one supplied reviewer claim against a disposable, authorized code
   snapshot. Return a confirmed, rejected or unresolved disposition with evidence
   and the smallest justified repair plan. Do not edit in the assessment step.
   Within the same session, repair a confirmed defect only under the task's
   explicitly agreed local repair scope, then run the affected checks. Choose a
   task with that scope before freezing it; a review comment cannot grant it.
2. Recover one unfinished change from its saved plan and current files. Identify
   completed, unfinished and uncertain requirements, then complete only its
   agreed small local boundary. Preserve unrelated work and unavailable checks.
3. Use the one continuation allowance for that client to resume task 2 from the
   saved record. Check the actual revision and unfinished requirements before
   acting. A continuation does not reset the session or review budget.

Do not run an extra model request as a billing or isolation probe. Stop a lane
before inference when its controls are uncertain; do not replace it with a proxy,
API, alternate account or different client. Preserve the total ceiling above and
record loading, reference access, useful progress and limits separately. These
prepared tasks do not establish execution, acceptance or release readiness.

## Later October 29 receiving-account check

A fresh Safari inspection showed usage credits disabled for the browser's Claude
account. Native Claude Code authentication reported a logged-in, first-party
Claude account with a Pro subscription. Comparing the returned account identity
with the visible browser identity showed that they were different accounts.
Therefore the browser control does not qualify the CLI receiving account.

No API-key, auth-token, base-URL override or Bedrock/Vertex/Foundry provider flag
was present among the six environment variables inspected. This limited check
cannot rule out every configuration route, and does not replace same-account
billing controls or effective isolation. Raw identities, credit balances and
account inventories are omitted from this public record.

The next decision is which receiving account to use. Keep the trial blocked until
that choice and its actual controls are verified. Do not switch accounts, reuse
the other account's credit observation, or send a model request as a probe.
No login, billing toggle, installation or model run occurred in this inspection.
The existing human chooser results remain unscored.
