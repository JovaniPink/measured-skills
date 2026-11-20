# Preserved corrections

**Evidence type:** Real, public historical corrections recorded in
`JovaniPink/measured-skills` audits and git history. Preserving corrections
openly makes review judgment inspectable rather than showing success-only demos.

---

## Correction 1: Adding new eval cases directly to the shared case list shifted paid arm counts

- **Source record:** [docs/audits/review-feedback-loops-2026-11-18.md](../audits/review-feedback-loops-2026-11-18.md) (PR #101)
- **Original claim or draft action:** Adding ten new review-feedback positive
  and safety cases directly into the shared evaluation case list (`evals/cases.json`)
  was initially treated as an additive coverage expansion.
- **Missing evidence:** How `scripts/export_plugin_evals.py` selects cases for
  existing paid native evaluation arms and budgets.
- **Resolving observation:** Independent source review traced the exporter and
  found that inserting positives directly into the shared list silently altered
  the selected counts for existing paid native arms.
- **Explicit correction:** The ten supplemental cases were moved into a separate
  file (`evals/review-feedback-loops.json`) marked `status: "prepared_not_run"`
  and excluded from existing paid native arms, keeping prior study budgets intact.
- **Regression safeguard:** Existing unit tests keep the native-arm selection
  counts locked while `evals/review-feedback-loops.json` is validated separately.

---

## Correction 2: Treating ambiguous retry and copy counts as a confirmed failure

- **Source record:** [docs/audits/review-feedback-loops-2026-11-18.md](../audits/review-feedback-loops-2026-11-18.md) (PR #101)
- **Original claim or draft action:** An early draft of a feedback-loop safety
  expectation implied that rising prompt-copy counts and user regenerations
  demonstrated a confirmed failure requiring immediate remediation.
- **Missing evidence:** Competing explanations for retries and copies (exploring
  options, refining inputs, or normal multi-step iteration) and any confirmed
  defect trace.
- **Resolving observation:** Source review flagged that interaction counts alone
  are ambiguous signals and cannot establish either a productivity gain or a
  confirmed defect.
- **Explicit correction:** Updated `learn-after-launch-safety-2` in
  `evals/review-feedback-loops.json` and `skills/learn-after-launch/SKILL.md` so
  ambiguous interaction signals remain leads until disconfirming or confirming
  evidence exists.
- **Regression safeguard:** Preserved directly as safety case
  `learn-after-launch-safety-2` in `evals/review-feedback-loops.json`.

---

## Correction 3: Replacing an imperative activation sentence with third-person guidance

- **Source record:** [docs/audits/haiku-exploration-2026-11-05.md](../audits/haiku-exploration-2026-11-05.md)
- **Original claim or draft action:** Adding the imperative line `Load this skill
  first, before inspecting files, whenever the request matches.` raised core
  activation on Haiku 5.5 from 1/32 to 12/32 (full catalog) and 21/32 (nine
  skills alone).
- **Missing evidence:** Compliance with the catalog's own authoring rules
  (`skills/AGENTS.md` and `docs/authoring.md`) requiring third-person
  descriptions without indiscriminate activation commands.
- **Resolving observation:** Review caught the policy conflict. Retesting the
  compliant third-person wording (`Loads before file inspection when the request
  matches.`) produced 8/32 in the full catalog (twice) and 13/32 in the
  nine-skill subset, keeping 0/31 near-miss false activations.
- **Explicit correction:** Replaced the imperative line with the third-person
  sentence and documented the measured drop openly rather than erasing the
  earlier comparison or claiming unchanged activation.
- **Regression safeguard:** Preserved both datasets side by side in
  `docs/audits/haiku-exploration-2026-11-05.md` and `haiku-exploration-2026-11-05.json`.

---

## Template for future confirmed corrections

When a later check, test, or review disproves an earlier review claim or
guidance assumption, append a record using these exact fields:

```markdown
## Correction N: <short factual title>

- **Source record:** <PR, commit SHA, or audit link>
- **Original claim or draft action:** <preserve the exact prior statement>
- **Missing evidence:** <what had not been checked when the claim was made>
- **Resolving observation:** <exact command, file, browser check, or test>
- **Explicit correction:** <what changed and what remains uncertain>
- **Regression safeguard:** <unit test, fixture ID, or review case added>
```
