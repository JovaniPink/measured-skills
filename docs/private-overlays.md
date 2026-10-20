# Private Repo-Local Overlays

Private facts stay with the repository that owns their authority. The portable public catalog supplies reusable workflows; a private overlay supplies only the product-specific authority, topology, schema, identity, or operational contract needed by that repository.

```text
.agent-skills/skills/       # Canonical private repo-local source
.agents/skills/             # Generated Codex projection
.claude/skills/             # Generated Claude projection
```

The canonical private source is authoritative. The two client directories are projections and must be regenerated rather than hand-edited. A repository may keep these paths private even when its application code is public.

Synchronize an overlay with:

```sh
python3 scripts/sync_private_overlay.py --repo path/to/private-repository
python3 scripts/sync_private_overlay.py --repo path/to/private-repository --check
```

The synchronizer writes only `.agents/skills/` and `.claude/skills/` inside the named repository. It does not publish, install, push, or grant tool permissions. When it writes, `--repo` must be a real path with no symlinked component; the synchronizer refuses a symlinked path rather than following it. Pass the repository's real path, for example the output of `pwd -P`. It also refuses symlinked `.agents` or `.claude` folders. The `--check` mode only reads.

An overlay always lives inside the product repository that owns the private facts. The separate `skills-private` repository holds only the policy and the validator. It stores no skills, and it is never a synchronizer target. Point `--repo` at the product repository, not at the policy repository.

## Existing Conventions

Before creating an overlay, check whether the product repository already has repo-local skills, a projection script, or `AGENTS.md` rules about them.
- If it does, follow that repository's convention and its own checker. Do not add `.agent-skills/` or run the synchronizer there.
- Use the synchronizer only for repositories that have no existing convention.
- The synchronizer enforces part of this check. It refuses to write or check a repository that has `.claude/skills/` or `.agents/skills/` but no `.agent-skills/` source. A root `AGENTS.md` alone does not block it, so still read that file first.

## Fictional example

Assume a fictional warehouse service named Northwind Relay. Its public workflow can use `authority-boundary-review` to ask which system owns an order and which systems are projections. Its private overlay may identify `Order Ledger A` as the current authority, name an internal reconciliation report, and state who may ratify a writer change. Those private names and contracts remain in Northwind Relay's repository; the public skill contains none of them.

## Placement test

- Public core: reusable across independent contexts, independently sourceable, safe to expose, and testable without private facts.
- Private overlay: correct execution depends on a private authority, identity, topology, contract, dataset, customer, or product.
- Neither: proprietary, unsafe, obsolete, duplicative, unsupported, or without demonstrated use.

An overlay may narrow or supply private context, but it must not weaken the public workflow's safety boundaries or silently grant tool permissions. Publication, deployment, migration, deletion, and authority ratification remain separately authorized actions.

## Example notice

The fictional, copyable example under `examples/private-overlay/` carries the full repository MIT notice in its canonical skill and both generated projections. Keep that notice when reusing the example. The synchronizer preserves a source skill's existing notices; it does not assign the public repository's MIT license to a private overlay or establish rights in private material.
