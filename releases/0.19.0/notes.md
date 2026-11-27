# Measured Skills 0.19.0

Choose one of 22 tasks, set its scope, and copy a request into an assistant
that can read your project. Start with [the workflow guide](../../docs/start.md)
or download [the offline chooser](../../dist/discovery/index.html). For a code
review, you can prepare a change, inspect a diff, or assess review feedback.

## Optional CLI packs

The four packs contain 91 skills on Codex CLI and Claude Code. Antigravity CLI
includes 74 skills and excludes the 17 workflows that require explicit selection.
We verified install, upgrade, downgrade, uninstall and reinstall on all three
CLIs. Follow the [client instructions](../../docs/client-support.md) to select
tag `v0.19.0`. If you have an older installation, use the
[migration guide](../../docs/migration-0.19.md) to map the old names.
The rehearsed rollback target is `v0.16.0`.

Human chooser usability and productivity are unmeasured. A packaging check
does not establish model behavior. Desktop and web apps and API use have their
own qualification requirements. The 17 explicit-only account-upload ZIPs stay
on hold. See the [release decision](../../docs/audits/release-decision-0.19.0.md)
and [artifact hashes](manifest.json).
