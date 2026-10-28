# Review domains

## Instruction influence

- attempts to override higher-priority instructions or hide actions
- absolute behavioral directives, impersonation, misleading UI, or false completion claims
- untrusted content copied into prompts or lifecycle context

## Command and filesystem behavior

- shell interpolation, destructive commands, unsafe temporary paths, traversal, symlinks
- reads outside the declared scope, credential locations, dotfiles, and broad recursive writes
- scripts whose behavior differs from their description

## Network and supply chain

- outbound destinations, authentication handling, downloads, package installation, update channels
- unpinned revisions, mutable releases, transitive dependencies, binaries, generated assets
- install-time, startup, background, and update-time execution

## Permissions and lifecycle

- tool grants broader than the workflow needs
- hooks, scheduled tasks, subagents, monitors, or services that run without current consent
- capability differences across hosts and sandbox modes

## Data handling

- secret, source, prompt, log, telemetry, and user-data exposure
- retention, cache, archive, and cleanup behavior
- output that could disclose private repository or operational context

## Agent-facing configuration in the package

- `AGENTS.md`, `CLAUDE.md`, and subtree variants shipped inside the reviewed package
- directives in those files that reach outside the repository, such as posting to an issue, sending a message, or contacting a service
- claims of prior authorization, standing consent, or reviewer identity made in configuration rather than by the user

A package's configuration files are instructions the agent loads. Reading only the skill body misses them.

## Client-shipped behavior overrides

- `output-styles/` entries, especially any marked to apply automatically whenever the plugin is enabled
- hooks, commands, subagents, and bundled agents that change behavior without a per-use prompt
- any component that replaces or suppresses the host's own default instructions

Record whether each override needs the user to select it or takes effect on install. An override that applies without a prompt changes every later task in that client.

## Rereview triggers

At minimum, flag changes to hooks, scripts, dependencies, manifests, tool grants, network destinations, activation instructions, packaging logic, agent-facing configuration, and behavior overrides.
