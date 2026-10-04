# Security Policy

## Which version is supported

Only the latest tagged release is supported. That is `v0.16.0`, the only tag so far. The 0.18.0 candidate has no tag yet, so for it, name the commit you ran.

Report issues against that tag, and name the tag you used. If you are running the default branch instead, say so. The branch moves, so your copy may not match anyone else's.

## How to report a problem

Do not open a public issue that contains any of these:

- credentials
- private repository names
- customer data
- internal infrastructure identifiers
- working exploit steps

Contact the repository owner privately instead. The security-reporting channel is listed on their public profile.

In your report, name the skill or script, the revision, and the client you used. Say what you saw, what it affects, and the smallest safe way to reproduce it. Take out live secrets and personal data first.

## What this catalog ships

The catalog ships instructions and reference notes. It ships no skill-level programs, hooks, MCP servers, install scripts, output styles, or broad tool grants.

Output styles matter here. A plugin is allowed to ship one that applies as soon as the plugin is enabled, which replaces your own setting for every later reply without asking. This catalog ships none. Each pack contains a `skills` folder and nothing else.

This matters because a skill you install can shape every later task. Keeping it to text means you can read the whole thing before you trust it.

Packaging scripts work offline. The upstream freshness checker can make network requests when explicitly run with `--online`; workflow validation uses the reviewed CI dependencies. Text-only skills do not prevent the host's tools from reaching the network. Sandbox, permissions, and explicit authority remain the enforcement boundary.

A skill can recommend an action. Your client's permissions and your own approval decide whether it happens. A skill cannot grant itself a tool or a permission.

Read the [security model](docs/security-model.md) for the threat model and the review criteria.
