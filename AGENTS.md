# Repository guidance

- Before changing a subtree, read its applicable subtree `AGENTS.md`; for specialized work, launch from that directory so client instruction loading is observable.
- Author skills only under `skills/`; regenerate client distributions.
- Treat `plugins/` as generated output.
- Do not add private paths, identities, infrastructure contracts, secrets, proprietary text, hooks, MCP servers, broad tool grants, or skill-level executables.
- Keep diagnosis, review, publication, merge, deployment, and provider acceptance as separately authorized actions.
- During a release freeze, do not change plugin, ZIP, or discovery bytes. See `docs/audits/release-decision-0.19.0.md`.
- Run `python3 scripts/validate.py` and the unit tests before describing the catalog as valid.
- Record manual client behavior as observed evidence; never infer parity across clients.
- Use ASCII, US English, and approachable language. Follow `docs/editorial-style.md`.
