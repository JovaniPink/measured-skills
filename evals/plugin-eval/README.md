# Native plugin eval suite

Status: prepared. One pass of `routing-specialist` has run, as recorded in
[First run](#first-run). The other four arms have not been executed. Every paid
run needs the maintainer's own yes.

This is the repeatable form of the November 5 Haiku exploration. It uses
`claude plugin eval` from Claude Code 2.1.316, so outside readers can rerun the
routing and outcome checks without the private harness.

## What is here

| Path | Purpose |
| --- | --- |
| `arms.json` | Model, limits, tool grants, cost ceiling, and case selection for each arm |
| `graders/` | Outcome graders copied into each behavior case |
| `fixture/build-half-finished-pr.sh` | Rebuilds the synthetic half-finished change, including its stash |
| `../../scripts/export_plugin_evals.py` | Generates one arm as a temporary plugin outside the checkout |

The exporter writes routing cases from `evals/cases.json`, assess requests from
`catalog/workflows.json`, and copies the generated packs from `plugins/claude/`.
It runs no client and writes nothing in this repository.

## Arms

Ceilings are hard stops for one pass. Estimates use the mean client-reported
list price per run on November 5. They cover agent runs only and are not a bill.
That data holds no judge cost, so the behavior ceilings leave room for three
judge calls per run.

| Arm | Cases | Runs each | Agent runs | Estimate | Ceiling |
| --- | --- | --- | --- | --- | --- |
| `routing-core` | 63 | 1 | 63 | $0.19 | $0.50 |
| `routing-specialist` | 128 | 1 | 128 | $0.40 | $1.00 |
| `routing-listing-8000` | 96 | 1 | 96 | $0.21 | $0.50 |
| `behavior-plain` | 2 | 10 | 40 | $0.31 | $1.25 |
| `behavior-forced` | 2 | 10 | 20 | $0.15 | $0.75 |

One pass of every arm stops at $4.00. The ceiling is checked before each run
starts, so runs already in flight can finish and overrun it slightly. A second
pass needs its own approval and its own ceiling.

- `routing-specialist` covers the 64 specialist positive cases and each
  specialist's first near miss.
- `routing-listing-8000` forces an 8,000 character listing. It uses the same 96
  positive cases as the November 5 overflow run.
- `routing-core` uses all 63 core cases in the full catalog.
- `behavior-plain` adds the native no-plugin baseline. `behavior-forced` loads
  `plan-change` by slash command. Compare it with the without arm of
  `behavior-plain`, which avoids the unresolved prefix that made the November 5
  repeat only a near repeat.

## Run an arm

Commit first. Exports refuse a dirty checkout. Choose a new folder outside the
checkout, under a parent that is not a symlink.

```sh
python3 scripts/export_plugin_evals.py --arm routing-specialist --output /private/tmp/measured-eval-specialist
```

The exporter prints the exact command and stores it in `receipt.json`. For this
arm it is:

```sh
CLAUDE_CODE_EFFORT_LEVEL=medium DISABLE_AUTOUPDATER=1 claude plugin eval /private/tmp/measured-eval-specialist --ablation none --threshold 0 --max-cost-usd 1.00 --concurrency 5 --no-publish --trust-plugin --output-dir /private/tmp/measured-eval-specialist/results --disallow-tools Agent Task TaskStop
```

Keep `--no-publish`: without it the report goes to claude.ai when the account
supports that. `--threshold 0` keeps exit 1 from reading as a failed measurement.
Exit 2 means the ceiling stopped the run and results are partial.

To compare wording, export the same arm from each clean checkout and run both.
Compare only runs of this suite. November 5 numbers are not a baseline for it.

```sh
python3 scripts/export_plugin_evals.py --arm routing-specialist --source /path/to/other/checkout --output /private/tmp/measured-eval-specialist-other
```

## What repeated runs mean

Repeated runs measure stability, not independent cases. Raising `--runs` shows
how much one prompt moves between runs. It adds no new tasks, and the behavior
arms still rest on one fixture. Report a repeat as a repeat, and raise the ceiling
in proportion only with a new approval.

## Reading results

Results land in `results/` inside the temporary folder. Do not commit them.
They hold raw traces. Each run in `aggregate-result.json` carries its grader
results, cost, turns, and any error.

- **Hit:** `expected-skill-called` passed. `no-other-skill-called` records a
  wrong skill on a positive case.
- **Near miss:** `own-skill-not-called` is the precision check.
  `no-skill-called` also fails when a better fitting skill fires, so read those
  requests before calling them errors.
- **Skill loaded:** every behavior run records `skill-tool-called` and
  `skill-body-seen`. A slash command loads the body without a `Skill` call, so
  read both. Compare skill and no-skill outcomes only on runs where a load is
  recorded.
- **Completed:** a run completed when `error` is null and
  `completion-cites-code` passed. That grader looks for code names that a blocked
  run cannot know, and it checks no planted trap. On the retained November 5
  outputs it passed all 140 runs that reported findings and none of the 12 blocked
  runs. Report blocked runs. Do not drop them. Check `error` as well as the score:
  in the offline check, runs that ended on an API error were still graded.

## Graders

Regex graders are free and scored. `reasoning-holds-up` adds a paid judge because
a matched sentence does not prove sound reasoning. These fixes answer the limits
in the November 5 record:

| November 5 weakness | This suite |
| --- | --- |
| `Retry-After` and `skip` matched as single words | The word must appear with a claim, in the same line: dropped from the plan or kept by the decision, or skipped on the jitter test |
| A jitter mention defined a completed run | `report-jitter-not-implemented` is an ordinary trap, and it can now fail |
| Loading was not recorded per run | Two indicators record it on every behavior run |

Patterns were checked offline against the retained outputs, which were also used
to tune them, so expect some misses on new wording. They found the billing change
in all 85 completed long-request runs and 5 of 55 short-request runs. Reports often
place it under an `Unrelated` heading, so that grader reads a short section.

Native graders have no custom code, so these are regex, tool, and judge graders.
`boundary-no-edit`, `boundary-no-write`, and `boundary-no-test-run` count attempts
from the trace, and the fixture's test file must survive.

## First run

One pass of `routing-specialist` ran on November 5 with Claude Code 2.1.316 and
Haiku 5.5, against the packs at `7a0da14`, which carry the added description
sentence. All 128 runs finished at $0.44 list price, and the ceiling did not stop
it. Raw traces are not kept here.

| Measure | Result |
| --- | --- |
| Positive cases that loaded the expected skill | 46 of 64 |
| Positive cases that loaded another skill | 1 of 64 |
| Near misses that fired their own skill | 0 of 64 |
| Near misses that fired any skill | 12 of 64 |
| Runs that hit the 4-turn limit | 48 of 128 |

**This run does not measure the added sentence, and the rise in specialist
activation is unexplained.** The sentence sits only on the nine core skills, and
this run has no baseline from this suite. The November 5 result of 17 of 64 is not
comparable, because that harness offered `Bash` and this arm does not. That
difference alone cannot explain the rise: a retest on the November 5 harness, with
`Bash` offered and a third-person wording of the sentence, also reached 32 of 64 on
the same prompts. The cause is unknown, and it may be drift between runs. An export
from a checkout without the sentence would give a baseline, but one pass cannot
separate an effect from drift.

## Offline check

Before the first run, the suite passed through the real loader at no cost. On
Claude Code 2.1.316 on macOS, one `behavior-long` run and one
`plan-change-positive-1` run were started with outbound network denied by
`sandbox-exec`, `ANTHROPIC_BASE_URL` set to a closed loopback port, and a dummy key.
Each run ended on a connection error and reported $0.00. That shows the following:

- Case files and graders load, and every free grader produces a verdict. The judge
  grader failed on the closed port, as expected, so its rubric has not been used.
- The scaffold builds the fixture in the workspace.
- The child lists all 90 catalog skills from the four packs.
- `--disallow-tools` leaves `Bash`, `Glob`, `Grep`, `Read`, `Skill`, and `ToolSearch`.

It shows nothing about routing, reports, or cost, and it does not test whether a
Bash grant works.

## Known limits

- Static reading of Claude Code 2.1.316 shows that
  `SLASH_COMMAND_TOOL_CHAR_BUDGET` and `CLAUDE_CODE_EFFORT_LEVEL` reach the eval
  child. No run has confirmed it. The offline check could not see the client's
  `Skill listing over budget` warning, which appears neither in the trace nor in the
  parent debug log. Until a run shows that warning or shortened descriptions,
  `routing-listing-8000` is not overflow evidence.
- `--ablation none` makes `tool_used: Skill` a scored grader. Under a two-arm run
  it is only an indicator, so keep routing arms single-arm.
- The setup differs from the November 5 harness, so expect some difference from
  those results. Routing runs have no `Bash`. Behavior runs grant read-only `git`
  commands, and the two `git stash` grants replace a client default that appears
  to have allowed them on November 5. The eval child listed 106 skills offline, against 112 on
  November 5: the 90 catalog skills plus 16 others, so the listing is not the same.
- A compound shell command is still denied. That blocked about 9 percent of
  November 5 runs, and this suite keeps measuring it.
- The nine-skill-only arm is not included, so the installed-set comparison has no
  native form yet.
- Safety cases and output rubrics in `evals/cases.json` are not exported. Routing
  arms measure selection only, not answer quality or safety behavior.
- Every result covers one model and one client. A pass here is not client
  acceptance, and it says nothing about Codex or Antigravity.

Authority: [Claude plugin evals](https://code.claude.com/docs/en/plugin-evals),
reviewed 2026-11-05, and `claude plugin eval --help` from Claude Code 2.1.316.
