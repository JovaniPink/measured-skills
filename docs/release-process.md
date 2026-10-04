# Catalog Release, Rollback, and Revocation

The catalog uses one SemVer release train. Every canonical skill, generated plugin manifest, Claude marketplace entry, ZIP filename, compatibility record, and release manifest uses the same version.

## Staged release

1. Confirm scope, identity, branch, clean status, provenance, and the target version.
2. Regenerate client trees and marketplaces.
3. Package individual Claude.ai ZIPs twice and compare checksums.
4. Run open-spec, client adapter, schema, link, boundary, trigger, fixture, drift, and unit validations.
5. Install, upgrade, downgrade, uninstall, and reinstall every affected plugin on each supported CLI surface.
6. Record Desktop, web, API, and command-line observations separately. Historical blocked records remain historical. Create a terminal row only after it can be recorded as `pass`, `fail`, or genuinely `not_supported`; do not use a placeholder row to imply acceptance.
7. Build the release manifest from the exact tested source commit and artifact checksums. Run `python3 scripts/build_release_manifest.py --source-commit <full commit hash>` on a clean checkout whose HEAD is that commit, then commit only the manifest.
8. Open and review a release PR. Merge, tagging, public-directory submission, and publication remain separately authorized.
9. When tagging is authorized, use `vX.Y.Z` only after the manifest and exact merged commit agree.

## Rollback

Reinstall the last accepted tag, verify its release manifest and checksums, then repeat discovery, implicit activation, explicit-only controls, focused-reference loading, and uninstall tests. A repository rollback does not prove already installed clients changed.

## Deprecation

Record the replacement, announcement version, removal version, reason, and migration steps. Allow at least one release of notice unless immediate removal is required for security.

## Revocation

Add the skill to `catalog/revocations.json`. Generation, packaging, and marketplace advertisement must omit revoked skills. The catalog can withdraw availability but cannot forcibly delete a copy already installed on a client. Notify users through an authorized release channel and provide a replacement or explicit removal guidance.
