# Find your next workflow

Start with [the offline chooser](../dist/discovery/index.html) or its
[plain-text guide](../dist/discovery/guide.md). Download the HTML file and open it
locally; GitHub shows its source. It needs no server, login, network or installation.
The Studio's `/skills` page uses the same revision-pinned records when published.

## Start with the unfinished task

Choose **Finish existing work**. If you need to know where things stand, use
**Find out what remains - no edits**, which is already expanded in the chooser.
You only need the repository and the task or PR. You do not need to know the
branch, comparison revision, skill name, or plan filename: the assistant discovers
those from the project and asks if it cannot identify the target safely.

For example, a fictional half-finished PR might produce: "The API repair is
present; the browser recovery path is unverified. Next, inspect that path before
choosing a repair." That is an assessment, not a claim that the feature works.

Choose another finish line only when you want it:

| Choice | What you receive | What it permits |
| --- | --- | --- |
| Find out what remains - no edits | Done, unfinished, uncertain and blocked work, with evidence and one next step | Inspection of existing evidence; no edits or test runs |
| Finish a local repair - no push | A scoped repair, relevant check results and remaining gaps | Local edits and checks; no commits or external writes |
| Update this draft PR - no merge | Scoped commits, draft updates and an exact-revision handoff | Ordinary pushes and technical replies to existing findings on the named PR, within three review rounds and 30 minutes of cumulative waiting |

Select your client and leave **Ordinary request** selected unless you have verified
the installed skill entry. Copy the request, replace its placeholders, and send it
to your assistant. The chooser does not run anything. The request's scope takes
effect when you send it; preserve any narrower constraints you already set.

You can stop after the assessment. If you choose repair, use its identified next
step as context; do not restart a planning exercise for an already clear change.
Local repair uses local checks. Provider-backed checks, production access and
additional model calls need separate authorization for the task. If those checks
are unavailable, keep the gap visible and continue the authorized local work.
A familiar response does not prove that a skill loaded or that work is complete.

## Use the guide with the skills you actually have

The chooser describes the 0.19 preview, not your installed inventory. If your
client still has 0.18, a 0.19 command can be missing even though its older capability
exists. Check the [name and pack migration](migration-0.19.md); do not combine an
old pack name with a new skill name or install an alias to make a prompt work.

Before sending a Codex or Claude Code prompt, select the exact installed entry.
The interactive chooser defaults to **Ordinary request**, which works without
selecting a skill. Choose **Verified installed skill** only after checking its
source; the resulting prompt includes the native command. The text-only guide
also gives ordinary requests and identifies the optional native entry. Neither
request style proves that a skill loaded.

If you use another example whose entry is missing or ambiguous, remove its leading
`$pack:skill` or `/pack:skill` token before sending the ordinary request. Say that
skill loading is unverified. The fallback sentence inside a prompt cannot make a
client accept an unknown native command. Preserve the same scope and finish line.

The core profile supplies assessment, diagnosis, review, and verification. It
does not include `execute-plan` or `publish-change`. The action card identifies
those additional entries. Antigravity prompts request authorized work in ordinary
language without invoking its excluded explicit-only workflows. None of these
steps requires changing your installation to read or use a request.

Replace placeholders and carry forward your actual constraints. For example,
if checks must not be rerun, replace a copied instruction to run checks with
"Inspect existing check evidence and source only; do not rerun tests. Report the
untested scope." A generic repair prompt must not override that constraint.

The **0.19.0 preview** has 90 skills in four distribution packs. Start with the
nine-skill `finish-work-core` profile, adding a stack only when needed. Do not
activate all packs merely to find one task. The preserved 0.18 candidate has its
own acceptance and release work; 0.19 inherits none of those observations as a pass.

Use [the migration guide](migration-0.19.md) before any later installation change.
For deeper help, see [finish existing work](finish-existing-work.md),
[feature development](feature-development-workflow.md), and
[the complete catalog](skill-catalog-reader-guide.md). The chooser is the single
beginner entry point; these documents explain a selected route in more depth.

[Acceptance exercises](acceptance-0.19.md) are prepared, not completed.
[Merged status and remaining gates](release-status.md) separate source delivery
from installation, release, and website publication.
[Source and research decisions](audits/discovery-0.19.md) distinguish facts from proposals.

For upgrades, refactoring, queries, replay and Swift diagnosis, search the chooser.
[Workflow depth and evidence limits](workflow-depth-0.19.md) explains these routes.
