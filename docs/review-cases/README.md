# Review casebook

This directory collects concrete code-review examples that show how Measured
Skills separates supported findings, cleared concerns, unresolved coverage gaps,
and corrections over time.

Every record labels its evidence type explicitly. Do not mix them:

| Record | Evidence type | What it shows |
| --- | --- | --- |
| [Captured review case (2026-11-19)](captured-review-case-2026-11-19.md) | Captured read-only review against real repository revisions (`92d24711..42950f2d`) | One supported finding, one concern cleared by counter-evidence, one unresolved coverage gap, and a 5-dimension state ledger. |
| [Disconfirmation and failure cases](disconfirmation-and-failure-cases.md) | Synthetic and reconstructed teaching cases | Concrete failure mechanisms and false alarms, including authorization below the handler, Next.js cache/auth boundaries, tautological tests, and mixed-version rollouts. |
| [Preserved corrections](preserved-corrections.md) | Public historical correction records from this repository | Original claims, missing evidence, resolving observations, explicit corrections, and regression checks. |

## What this casebook does not establish

A single captured review or a set of teaching cases demonstrates the intended
review structure and judgment. It is not a controlled multi-user benchmark and
does not prove that loading a skill outperforms a structured prompt alone. See
the [3-arm review comparison kit](../../evals/review-comparison-v1/README.md) for
the controlled evaluation design.
