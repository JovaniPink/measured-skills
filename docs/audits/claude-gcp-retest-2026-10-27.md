# Claude GCP and native-control retest, October 27

All four cases and both fixed follow-ups completed on Claude Code 2.1.311,
Haiku 5.5 (`claude-haiku-5-5`), medium effort, manual permissions. The allowance
is consumed, with no model retries. **Claude acceptance remains failed.**
The native controls are valid this time, but two output defects remain.

The [machine-readable observation](claude-gcp-retest-2026-10-27.json) records
input, transcript, staged-body and reference hashes. The
[frozen preparation](gcp-routing-retest-preparation-2026-10-26.json) remains an
unchanged historical proposal. The user separately authorized this execution;
its earlier `prepared_not_run` status is not a statement about this new result.

## Source and preconditions

The tested clean source is `1a23a574f43e1e9032985f97536bb0b1ce35262c`, with manifest
source `a55f0f750d64e005f6768dba2c5c971a1f5fbfd0`. A new daily-profile stage used
the existing exporter and `measured-daily-pilot` wrapper. All 50 receipt files
matched before and after execution. No installed skill was updated.

Fresh native authentication identified the existing first-party Claude Pro route.
The browser usage page showed credits off, auto-reload off and available included
quota. Native usage independently showed credits off and available quota before
and after input. No provider environment override was present. No login or billing
setting was changed, and no paid fallback was requested. Native token-cost
estimates are not evidence of an invoice or extra charge; these observations
establish the checked route, not an account-wide billing audit.

The disposable workspace had twelve staged profile skills and sixteen native
built-ins. Native context readback had no ambient memory or MCP category. Hooks
and auto-memory were disabled, MCP configuration was strict and empty, and only
project/local settings were selected. Local reference reads used one-time manual
permission. No cloud query, provider job, file mutation or external communication
occurred in the cases. The native session was closed after the final usage check.

## Observed results

| Case | Selection and loading | Output finding |
| --- | --- | --- |
| Implicit GCP | Expected Skill call, exact expanded body, exact warehouse reference | Failed: the answer promoted an example's authoring clock and unbounded event age into supplied facts. |
| Translation near miss | No skill or tool call | Passed the inspected requirement: translated hello as hola. |
| Native GCP control | Registered command dispatched; exact body and warehouse reference | Passed inspected core requirements: retained missing contracts and avoided prescribing a fixed window or assuming a merge strategy. Limited to supplied synthetic context. |
| Native code-review control | Registered command dispatched; exact review body | Failed the prediction distinction: a desired denial assertion was described as the predicted result under an assumed missing tenant control. |
| Pause and resume follow-ups | Same review session; goal, conditional finding and gaps retained | No unrun check was claimed passed. Both carried the desired-result versus prediction problem forward. |

Each control command was typed outside the paste envelope, followed by its exact
arguments and one submission. Transcript command markers and expanded bodies
confirm native dispatch; a later model-issued Skill call is not the basis for
this conclusion. Four distinct case sessions and both exact follow-up payloads
were checked. The implicit GCP payload's native paste envelope was removed only
for comparison with the frozen input, not from the retained raw receipt.

### Unsupported GCP facts

The implicit answer states: "Corrections arrive within two days of being authored,
but they can update events from any earlier date." The case only says corrections
can arrive two days late. Neither the reference clock nor the maximum event age
was supplied. They must remain unknown. The canonical skill contains a separate
example with those facts; this suggests example leakage, but one observed answer
does not prove the cause. Other parts of the answer correctly asked for missing
contracts. Those qualifications do not undo the factual overstatement.

### Desired assertion versus predicted behavior

The code-review answer correctly made cross-tenant exposure conditional on the
uninspected store and upstream authorization contract. It kept test existence
unknown and execution unrun. However, after proposing not-found or forbidden for
a cross-tenant request, it described this as an expected result assuming no implicit
scoping. The resume answer again called denial a prediction under the stated
assumptions. That confuses the test's desired assertion with the vulnerable
implementation's predicted response. With an unscoped store and no equivalent
control, the predicted response is the other tenant's object; a test asserting
denial should then fail. Neither result was executed or observed here.

## Limits and next work

This is Codex-assisted grading against the prepared contract, not independent
human acceptance or an automated judge. A direct-control pass does not erase an
implicit failure. Known synthetic cases, one model and one client version cannot
establish selection reliability, causal improvement, whole-profile acceptance,
app acceptance, second-machine acceptance or cross-client parity.

The first follow-up submission was blocked as ad hoc before input delivery.
Its exact frozen hash and unused request count were verified, after which the
same authorized submission was allowed. Native input confirmation preceded one
actual delivery. This guard event did not add a model request or retry.

Next, inspect how the GCP example is separated from case facts and clarify the
review contract's distinction between a desired assertion, a predicted response
and an observed outcome. Review those repairs offline before proposing another
bounded run. No further model execution is authorized by this record.

Raw sessions, account observations and screenshots remain private. This update
changes documentation only. Canonical skills, generated projections, archives,
frozen inputs, source pins, the accepted originality packet and the existing
manifest binding remain unchanged. Online freshness was not rechecked; retain
the dated source closeout and other blocked client lanes. Release remains held.
