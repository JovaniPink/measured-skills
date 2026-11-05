# Catalog Release, Rollback, and Revocation

The catalog uses one SemVer release train. Every canonical skill, generated plugin manifest, Claude marketplace entry, ZIP filename, compatibility record, and release manifest uses the same version.

## Staged release

Select the version's source before running any generator. Merged `main` contains
0.19; it cannot rebuild the preserved 0.18 candidate by changing a command label.
Use the exact candidate and manifest source identities in [release status](release-status.md).
Keep older candidates in separate clean checkouts, preserve their anchors, and
reconcile intentional changes through ordinary commits. A merged preparation PR
does not authorize tagging or turn its old client observations into new acceptance.

1. Confirm scope, identity, branch, clean status, provenance, and the target version.
2. Regenerate client trees and marketplaces.
3. Package individual Claude.ai ZIPs twice and compare checksums.
4. Run open-spec, client adapter, schema, link, boundary, trigger, fixture, drift, and unit validations.
5. Build the release manifest from the exact tested source commit and artifact checksums. Run `python3 scripts/build_release_manifest.py --source-commit <full commit hash>` on a clean checkout whose HEAD is that commit, then commit only the manifest.
6. Set the freeze. Open and review a release PR, and merge it with a merge commit. A release decision defines what the frozen candidate is and which bytes may still change.
7. On the frozen candidate, install, upgrade, downgrade, uninstall, and reinstall every affected plugin on each claimed CLI surface.
8. Record Desktop, web, API, and command-line observations separately. Historical blocked records remain historical. Create a terminal row only after it can be recorded as `pass`, `fail`, or genuinely `not_supported`; do not use a placeholder row to imply acceptance.
9. Run the human and client gates the release decision names, and report any miss as it happened. If a behavior gate fails or does not run, remove that claim.
10. Tag only through the sequence below. Merge, tagging, public-directory submission, and publication remain separately authorized.

## Tag a release

Upstream sources move often, and tag pushes run no CI, so do these steps in one sitting.

1. Open one PR with the tag-time text, any reviewed repins, and a manifest-only commit if pins moved. Word the text to be true once the tag exists. Rebind the delta, then merge with a merge commit.
2. On that merge commit, read the hosted CI result and run the online check: `gh workflow run upstream-freshness.yml`, plus `python3 scripts/check_upstream_freshness.py --online --output <receipt>`.
3. If it passes, compare the manifest's artifact hashes with the freeze. Only `catalog/upstream-pins.json` and `catalog/upstream-reviews.json` may differ. Then tag that commit as `vX.Y.Z`.
4. If a source moved, review it individually, keep the failed receipt, and repeat from step 1. A repin moves `source_commit`; the artifact hashes are what must stay the same.

"Agree" means `python3 scripts/validate.py` passes on the commit being tagged, hosted CI passed on that same commit, and the tag equals `v` plus the catalog version. See [the 0.19.0 decision](audits/release-decision-0.19.0.md) for an example of a freeze, narrower claims, and a rollback target.

## Rollback

Reinstall the rollback target named in the release decision, verify its release manifest and checksums, then repeat discovery, implicit activation, explicit-only controls, focused-reference loading, and uninstall tests. A repository rollback does not prove already installed clients changed. The rollback target may not have accepted behavior, so state that when you use it.

## Deprecation

Record the replacement, announcement version, removal version, reason, and migration steps. Allow at least one release of notice unless immediate removal is required for security.

## Revocation

Add the skill to `catalog/revocations.json`. Generation, packaging, and marketplace advertisement must omit revoked skills. The catalog can withdraw availability but cannot forcibly delete a copy already installed on a client. Notify users through an authorized release channel and provide a replacement or explicit removal guidance.
