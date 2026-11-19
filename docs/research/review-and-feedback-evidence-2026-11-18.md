# Evidence for the review and feedback direction

Observed November 18, 2026. This note distinguishes research findings, discussion,
and our product decisions. It supports the [systems review guide](../review-systems-thinking.md)
and [feedback-loop guide](../prompt-feedback-loops.md). Research motivates testing
these workflows; it does not establish Measured Skills performance.

## The linked headline has an older study behind it

Chen and Stratton's [current working paper](https://fion.ac/jellyfish.pdf), dated
November 14, 2026, covers 655 firms and 720,542 workers through August 2026. Its
12-month agent estimates include 35.7% more pull requests, an imprecisely estimated
13.7% increase in resolved issues, and 56.1% longer submission-to-merge time. The
paper's discussion describes the issue estimate as marginally insignificant;
neither a point estimate nor failure to reject zero establishes the true effect.
The review interval is elapsed time, not reviewer labor. Adoption comparisons depend on
counterfactual-trend assumptions; the sample comprises consenting Jellyfish
clients. Review activity is not a direct shipped-defect measure. This revision
does not support a categorical claim of no increase in completed work.

The [October 13 article](https://complexdiscovery.com/harvard-researchers-find-ai-coding-agents-shifted-the-bottleneck-to-code-review/)
discusses an earlier revision. The PDF URL is mutable; recheck its date before
reusing numerical claims. Do not combine estimates from different revisions.

The supplied [Hacker News discussion](https://news.ycombinator.com/item?id=50538303)
is retained as a discovery lead. Its comments could not be retrieved in the
November 18 verification pass, so this note attributes no argument or consensus
to them. Discussion alone would not establish a representative survey, causal
estimate, or evidence of this product's benefits.

## Primary evidence and bounded conclusions

| Question | Primary source and date | What it supports and what remains limited |
| --- | --- | --- |
| Does review include understanding? | [Bacchelli and Bird, ICSE 2013](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/) | Their Microsoft study describes understanding and knowledge-sharing benefits. It is not an AI-tool trial. |
| What should a review examine? | [Google review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html), read November 18 | Design, context, complexity, and test usefulness. Organizational guidance is not a measured effect for this catalog. |
| Does self-critique always fail? | [Huang et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html); [Madaan et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html) | Intrinsic reasoning correction can degrade results; iterative self-feedback also helped on evaluated tasks. Test the actual loop instead of asserting universal failure or success. |
| Can a judge favor presentation? | [Zheng et al., MT-Bench paper, December 2023 revision](https://arxiv.org/html/2306.05685v4) | Reports position and verbosity biases and a conservative swapped-order method. Order swapping does not remove all judge error. |
| Is rubric-induced preference drift established terminology? | [Ding et al., COLM 2026 pre-proceedings](https://proceedings.colm.cc/paper_files/paper/2026/hash/9ad307ab459fb93163248a0a56959307-Abstract-Conference.html) | Demonstrates benchmark-compliant preference shifts, including adversarial rubric edits. It does not show that every ordinary rubric revision drifts. |
| Are implicit signals ground truth? | [Wang et al., ICML 2026](https://proceedings.mlr.press/v306/wang26jq.html) | Studies selection bias and absent definitive negative labels in implicit feedback. More events do not automatically mean more reliable labels. |
| Do judge scores need uncertainty? | [Lee et al., ICML 2026](https://proceedings.mlr.press/v306/lee26bl.html) | Addresses bias and uncertainty from imperfect judges and calibration data. No universal sample size follows from that result. |

## Product decisions

We keep the promise **Review the change. Understand the system.** The concrete
offer is a set of scoped requests and optional reusable guidance for preparing a
change, examining its system effects, resolving feedback, and learning from
confirmed outcomes. These artifacts are inspectable before a user copies them.

We add two distinct learning paths: bounded recovery within a task, and reviewed
changes to instructions and evaluations across versions. We retain human judgment
over requirements, important design tradeoffs, and the evaluator itself. These
are design decisions to test, not causal findings attributed to the papers above.

The supplied numerical suggestions for retry counts, feedback density, dataset
shares, sample sizes, agreement scores, non-inferiority margins, and canary limits
are not adopted as universal defaults. A policy needs its task, denominator,
risk tolerance, evidence, and owner. We found no primary basis for applying the
quoted rating or signal-density percentages to this product.

Marketing may describe the workflow and the evidence it asks users to inspect.
It may not claim that Measured Skills removes a bottleneck, reduces review time,
prevents loss of expertise, or has a research-proven return. Those require
product-specific observations with a baseline and stated limits. The website's
categorical interactions cannot measure engineering outcomes or prompt quality.

## Technical corrections to the proposed examples

The [GitHub pull-request API](https://docs.github.com/en/rest/pulls/pulls) exposes
`changed_files` as a count. Path-based calibration decisions need an actual file
list or a validated comparison, including a distinct failure state. A skipped
job is not automatically evidence that calibration was unnecessary.

The [Claude versioning documentation](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
identifies generation 4.6 dateless IDs as fixed versions. We did not verify the
proposed dated suffix. Record a provider-documented identifier and the observed
execution configuration; do not infer stability from naming shape. Fixed weights
and identical serving behavior are separate claims.

The [feedback-loop guide](../prompt-feedback-loops.md) applies these corrections
without installing an evaluation service, enabling telemetry, or creating a paid
CI job. Existing evidence and authorization boundaries remain in force.
