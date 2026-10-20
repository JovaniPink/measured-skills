# Daily engineering trigger trial

Status: `prepared_not_run`. All 30 cases are synthetic and public-safe: two
positives per profile skill, three near misses, and three safety cases. They
measure selection separately from output quality. No model run is recorded.

## Prepare an export

Commit the source first. From a clean checkout, choose a new folder outside it
with an existing, nonsymlinked parent:

```sh
python3 scripts/export_trigger_evals.py --output /private/tmp/daily-trigger-review
```

The export contains a temporary Claude plugin, the same portable case definitions
and canonical skills for Codex, and a receipt of source revision and file/case
hashes. It does not install, authenticate, invoke a client, or publish a report.
A changed or dirty checkout, unsafe destination, unknown selection, or existing
output is rejected. Output graders in the Claude package use a judge model if
run later; tool-selection graders are deterministic. Model and judge runs both
need an agreed budget.

The exporters do not modify the separate lab. Its operator must adopt the cases
under that lab's own isolation and run contracts. Existing frozen studies remain
unchanged and are not relabeled as results for this profile.

## Two-week protocol for a separately authorized trial

1. Before day one, freeze cases, original and refined source revisions, profile,
   client/model versions, permissions, tools, and run budget. Review cases before
   exposure to results. Use equivalent inputs and fixtures for both descriptions.
2. In week one, compare the original and revised descriptions within the same
   12-skill selection and client. The new GCP skill is held constant in both arms
   and reported separately because the original 86-skill catalog did not have it.
   A no-custom-skill baseline is a separate output-quality comparison.
3. Log missed selection, wrong selection, unwanted activation, and unavailable
   listing entries separately. Inspect actual invocation arguments; a matching
   answer is not proof of loading. Keep duplicate installs out of the isolated
   treatment; do not remove ordinary user installations.
4. In week two, repeat the same cases for stability and review held-out public
   examples. Repetitions are not new independent cases. Record interrupted,
   unavailable, and failed runs rather than silently excluding them.
5. Report each client independently. Include correct-selection rate, near-miss
   false positives, safety failures, output-quality judgments, cost, and limits.
   Any authority violation prevents promotion regardless of average score.

For a future authorized Claude run, use the native plugin eval command with
`--no-publish`; select model, repetitions, tools, and spend limits explicitly.
A one-run, no-ablation iteration is debugging evidence, not a benefit result.
No trial is scheduled by this document.

Case format v1 has `id`, `kind`, `prompt`, `expected_skills`, `forbidden_skills`,
and `output_rubric`. The exporter rejects unsupported fields and inconsistent
coverage. Canonical skill names appear in expectations, not implicit prompts.

Authority: [Claude plugin evals](https://code.claude.com/docs/en/plugin-evals),
reviewed 2026-10-20. The native package format is prepared, not client-qualified.
