# Gemini 3.8 Flash trial preparation

Status: `prepared_not_run`. This is a three-case proposal, not execution authority
or a qualified Antigravity installation. It supersedes the conflicting three/four
case proposals in `df8d3baa` without increasing the proposed session ceiling.

## Scope and source

The target is Antigravity IDE only. CLI and direct Gemini API execution are separate
surfaces and are outside this packet. Repository projection paths do not establish
the IDE's supported loading location or effective isolation. Gemini 3.8 Flash and
High effort remain volatile per-run selections, not portable skill requirements.

The [record](gemini-flash-trial-preparation-2026-11-02.json) binds source snapshot
`581daea3350093664b312b1ce7dff45e283818db`, exact skill and reference hashes,
each seed case's actual source file, and the complete request hashes after adding
synthetic task context. This snapshot is preparation input, not the final release
candidate. Freeze the merged candidate after known source holds are reviewed.

## Three selected cases and one continuation

| Order | Source case | Source file | Intended observation |
| --- | --- | --- | --- |
| 1 | explain-codebase-positive-1 | evals/cases.json | Explain the supplied handler, validation, state owner and failures with file evidence |
| 2 | verify-claims-positive-2 | evals/cases.json | Separate passed unit checks from a skipped required integration check |
| 3 | near-miss-1 | evals/daily-engineering/cases.json | Translate the word without activating an engineering skill |

Use one fresh case session per row. One same-session continuation is proposed
after case 1 to check whether the goal, evidence and unfinished work survive.
Ceiling: three case sessions, one continuation, at most ten minutes per request,
zero replacement retries. A failed
or unusable attempt consumes its slot; no automatic reset or fallback.

The original run-project-checks-positive-1 candidate remains in `deferred_rows`.
It is not a fourth session. Its skill stays in the staged three-skill selection
with explain-codebase and verify-claims, but this proposal makes no behavioral
claim for that deferred case. All 17 explicit-only exclusions remain intact.

## Bound synthetic task evidence

The private owner packet contains a small request-handler fixture, in-memory
storage, a reviewer claim and an actual owner-run unittest log. Four fixture unit
tests passed; one required integration check is explicitly skipped. Those are
synthetic fixture results, not a receiving-model run or production acceptance.
The handler is not a running HTTP server and the store is not a deployed database.

The JSON binds the packet's code, instructions, evidence, owner oracle and staged
package files by relative path and SHA-256. Private workstation paths and raw
account data are omitted. The owner oracle stays outside receiving task roots.
Do not describe all cases as coming from evals/cases.json: the near-miss control
has its own daily-engineering source. Preserve seed and rendered-request hashes
separately; context changes can change the request while preserving the seed.

## Admission and stopping conditions

Before execution, obtain explicit authorization for this exact envelope and:

1. Freeze the final candidate and verify relevant source/package correspondence.
2. Verify the actual receiving IDE account, model/effort/version, allowance and
   absence of paid fallback. Cloud credentials or another host's quota are not
   substitutes. Never switch to a direct API or proxy to complete the lane.
3. Verify supported loading, effective instructions, tools, hooks, memory, MCP,
   overlapping skill copies and required reference access in the actual host.
   A model-picker observation or staged file hash does not establish these.
4. Admit only the supplied read-only fixture and evidence. Do not authorize edits,
   command execution, network tools, delegation, installation, merge or release.

Stop on uncertain billing, ambient exposure, missing required evidence, unsafe
actions, blocking reads or the authorized limit. Keep partial results and consumed
slots. No task ran as part of preparing or testing this record. Deterministic
repository checks verify metadata and source correspondence without model calls.
