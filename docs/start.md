# Find your next workflow

Start with [the offline chooser](../dist/discovery/index.html) or its
[plain-text guide](../dist/discovery/guide.md). Download the HTML file and open it
locally; GitHub shows its source. It needs no server, login, network or installation.
The Studio's `/skills` page uses the same revision-pinned records when published.

**Finish existing work** is the first route. Choose the finish line you mean:

- Assess and plan: inspect current state and recommend the next repair.
- Repair and verify locally: edit the scoped change and run relevant checks.
- Maintain this draft PR: commit, push normally, update the named draft and reply
  technically to existing findings within the stated three-round/30-minute limits.

Selecting a card executes nothing. Sending the copied request grants only its
stated scope. Replace placeholders, verify the checkout, and check the installed
entry before relying on a command. A familiar response does not prove a skill loaded.

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
