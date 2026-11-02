# Moving from 0.18 to the 0.19 preview

This is a breaking identity migration, not an automatic update. No installation
has been changed. The exact map is [0.18 to 0.19](../catalog/migrations/0.18-to-0.19.json).
The older [0.16 to 0.17 map](../catalog/plugin-migrations.json) remains intact.

## What changes

All 88 existing capabilities have one destination. Names describe actions and
objects; supporting profiles use `stack-<technology>`. Four packs distribute the
catalog: Measured Workflows, Quality, Stacks and Operations. They are not activation
recommendations. The marketplace and repository remain `measured-skills`; there is
no catch-all plugin with that name. The chooser and motion design add two read-only
skills. All 17 prior explicit-only classifications and all risk classes survive.

Historical names are searchable, not installed aliases. Current exporters reject
old identifiers and print the replacement. Existing daily and finish-work profiles
keep their IDs with mapped selections. The new `finish-work-core` has nine skills;
explicit execution, publication and handoff remain outside it.

## Prepare an upgrade, when separately authorized

1. Record the exact old source revision and installation receipt, client, account
   and machine. Keep an immutable backup or rebuildable old package.
2. Inspect enabled plugins, project skills and account uploads. Detect old and new
   names together, including duplicate source locations. A version label alone
   cannot establish the loaded bytes.
3. Review this map and stage a focused profile from an exact clean commit. Example:

   ```sh
   python3 scripts/export_selected.py --profile finish-work-core --stack stack-python --client codex --output /new/staging/directory
   ```

   Replace the destination with a new directory under an existing parent. This
   writes a staging bundle only. Use `claude` or `antigravity` for those projections.
   Duplicate selections, obsolete names, explicit-only additions and unsafe paths fail.
4. Under separate installation authority, disable the replaced sources using the
   client's supported controls before enabling their replacements. Do not delete
   unrelated skills or account uploads. Stop if mixed identities remain ambiguous.
5. Verify bytes, then inspect actual loaded entries in a disposable workspace.
   Loading is separate from successful behavior. Test each client/account/Mac
   independently; do not transfer credentials, caches or acceptance claims.

Antigravity still excludes all 17 explicit-only skills. Ordinary authorized work
can proceed without importing them. The project projector retains its stricter
read-only implicit selection rule; use staged exports for bounded-execution skills.

## Roll back

Disable the new selection under explicit installation authority; restore the
recorded old package using its exact source revision and receipt. Verify bytes and
loading again. Old receipts remain verifiable against old sources; do not rewrite
them with new names. A Git revert alone does not roll back client installations.

Use ordinary commits and pushes. Preserve historical source anchors and manifests.
For catalog releases, commit sources and generated artifacts, then bind the manifest
from that clean source commit in a separate commit. No rebase, squash or force-push
may remove those anchors. Publication, merge and release remain separate decisions.
