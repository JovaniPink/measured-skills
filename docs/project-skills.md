# Owned project projections

The canonical workflows stay in `skills/`. Each project owns `docs/skills/project.json` and its Markdown contract. The manifest format is version 1: full `source_commit`, unique selected `skills`, a kebab-case `prefix`, relative `contract`, and tested `codex_version` (currently exactly 0.154.0).

Use a reviewed checkout of this repository at the full pin:

```sh
python3 scripts/project_skills.py --source-root . --project-root /path/to/project --check
```

Omit `--check` to regenerate. The tool reads committed Git bytes, not dirty source files. A missing checkout, different HEAD, stale contract, edited owned output, unsafe path or ownership collision blocks the operation. It performs no network access or package installation.

Read-only implicit workflows use `.agents/skills`; Codex explicit-only workflows use `.codex/skills`; Claude uses `.claude/skills` with native invocation controls. Explicit workflows never enter the shared directory Antigravity discovers. Every copy contains its required references and project contract; generated names carry the project prefix.

`docs/skills/generated.json` records exact source, manifest, contract and output hashes, logical skills and physical client paths. Generation preflights ownership and paths, stages replacements, and rolls back an interrupted write. Cleanup removes only previously owned files and empty owned directories. Local edits to generated files block regeneration; edit canonical source or the project contract instead. Revoked skills and packs are removed on an explicit pin update, including the final skill-to-zero transition.

CI must check out the owned source at the manifest pin and compare bytes without rewriting output. This supports reproducibility, not automatic revocation propagation: owners must review source revocations and advance pins. Client upgrades require a new native discovery probe and an explicit compatibility update. A successful file check does not prove behavioral invocation controls.
