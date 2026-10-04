# Finding Vocabulary

Use this vocabulary when a skill reports findings. It gives every review the same severity words and the same way to say whether a change introduced a problem.

## Why this exists

The catalog has 31 skills in the `review` capability family, and they do not all return the same shape of output. Fourteen skills return a list of findings: nine in the review family and five outside it. Thirteen return a gate or a verdict instead, including all 11 stack profiles. Four return an assessment or a record. This vocabulary applies to the 14 that return findings.

Overlap among them is deliberate: every skill declares `composes_with`, 27 declare `conflicts_with`, and 11 route to a named sibling in their own instructions. A motion review can hand work to accessibility, performance, and authority reviews in one pass.

Four skill bodies use the word `severity` for their own findings, and none of them defines a scale: `code-change-review`, `agentic-system-security-review`, `skill-security-review`, and `retrieval-grounding-quality-review`. Nine more use `blocking` or `blocker`, and the 11 stack profiles use `hazards` for a different idea entirely. So `code-change-review` asks for findings "ordered by severity" against a scale that does not exist, and two skills reviewing the same code produce findings a reader cannot rank against each other.

That is an evidence problem, not a formatting problem. A duplicate finding counted twice overstates how much is wrong.

## Severity

Use these four words, ordered from least to most severe. They come from the Static Analysis Results Interchange Format (SARIF), an OASIS standard for exchanging analysis results between tools.

| Severity | Use it when |
| --- | --- |
| `none` | The finding carries no judgment. It records something the reader asked about. |
| `note` | The reader may want to act, and nothing breaks if they do not. |
| `warning` | Something is wrong and the reader should decide. It does not block on its own. |
| `error` | Something is wrong enough to stop the reviewed action until it is resolved. |

Two rules keep the scale honest:

- Severity describes the finding, not the reviewer's confidence. Say what the evidence supports separately.
- A skill may not invent a fifth severity. If a finding does not fit, say why in the finding itself.

The word is `severity`, not `level`. Two skills already use "level" for WCAG conformance levels, and one output should not carry two meanings of the same word.

## Finding state

State whether the reviewed change caused the problem. These four words also come from SARIF, where they describe a result against a prior run. Here they describe a finding against the state of the artifact before the reviewed change.

| State | Meaning in a review |
| --- | --- |
| `new` | The reviewed change introduced this. |
| `unchanged` | The problem predates the change and the change did not touch it. |
| `updated` | The problem predates the change, and the change altered the affected code. |
| `absent` | The problem was present before the change and the change removed it. |

Finding state applies only when the review pins a before and an after. A skill that reviews a system, a package, or a corpus with no change under review reports severity alone and says so. Do not assign a state you cannot support.

When a change is pinned, every finding needs a state. Reporting an existing problem as if the change caused it is the error this prevents, and it is the same class of mistake as reporting a proposal as a ratified decision.

A changed line is not automatically the cause. An unchanged line can still be affected. Decide the state from what the evidence shows, not from whether the line appears in the diff.

## Ownership

One root cause is one finding, owned by one skill.

When two skills would report the same cause, the skill that owns the underlying rule reports it. Another skill may name the effect it observed and point to the owner. Do not report the same cause once per skill, and do not report it once per location: list the locations inside the single finding.

## Volume

Rank findings by reader impact and report the most severe first. When a review would return more findings than a reader can act on, report the top ones and state how many were left out and where. A silent cut is a false clean result.

## What this does not adopt

SARIF is a JSON exchange format for analysis tools. This catalog produces prose reviews written by agents for people to read. Only the vocabulary and the distinctions transfer.

Skills do not emit SARIF documents, do not compute fingerprints, and do not carry rule identifiers or numeric ranks. A skill that later needs machine-readable output should treat that as its own decision with its own review.

## Known gap

One partial rule already exists. `skills/multi-agent-orchestration/references/coverage-fanout.md` requires findings to carry location, scenario, evidence, severity, and uncertainty, and tells the integration owner to deduplicate overlapping findings and reconcile conflicting conclusions against the artifact. It binds only inside one explicitly invoked orchestration run, and it names severity without defining it.

Nothing covers the ordinary case: several reviews invoked separately, each returning its own list, with no step that merges them. `cross-stack-quality-gates` consolidates gate results, which are command outcomes rather than findings.

This vocabulary had to exist first, because findings cannot be merged or ranked until they are comparable.

## Adoption

Adoption is partial and tracked here. A skill released before this vocabulary keeps its own wording until it is revised.

| Skill | Adopted |
| --- | --- |
| `code-change-review` | Yes, 0.15.0 |
| `accessibility-review` | Yes, 0.15.0 |
| `application-security-review` | Yes, 0.15.0 |
| `api-contract-compatibility-review` | Yes, 0.15.0 |
| `dependency-supply-chain-review` | Yes, 0.15.0 |
| `test-quality-review` | Yes, 0.15.0 |
| `skill-security-review` | Yes, 0.15.0 |
| `functional-motion-review` | Deferred |
| `agentic-system-security-review` | No |
| `retrieval-grounding-quality-review` | No |
| `agent-tool-action-boundary-review` | No |
| `agent-protocol-interoperability-review` | No |
| `source-output-conformance-audit` | No |
| `public-private-boundary-review` | Exempt |

`public-private-boundary-review` is exempt. Its `BLOCK`, `REVIEW`, and `CLEAR` values state what the reader must do about the artifact, not how bad a finding is. They are defined in its own body and they are the publication gate's whole interface, so converting them would lose information rather than add it.

These skills do not report findings and are out of scope: the 11 stack profiles, whose `Hazards` are conditions to avoid before running a gate and whose `Results` are command outcomes; the readiness reviews, where a go or no-go verdict is already the aggregate; and the assessment skills, which return a cause, a blast radius, or a record rather than a ranked list.

## Sources

Severity and finding-state vocabulary follow [SARIF Version 2.1.0 Plus Errata 01](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html), 28 August 2023, read 2026-09-10. Its `level` property defines the four severity values as ordered from least to most severe. Its `baselineState` property defines the four finding states against a baseline run.

This catalog narrows both. It reuses the four state words against the pre-change state of the reviewed artifact, which is narrower than a run-to-run comparison. It uses "severity" rather than SARIF's "level" because two skills already use "level" for WCAG conformance levels.
