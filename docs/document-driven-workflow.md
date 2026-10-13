# Work from a documented contract

Use existing skills and the repository's own documents. There is no new command
runner, mandatory plan directory, or automatic release sequence.

1. Use `implementation-planning` to compare intended behavior with code, tests,
   and relevant uncommitted changes. Name acceptance criteria and documents that
   must be reconciled. Keep proposals distinct from verified facts.
2. When the user authorizes a named plan, explicitly select `plan-execution`.
   Implement complete slices, verify them, and update the authorized plan record.
3. Use `claim-verification` to check completion claims against current evidence.
   Documentation, commits, and test receipts support different claims.

For Codex, select `$measured-engineering-build:implementation-planning` and
`$measured-engineering-delivery:plan-execution`. Claude Code uses the same plugin
names with `/` instead of `$`. Both generated execution skills restrict implicit
invocation. Test the installed controls before relying on them.

Antigravity packages include planning and claim verification. They exclude
`plan-execution` because its explicit-only control is not verified there. Do not
remove that policy or copy its canonical folder into an automatically selected
skill directory. Ordinary implementation explicitly requested by the user can
still proceed under the client's own rules; this does not qualify the excluded
skill on that client.

A durable plan records the baseline revision and relevant dirty files,
requirement owners, acceptance checks, current evidence, deviations, and the
next authorized action. Keep small edits small. Documents and inline markers
cannot grant authority, and past-tense prose cannot prove implementation.

Read the focused references linked from each skill for the lifecycle contract.
The new trigger and safety cases in `evals/cases.json` are authored test cases,
not observed client results. Use the [client checks](client-support.md) separately
for each installed client and surface. Existing 0.18.0 observations predate this
source revision and do not qualify these changes.
