# Review systems and prompt feedback refinement

This continuation starts from PR #100 head
`c40f1e05817c96e325bc5fea183fd57d911f91b5`. The maintainer requested a stronger
code-review and systems-thinking direction, including distinct runtime and
offline feedback loops. It remains a 0.19.0 preview with 90 skills and 21 chooser
tasks. It adds no executable evaluation service, telemetry, paid runs, installation,
release, or publication.

## What changes

| Existing capability | Deliberate refinement |
| --- | --- |
| `request-review` | Explain why the change belongs, what the maintaining owner must understand, and which decisions require that owner's judgment. |
| `review-code-change` | Examine prompt, rubric, tool, and runtime-loop changes; preserve critical contracts, counter-evidence, and earlier no-progress stopping. Isolated critique remains subject to correlated errors. |
| `assess-change-impact` | Trace receiving queues, review capacity, rework, knowledge ownership, and feedback delay as well as runtime consumers. |
| `design-agent-evaluations` | Distinguish runtime recovery and offline improvement; link input versions; calibrate changed graders independently; retain uncertainty and privacy limits. |
| `learn-after-launch` | Separate generated activity from accepted work and user outcomes; promote confirmed failures into reviewed cases without automatically weakening the rubric. |

The evaluation skill's description and native default prompt now include prompt
and judge drift. Ten additional [prepared trigger and safety cases](../../evals/review-feedback-loops.json)
cover the new questions and failure conditions. They are a supplemental lane,
outside the existing paid native arms, whose case selections and budgets remain
unchanged. The affected output rubrics in `evals/cases.json` also describe the new
expectations. Existing cases, baseline limits, invocation policy, risk classes,
and historical evidence remain. Prepared entries are not native-model observations.

The [systems guide](../review-systems-thinking.md) explains where review fits in
delivery and how to measure its constraints. The [feedback guide](../prompt-feedback-loops.md)
provides a diagnostic example, version contract, evaluation funnel, calibration
and sampling decisions, and a corrected CI design. The [research note](../research/review-and-feedback-evidence-2026-11-18.md)
records source dates and limitations, including the newer working-paper revision.
Entry-point docs and the PR template link this practice to ordinary review work.

## Evidence and implementation decisions

The supplied research and framework identify questions to investigate. The new
prose and synthetic scenarios are independently authored for this catalog. No
third-party skill implementation, raw customer trace, private code, or distinctive
external example is imported. Primary research is summarized in the dated note;
it is not a license to reuse implementations or a product-effectiveness claim.

We adopt bounded loops, actionable diagnostics, version records, calibrated
graders, and representative regression evidence. We qualify self-critique and
position-swapping claims, distinguish rubric staleness from rubric changes, and
decline unsupported universal numerical defaults. The GitHub changed-file count
and unverified model suffix are corrected in guidance. No placeholder workflow is
presented as a working CI gate.

## Verification and limits

Canonical and generated content must pass the existing syntax, typing, lint,
distribution, packaging, validation, and regression checks. The manifest is
refreshed from a clean committed source and kept in its own commit. Discovery
exports identify their committed inputs; the companion website pins the export
containing these guides. Preserve those ancestors with a merge commit.

Independent source review found that adding positives directly to the shared
case list changed the selected native-arm counts. The new cases were placed in
the explicit supplemental lane, preserving the existing study design. Review
also corrected an expectation that could demand a confirmed failure from
ambiguous interaction counts, and made CI guidance account for truncated file
lists. A separate fresh-context desk exercise identified the supplied evaluator
and retry flaws; it did not load an installed client or execute a model benchmark.

The PR records exact-revision local and hosted results. Source review and prepared
scenarios do not establish native
loading, judge reliability, faster review, preserved expertise, human usability,
or production outcomes. Earlier acceptance and source-review dates remain
historical, with no implied new maintainer acceptance or replacement freeze.
