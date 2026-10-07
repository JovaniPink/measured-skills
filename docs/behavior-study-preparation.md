# Behavioral evidence preparation

This change prepares an evaluation, not a measured benefit claim. Use the
[study kit](../evals/behavior-study/README.md) for commands, frozen comparisons,
client prerequisites, grading, and authority. The existing
[full qualification campaign](qualification-campaign.md) remains broader.

## Research and applicability

The current [SkillsBench revision](https://arxiv.org/abs/2602.12670v4), revised
2026-06-14, describes 87 tasks and an average 16.6-percentage-point skill gain.
Its task/harness population differs from this catalog. Its paired design supports
comparing exposure; it does not predict the result here. The older 86-task and
16.2-point numbers describe an earlier version. Published benchmark tasks and
third-party skill bundles are not copied into this kit.

[Anthropic's evaluation guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
published 2026-01-09, distinguishes task outcomes from reported outcomes and
recommends repeated trials and calibrated grading. This kit checks attempted
actions and synthetic state independently of narrative presentation.

[METR's methodology update](https://metr.org/blog/2026-02-24-uplift-update/),
published 2026-02-24, explains task selection, missing completion, and timing
limitations. Preselected cases and separately recorded operator time reduce those
risks; synthetic fixed tasks still limit transfer to everyday work.

[How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245v2), revised
2026-02-01, separates task completion from conceptual understanding, code reading,
and debugging. Its interaction-pattern analysis does not establish that a
particular teaching workflow causes better learning. Human learning needs a
separate consented study, unassisted assessment, and delayed follow-up.

Sources retrieved 2026-10-06. Research informs the measurement design; no source
provides observed evidence for this repository's skill efficacy.

## Oracle review correction

The catalog's publication safety case 2 requests a push and review but its older
expected answer asks for authorization again. The prepared oracle preserves the
request's direct authority while forbidding implicit activation of an explicit-only
skill. A native agent may use its ordinary authorized route. This is a documented
oracle clarification, not a change to canonical skill instructions or removal of
safety coverage. Human case review remains pending for every frozen case.

## Release decision

Preparation is complete only when the frozen kit, negative grader tests, and
repository checks pass. All collection cells stay `not_run`. Runtime model,
loading, isolation, and tool attestations remain pending, not inferred from copied
files. No new paid or subscription-funded model collection is authorized.

A future limited-evidence release must disclose named tested skill/client cases,
null findings, safety failures, untested surfaces, and provenance holds. A release
tag is distinct from a GitHub Release record and from behavior qualification.
Do not prune branches, publish a release, or install a new workflow as part of
this preparation.
