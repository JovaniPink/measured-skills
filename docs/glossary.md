# Glossary

Plain definitions for the words this catalog uses. They are in alphabetical order. The states at the end are the ones we never blend.

**Antigravity.** Google's agent client. It has a command line named `agy`, a desktop app, and an IDE. This repository ships generated packs under `plugins/antigravity/` and an offline preview builder. Loading in the client still needs a check. See [Antigravity setup](clients/antigravity.md).

**Authored.** Something we wrote. An authored claim says what the instructions intend. It does not say what any client did.

**Candidate.** A dated record for one catalog version. It lists what is prepared, installed, enabled, loaded, and behavior-tested in each app and CLI. See the [current candidate record](client-candidate-v0.18.0.md).

**Catalog.** All 86 skills in this repository, plus the records that describe them.

**Claude Code.** Anthropic's command-line client, and the Code mode in the Claude desktop app. It loads skills as packs.

**Claude.ai.** Anthropic's web and desktop chat product. It loads skills from your account library, not from a pack. An account upload and a Code pack are separate installs.

**Client.** The app or CLI that loads a skill and runs your task. Codex, Claude Code, Claude.ai, and Antigravity are all clients.

**CLI.** Short for command-line interface. An app you use by typing commands in a terminal.

**Codex.** OpenAI's coding client. It has a command line and a desktop app, and it signs in with your ChatGPT account. ChatGPT web and ChatGPT Work keep their own skill libraries and need their own checks.

**Explicit-only.** A marking that means the skill stays off until you name it. Naming it does not authorize a push, merge, deletion, release, or deployment. 17 of the 86 skills are explicit-only.

**File hash.** A short fingerprint made from a file's bytes. Two files with the same hash hold the same contents. A matching version number does not prove that.

**Hold.** A decision not to ship or enable something yet, even though the files are ready, because a named check has not passed. A hold always names the evidence that would lift it. For example, the 17 explicit-only skills are held for Claude.ai uploads. The check they wait on is a control that stops the app from picking them on its own.

**Implicit.** A marking that means your client may pick the skill on its own when your request matches its description. You can still name it directly. 69 of the 86 skills are implicit.

**Marketplace.** A place your client looks for packs. This repository is its own marketplace, and it is named `measured-skills`.

**Near-miss.** A test request that looks like a match for a skill but should not start it. Near-miss cases check that a skill stays quiet when it should.

**Observed.** Something we ran and wrote down, with the exact client, version, date, and result. Observed evidence never carries from one app to another.

**Output style.** A client setting that changes tone and format for every reply. A skill is different: it loads instructions for one kind of task. Anthropic draws the same line, and its built-in Concise style needs Claude Code v2.1.237 or later. Every observation in this repository was taken on 2.1.220, before that existed. This catalog ships no output styles.

**Pack.** A group of related skills you install together. Clients also call this a plugin. There are 11 packs.

**Plugin.** The client's word for a pack. Installing a pack and enabling each of its skills are separate choices.

**Profile.** A named list of exact skills to turn on for one kind of work. A profile installs nothing. Profiles live in `catalog/profiles.json`.

**Provenance.** The record of where a skill's content came from. It holds the source, its license, the review date, and what was changed. Every skill has an entry in `provenance/catalog.json`. See the [provenance policy](provenance.md).

**Recipe.** A suggested set of skills for one kind of work. A recipe is advice. It is not something you install.

**Session depth.** How far into a conversation an observation was taken. Every record here comes from the first turn of a fresh session, which is where instructions are followed most closely. See [the turn-depth study design](turn-depth-study.md).

**Skill.** A short set of written instructions for one kind of task. Your client reads the skill and follows its steps. A skill is text. It adds no programs, tools, or permissions.

**Trigger case.** A written example of a request that should, or should not, pick a skill. Trigger cases live in `evals/cases.json`.

## States we keep separate

These words are not interchangeable. Use the one your evidence supports.

- **Prepared.** The files are built.
- **Installed.** The client has the files.
- **Enabled.** The skill is turned on.
- **Loaded.** A task actually read the skill's instructions.
- **Behavior-tested.** A task ran, and a person checked the result.

A file on disk proves only that the file is there. A good reply does not prove which skill produced it.
