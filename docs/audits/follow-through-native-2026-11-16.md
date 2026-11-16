# Follow-through native checks - November 16, 2026

These checks support technical merge preparation for the follow-through candidate.
They do not qualify a public release, a different model, autonomous execution, or
the ten ordinary-task observation. The human chooser exercise remains unscored and
is separate from this source PR's merge preparation.

## Candidate and clients

Tested source: `ad3028c28795d82ed3d966c4df2c298cf4d48b8f`. Artifact source:
`b54131f9d0f40dd013d61c66a6292d8cf1b5ecfc`. Only `measured-quality` and
`measured-workflows` changed in this candidate. No skill or package bytes changed
during the native checks; later evidence/protocol edits do not change those bytes.

| Client | Version | Model evidence | Exposure |
| --- | --- | --- | --- |
| Codex CLI | 0.167.0 | Requested `gpt-6-astra`, xhigh; served identifier not exposed | Native cached plugins; read-only shell read six entries and three continuity references |
| Claude Code CLI | 2.1.316 | Existing default reported `claude-opus-5-5` | Native inline plugins, Skill calls and slash-command expansion; Read access to linked references |

The earlier explicit-text smoke reported Sonnet for Claude. This fresh invocation
used the existing default and reported Opus; no model argument selected a substitute.
These are separate observations, not a controlled model comparison.

## Package lifecycle

Both clients completed install, upgrade from the legacy `v0.16.0` packages, downgrade
to that rollback target, uninstall, and candidate reinstall. All 99 recorded commands
exited successfully. Native enabled inventories and SHA-256 comparisons matched the
source files at each checkpoint; Claude's effective read-from-folder also matched.

These are explicit disable/install/remove migration paths across renamed packages,
not automatic in-place updates. Disposable client configuration directories kept
the active installations out of the lifecycle. Final disposable inventories were
empty, and fresh Codex discovery found no candidate plugin after removal. Raw command
receipts and full synthetic outputs are retained privately, outside the public repo.

## Initial native observations - retained

Codex read all six selected cached entries and the three continuity references. Claude
loaded `verify-claims`, `review-context-evidence`, and `review-engineering-prompt`
through Skill, but falsely reported the other three entries as not installed. The
session initialization listed them. They are explicit-only commands, not callable
through the model-visible Skill tool. This failed attribution remains a finding.

Corrected native slash requests separately exercised `execute-plan`, `handoff-work`,
and `coordinate-agents`. Each read its linked continuity or client-mapping reference.
Their decisions preserved the user pause, pending cost decision, current target,
superseded choice, review coverage, and parent integration obligation. These runs
used inline-plugin loading and do not replace the separate installed-cache evidence.

Independent grading found correct central decisions in the initial twelve-case
bundles, but also incomplete rubric criteria. Neither bundle is a clean 12/12 pass:

| Case | Incomplete expectation |
| --- | --- |
| context-failure | Both clients omitted preserving completed work and refreshing only facts needed next. |
| rejected-option-failure | Claude did not explicitly restrict independent work to already-authorized work. |

The independent grader initially also marked decision-history and review-findings
retention incomplete. Semantic re-review corrected those two grades: the answers
retained the supplied earlier decision, review approval and open acceptance. The
cases supply no other defect findings, and a literal field label is not required.
These were grading errors, not established model failures.

The harness requested only four fields with a 65-word case cap, although the rubric
grades a fuller continuation record. The corrected protocol removes that cap and
requests the complete record. It changes neither case prompts nor expected criteria,
and exposes no answer keys. The initial misses are preserved; this is a harness
correction, not evidence that unchanged skill text improved.

## Focused rerun

Three Codex cases and four Claude cases were selected from the initially flagged cases above.
Independent semantic review passed all three Codex cases and three of four Claude
cases. Claude's context case still prescribed broad revalidation of D-bound checks
without first establishing which receipts could apply to O. Its minimal-refresh
expectation remains incomplete. No authority reversal or unsupported whole-task
completion appeared. No further retries were made to obtain a passing label.

The expanded Codex answer was 3,236 whitespace-separated words. Loading six output
contracts together caused substantial ceremony in this test. This is a harness
limitation, not a normal workflow recommendation or measured performance regression.
For ordinary use and future behavior checks, select only the guidance needed for
the case; do not make the load-inventory exercise a compulsory skill chain.

Independent disposition: APPROVE WITH LIMITS for technical candidate merge
preparation. Native loading and lifecycle are evidenced. A universal behavioral
pass is not claimed; the remaining Claude observation stays visible for ordinary
work follow-up. No changed skill bytes or broad new rules are justified by these
bounded observations alone.

## Controls and limits

Only existing first-party subscription authentication was used. No API/proxy fallback,
login, account switch, billing toggle, model substitution, or permanent plugin update
was performed. No hypothetical case action ran. Claude had only Read and Skill tools
with empty MCP; built-in plugins remained visible. Codex used a read-only sandbox and
disabled apps, hooks and subagents; host-skill-discovery suppression is experimental,
not an isolation guarantee. No absolute absence of ambient context is claimed.

Native loading and correct bounded decisions are different from completing a real
repair, recovering from actual compaction, or demonstrating reliable field behavior.
The next ten eligible ordinary tasks remain unobserved. Historical release gates and
human results were not rewritten, waived, or inferred from these technical checks.
