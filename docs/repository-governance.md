# Repository review controls

## Prepared configuration and observed state

On November 17, 2026, the GitHub API reported `main` as unprotected and returned
no rulesets. The passing `validate` check came from GitHub Actions app ID 15368.
The code changes include a [prepared protection payload](../.github/main-branch-protection.json).
Committing that file does not apply GitHub settings.

The GitHub integration available for this work can write branches and pull
requests but does not expose an administrative settings mutation. The browser
settings page requires an authenticated administrative session. Activation is
therefore pending; do not describe this configuration as enforced.

## Intended controls

- Require the pull-request path and the `validate` check from GitHub Actions.
- Require the candidate branch to be current with `main` before merging.
- Resolve review conversations before the normal merge path completes.
- Prevent force pushes and branch deletion.
- Permit merge commits. Linear-history enforcement would conflict with the
  source and release-manifest ancestry contract.
- Keep an explicit administrator emergency bypass. This is a deliberate policy
  exception, not a routine completion path. Record the reason and revision when
  using it, and re-evaluate the exception if administrator access expands.

The solo-maintainer setting requires zero additional human approvals. A required
second reviewer would otherwise make the normal path unusable. When another
maintainer is available, use an independent review and raise the required count
deliberately. An automated source review does not claim human approval.

## Activation with administrative access

The payload follows GitHub's
[update branch protection API](https://docs.github.com/en/rest/branches/branch-protection#update-branch-protection).
From an already authenticated GitHub CLI with Administration write access, apply:

```sh
gh api --method PUT \
  repos/JovaniPink/measured-skills/branches/main/protection \
  --input .github/main-branch-protection.json
```

Before applying, read the current protection and rulesets again. Reconcile any
concurrent policy change instead of replacing it with a stale snapshot. Read back
the protection after applying and confirm the check name, app binding, review
settings, and force-push/deletion restrictions. Record that observed result and
date before marking this activation complete.

The [pull-request template](../.github/pull_request_template.md) and
[review workflow](code-review-workflow.md) connect these controls to intended
behavior, affected consumers, evidence, and recovery. Source checks, merge
approval, release acceptance, and production deployment remain separate decisions.
