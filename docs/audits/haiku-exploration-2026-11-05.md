# November 5 Haiku exploration

This is an exploratory owner observation of Claude Haiku 5.5 in Claude Code
2.1.316. It tested one model, one client, and one synthetic task. It does not
qualify a client, score human usefulness, or extend maintainer acceptance. The
behavior study cells stay `not_run`. Aggregates are in
[the data file](haiku-exploration-2026-11-05.json).

## What we changed because of it

| Change | Measured reason | Limit |
| --- | --- | --- |
| Name uncommitted work and stashes in the assess prompt | Stash found in 18 of 54 completed runs before, 19 of 19 after, and 12 of 12 with the generated chooser prompt | One fixture |
| Add one third-person sentence to the nine core descriptions | Activation in the full catalog went from 1 of 32 to 8 of 32 in each of two runs. No near-miss case fired its own skill (0 of 31, twice) | Haiku only. `diagnose-failure` and `plan-change` stayed at 0 of 11. The gain did not hold under a forced 8,000 character listing |
| Restate four trial-shaped lines in general terms | Review finding, not a model result | The meaning is intended to be unchanged |

The sentence moves `measured-workflows` to 6,137 description characters, past
the 6,000 warning line and under the 8,000 limit.

The first version was an imperative: `Load this skill first, before inspecting
files, whenever the request matches.` The [authoring guide](../authoring.md#task-focused-refinement)
and [skill guidance](../../skills/AGENTS.md) ask for third-person descriptions and
no indiscriminate activation commands, so it was replaced after review. Results
below that mention 12 of 32 or 21 of 32 describe that first version. See the
[retest](#third-person-retest).

## What we learned

**The prompt carried the result.** Long and short requests were compared on a
half-finished change with planted traps. Blocked runs are excluded below. Length
itself was not varied. These are two specific requests, and the long one names
`unrelated work` as a category.

| Trap reported | Long request (54 runs) | Short request (55 runs) |
| --- | --- | --- |
| Unrelated commit mixed into the branch | 54 | 8 |
| Work hidden in a stash | 18 | 0 |
| Embedded instruction refused | 54 | 45 |
| CI receipt bound to an older commit | 48 | 49 |
| Requirement dropped from the replacement plan | 54 | 55 |
| Plan item ticked but not implemented | 54 | 55 |
| Skipped test | 54 | 55 |

The last three rows do not separate the requests. The dropped requirement and
skipped test are single-word matches. The jitter row is how a completed run is
defined, so it is 100 percent by construction.

**Loading `plan-change` showed no measured benefit on this task.** With the long
request, the skill arm found the stale receipt in 17 of 18 runs and the stash in
6 of 18. The two no-skill arms found them in 31 of 36 and 12 of 36. The second
no-skill arm came from the empty-plugin runs, so each request carried an unresolved
`/core:plan-change` prefix. That makes it a near repeat, not an identical one. The
two arms still differed by about as much as skill and no skill did. The skill arm
did not record loading per run. A separate canary showed that the slash command
loads the body. This fixture may be too easy for Haiku 5.5, and it says nothing
about other skills or models.

**Ordinary requests rarely load core skills.** Haiku tends to start working
instead. Specialist skills activated more often, at 17 of 64. Near-miss precision
was high: 0 of 73 fired their own skill, while 10 of 73 fired some other skill.
After the change, 0 of 31 core near-miss cases fired their own skill and 3 fired
another core skill. All three requests fit that skill better: for example, running
lint and tests loaded `run-project-checks`. Only 9 of those 31 cases were in the
earlier sample, so this is not a before-and-after comparison.
A canary line proved that the slash command loads the body and that the same
ordinary request does not.

**The catalog size and the run both moved activation.** With the added sentence,
the nine core skills alone reached 21 of 32, against 12 of 32 in the full catalog.
No positive case loaded the wrong skill. The same sentence ran twice in the full
catalog: both runs scored 12 of 32, but only 10 cases hit in both. Read the total
as a rough level, not a stable per-skill rate. A smaller installed set may route
better, which is worth testing before choosing a default install.

**Boundaries held in every arm.** All 120 comparison runs had no edit attempts,
no test-run attempts, and no changed files. Both requests told the model not to
act, and the no-skill arms held too, so this is not credit for a skill.

**A long listing can overflow.** At a forced 8,000 character listing the client
warned `90 skills, 24349 chars > 8000 budget`. Haiku 5.5 reported a 1,000,000
token context here, and no warning appeared at the default. Forced overflow did
not reduce routing in this test: 20 of 64 specialists against 17 of 64. Models
with a smaller context may behave differently. We did not measure them.
This test used the descriptions from before the change. The added sentence was not
rerun under overflow or on the 64 specialist cases. The [retest](#third-person-retest)
covers both for the third-person sentence.

## Third-person retest

The maintainer approved a second run with a $3 ceiling. It tested `Loads before file
inspection when the request matches.` with the same harness, cases, model, and
client version. The tested Claude packs are byte-identical to the generated ones.

| Measure | No sentence | Imperative | Third person |
| --- | --- | --- | --- |
| Core cases, full catalog | 1 of 32 | 12 of 32, twice | 8 of 32, twice |
| Core near-miss firing its own skill | 0 of 9 | 0 of 31, twice | 0 of 31, twice |
| Core cases, nine skills alone | 3 of 32 | 21 of 32 | 13 of 32 |
| Specialist cases, full catalog | 17 of 64 | Not run | 32 of 64 |
| Core cases, 8,000 character listing | 0 of 32 | Not run | 1 of 32 |
| Specialist cases, 8,000 character listing | 20 of 64 | Not run | 18 of 64 |

**The imperative activated more often.** The third-person sentence gave up about a
third of the gain and kept the rest. It was steadier across its two runs, with 7
hits in common, and it is 23 characters shorter on each skill.

**No specialist displacement appeared, and the rise is unexplained.** Specialist
activation rose instead of falling: 18 cases hit only in the retest and 3 only in
the earlier run. Only the nine core descriptions changed, so this sentence is
unlikely to be the whole cause. The earlier baseline may simply have been low. Do
not cite 32 of 64 as a gain. In the wider set of 210 specialist cases, 7 loaded
the wrong skill, and 5 of those were stack prompts that loaded
`run-project-checks`. Those prompts ask to select project gates, so the fit is
arguable, and there is no earlier result for them.

**Overflow removes the gain.** At a forced 8,000 character listing, core activation
fell from 8 of 32 to 1 of 32, and specialists fell from 32 of 64 to 18 of 64. This
replaces the earlier reading that overflow did not reduce routing. If a client gives
the listing less room, this sentence should not be expected to help.

This run cost $2.64 at list price. A full pass had 472 cases rather than the sampled
169, so the second pass was stopped early and narrowed to the 63 core cases. The
nine-skill arm then ran once. Usage-credit controls were again not inspected. The
base URL was the first-party address, and authentication was first-party.

## Method

Each run started a separate client process with no user settings, no MCP servers,
a fresh copy of the task, and a cost ceiling. The nine-skill arms used the
`finish-work-core` export. Full-catalog arms used the generated Claude packs,
plus 22 skills built into the client.

Routing cases came from `evals/cases.json`. Each ran once at medium effort, with
every positive case for the nine core skills and the first positive case for
every other implicit skill. A hit means the expected skill loaded within four turns.

The outcome fixture is a small Python retry feature on a synthetic branch. Only
read tools and read-only `git` commands were allowed. Any edit or test run would
be denied and logged. The long request is the chooser's assess prompt. The short
request has 34 words: find what remains, report evidence and one next step,
inspect only, and run no tests. Each cell ran 10 times at each of medium and low
effort. Effort made no clear difference.

## Limits and errors

- Graders are deterministic text patterns. Finding a word does not prove the
  reasoning around it is sound. We read samples, not every output. A later review
  rechecked the raw outputs for the two main results. All 31 completed runs with
  the stash wording quoted the stash contents, and all 54 completed long-request
  runs placed the billing change with unrelated work.
- A run counts as completed if its report mentions the jitter gap. About 9 percent
  of runs were blocked: Haiku tried a compound shell command, was denied, and
  reported it could not inspect the repository. This is our harness, though it
  is also a useful failure mode.
- Evaluation prompts were written by this project, so routing rates are not
  a sample of real requests. The added description sentence was tuned and checked
  on the same cases. Expect some regression on new prompts.
- Repeated runs measure stability on one fixture, not independent tasks.
- Usage-credit controls were not inspected. The $3.85 and $2.64 figures are list-price
  estimates reported by the client, not bills. The maintainer allowed Haiku
  testing in the task request, but this run did not repeat the account check that
  earlier bounded client tasks required.
- Raw runs and the harness are not in this repository, because evaluation guidance
  keeps raw traces out. They are retained locally by the maintainer, so outside
  readers cannot rerun this harness. The later
  [native eval suite](../../evals/plugin-eval/README.md) is a public rerun path for
  routing, but its results do not compare with these.

Four harness errors were caught and their results excluded: a one-turn limit that
measured first actions instead of routing, a copy step that produced an empty
nine-skill plugin, a pilot whose skill arm never loaded, and a pilot fixture too
easy to separate the arms. The empty-plugin runs were kept only as no-skill repeats
for the noise estimate.

## Current guidance reviewed

Anthropic's [Haiku 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
warns that low effort can skip checks or stop early. Its
[skill authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
asks authors to test each intended model. The
[Claude Code skills guide](https://code.claude.com/docs/en/skills) describes the
listing budget. The [evaluation guide](https://agentskills.io/skill-creation/evaluating-skills)
recommends comparing runs with and without a skill. `claude plugin eval` now offers
a native no-plugin baseline. This catalog added a suite for it after this record.
