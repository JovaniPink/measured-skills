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
| Add one sentence to the nine core descriptions | Activation in the full catalog went from 1 of 32 to 12 of 32, with 0 of 31 near-miss fires | Haiku only. `diagnose-failure` and `plan-change` stayed at 0 of 11 |
| Restate four trial-shaped lines in general terms | Review finding, not a model result | The meaning is intended to be unchanged |

The added sentence moves `measured-workflows` to 6,275 description characters,
past the 6,000 warning line and under the 8,000 limit.

## What we learned

**The prompt carried the result.** Long and short requests were compared on a
half-finished change with planted traps. Blocked runs are excluded below.

| Trap reported | Long request (54 runs) | Short request (55 runs) |
| --- | --- | --- |
| Unrelated commit mixed into the branch | 54 | 8 |
| Work hidden in a stash | 18 | 0 |
| Embedded instruction refused | 54 | 45 |
| CI receipt bound to an older commit | 48 | 49 |
| Requirement dropped from the replacement plan | 54 | 55 |
| Plan item ticked but not implemented | 54 | 55 |
| Skipped test | 54 | 55 |

**Loading `plan-change` showed no measured benefit on this task.** With the long
request, the skill arm found the stale receipt in 17 of 18 runs and the stash in
6 of 18. The two no-skill arms found them in 31 of 36 and 12 of 36. Two identical
no-skill arms differed by about as much as skill and no skill did. This fixture
may be too easy for Haiku 5.5, and it says nothing about other skills or models.

**Ordinary requests rarely load core skills.** Haiku tends to start working
instead. Specialist skills activated more often, at 17 of 64. Near-miss precision
was high: 0 of 73 fired their own skill, while 10 of 73 fired some other skill.
A canary line proved that the slash command loads the body and that the same
ordinary request does not.

**Boundaries held in every arm.** All 120 comparison runs had no edit attempts,
no test-run attempts, and no changed files. Both requests told the model not to
act, and the no-skill arms held too, so this is not credit for a skill.

**A long listing can overflow.** At a forced 8,000 character listing the client
warned `90 skills, 24349 chars > 8000 budget`. Haiku 5.5 reported a 1,000,000
token context here, and no warning appeared at the default. Forced overflow did
not reduce routing in this test: 20 of 64 specialists against 17 of 64. Models
with a smaller context may behave differently. We did not measure them.

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
  reasoning around it is sound. We read samples, not every output.
- A run counts as completed if its report mentions the jitter gap. About 9 percent
  of runs were blocked: Haiku tried a compound shell command, was denied, and
  reported it could not inspect the repository. This is our harness, though it
  is also a useful failure mode.
- Evaluation prompts were written by this project, so routing rates are not
  a sample of real requests. The added description sentence was tuned and checked
  on the same cases. Expect some regression on new prompts.
- Repeated runs measure stability on one fixture, not independent tasks.
- Usage-credit controls were not inspected. The $3.85 figure is a list-price
  estimate reported by the client, not a bill.

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
a native no-plugin baseline. This catalog does not use it yet.
