# Skill Naming Review, 2026-10-28

This review compares the catalog's skill names with the naming choices in Google's Elephant-Goldfish Model (EGM) plugin and with the published naming rules. It is a research record. It proposes changes; it does not rename anything.

## Answer first

The catalog's core naming rule is sound and, on the axis that matters most, better than EGM's. Skill names carry no package or brand prefix, so they survived the 0.17.0 marketplace rename and plugin split unchanged. EGM bakes its brand into every skill name, which produces the stutter `/egm:egm-review` on namespaced clients and needs per-client invocation notes.

The weaknesses are in the vocabulary, not the format:

1. The `-review` suffix is overloaded. Twenty of 87 names end in it, while other review-shaped skills end in `-audit`, `-readiness`, `-verification`, `-diagnosis`, or `-design`. The suffix does not reliably tell a reader what kind of work the skill does.
2. Thirteen stack profiles spend the word `engineering` without discriminating anything, and in one case it changes the meaning: `gcp-data-engineering-profile` can be read as "GCP data engineering" or as "GCP data" plus the profile suffix.
3. A few clusters share so many tokens that the name cannot separate them without the description, for example `data-authority-migration-ratification`, `data-migration-readiness`, and `authority-boundary-review`.
4. The 17 explicit-only skills are typed by people, yet several are long noun phrases, such as `research-to-publication-lifecycle` (33 characters) and `merge-conflict-reconciliation` (29 characters).
5. `measured-skills` names the repository, the marketplace, and one 12-skill plugin. `measured-skills@measured-skills` has the same doubled shape as EGM's `egm@egm`.
6. The authoring guide states format limits but no naming grammar, and the validator does not reject the reserved words `anthropic` and `claude`.

There is no observed routing failure in this repository that traces to a skill name. The one recorded routing gap (0.13.0 motion review) was a description problem. Any rename should therefore be justified by an ablation test, not by taste, because renames break installed references and the catalog ships no compatibility aliases.

## What EGM does

EGM is an open-source plugin for drafting and reviewing design documents. It ships seven skills and nine reviewer personas. Observed in a clone of the `google/elephant-goldfish-model` repository, `main` branch, on 2026-10-28 at head `05f8984`. Repository files and commits below are cited by path and commit because this repository does not link external repositories.

- Every skill name has the brand prefix: `egm-brainstorm`, `egm-draft`, `egm-review`, `egm-review-loop`, `egm-resolve`, `egm-bootstrap`, and `egm-drift-report`. The plugin name is also `egm`, so Claude Code and Antigravity invoke them as `/egm:egm-brainstorm`. The README tells the reader to add the `/egm:` prefix in those clients and to use the skill picker in Codex.
- The website and the architecture design show the unprefixed command form, `/egm-brainstorm`, which is not what a Claude Code user types.
- All seven skills set `disable-model-invocation: true`. They are commands a person runs in sequence, so the names are short verbs: brainstorm, draft, review, resolve.
- Skill directories started as `skills/egm_brainstorm` with frontmatter `name: egm-brainstorm`. Commit `e45f640` (2026-10-27) renamed the directories because the omp client silently dropped all seven skills when the directory and name differed. The commit notes that Claude Code tolerated the mismatch and omp did not.
- Reviewer persona files still differ from their declared names. `agents/design_critic.md` declares `name: egm-design`, and `docs/codex.md` has to warn that `egm-design` maps to `design_critic.md`, not `design.md`.
- Commit `feff07d` (2026-10-28) corrected the README to say Antigravity also needs the `/egm:` prefix. Invocation guidance changed twice in two days.
- In omp, skills run as `/skill:egm-<command>`, a fourth invocation form.

## What the published rules say

| Rule | Source | Our status |
| --- | --- | --- |
| `name` is 1 to 64 characters, lowercase ASCII letters, digits, and single hyphens, with no leading or trailing hyphen | Agent Skills specification | Enforced by `skill_name_errors` in `scripts/validate_catalog.py` |
| `name` matches the parent directory | Agent Skills specification | Enforced; canonical metadata is compared with the directory |
| No reserved words `anthropic` or `claude` | Anthropic skill best practices | Not checked; no current name contains them |
| Prefer gerund form, such as `processing-pdfs`; noun phrases and action forms are acceptable; avoid vague names and inconsistent patterns within a collection | Anthropic skill best practices | Noun phrases, mostly consistent |
| Plugin skills are namespaced as `/plugin-name:skill-name` | Claude Code skills and plugin reference | Applies to all 11 generated plugins |
| A plugin skill and a same-named local skill both load because of that namespace; a bundled skill can be replaced by a same-named project skill | Claude Code skills documentation | Our names avoid the bundled `code-review` and `security-review` |

The best-practices guide also says the name and description are what Claude reads when deciding whether to use a skill. That makes names a routing input, but it does not say how much weight a name carries next to the description.

## Catalog measurements

Measured on this branch from `catalog/skills.json` and `skills/*/SKILL.md`, catalog version 0.18.0.

- 87 skills. Names are 12 to 41 characters, median 25. Token counts: 18 with two tokens, 40 with three, 26 with four, and 3 with five.
- Plugin-qualified names, such as `measured-engineering-review:code-change-review`, are 31 to 65 characters, median 49.
- Final tokens: `review` 20, `profile` 13, `design` 4, `diagnosis` 4, and 40 other suffixes used once or twice.
- 29 names repeat a token from their plugin name, for example `measured-engineering-review:accessibility-review` and `measured-stack-profiles:go-engineering-profile`. This is the same stutter as EGM's, but it comes from the skill's own meaning, not from a brand prefix.
- 70 skills are implicit and 17 are explicit-only. No name signals which is which.
- The catalog's `conflicts_with` fields hold 26 unique pairs. 18 involve at least one name ending in `-review`, and in 9 both names end in it. Conflict pairs mark skills that need careful routing, so a suffix shared across them adds little help.

## Lessons from EGM

### 1. Do not put the package into the name

EGM's prefix exists for clients without a namespace, but every namespaced client then shows the brand twice, and the docs must explain several invocation forms. Our generated projects already handle the no-namespace case correctly: `scripts/project_skills.py` adds the project's prefix only when it projects skills into a project directory, where no plugin namespace exists. Keep that split. The canonical name is the identity; prefixes belong to the packaging step.

The 0.17.0 migration in `catalog/plugin-migrations.json` shows why this matters. The marketplace changed from `jovanipink-skills` to `measured-skills`, and `jovanipink-engineering` split into three plugins, with `compatibility_aliases` set to false. Because no skill name carried the old brand, every skill identity survived.

### 2. One identifier per thing

EGM's underscore directories and its persona file names each cost a fix or a warning. Our validator already requires the directory and the name to match. Keep that check, and apply the same rule to any future agent or reference file that has a declared name.

### 3. Name for the reader who actually uses the name

EGM's names serve people typing commands in order, so they are short verbs. Our implicit skills are chosen by the model from a list, so their names should separate near neighbors. Our explicit-only skills are typed by people, so they should be short and start with a verb. The catalog already does this in places, such as `request-code-review` and `publish-change-safely`, but not consistently.

### 4. Never infer parity across clients

Claude Code accepted EGM's mismatched names, and omp rejected them without an error. That matches this repository's rule to record client behavior as observed evidence. Naming checks should follow the strictest documented client, not the most forgiving one.

### 5. Keep the brand at the system level

EGM's memorable names, Elephant and Goldfish, describe roles in the method. The skills themselves have plain names. The catalog does the same with `measured`, which appears only in plugin and marketplace names.

## Proposals

These are proposals, not decisions. Each rename is a breaking change for installed users, because the catalog does not ship aliases, and the Claude Code skills page describes aliases only for bundled skills.

1. **Write a naming grammar into `docs/authoring.md`.** Suggested form: `<object>-<mode>`, where the mode suffix comes from a closed list with defined meanings, for example `review` (find defects in an existing artifact), `audit` (check against an explicit external standard), `diagnosis` (explain an observed failure), `design` (propose a new structure), `planning` (order future work), and `profile` (stack-specific judgment). Explicit-only skills use a leading verb instead: `<verb>-<object>`.
2. **Add two cheap validator checks.** Reject `anthropic` and `claude` as name tokens, and warn when a new name ends in a suffix that is not in the closed list.
3. **Run a name ablation before any rename.** Re-run the existing routing and near-miss cases with each skill's name replaced by a neutral identifier and the description unchanged. If routing does not change, names are not worth a breaking rename, and the effort belongs in descriptions. If it does change, the cases that moved show which names to fix first.
4. **Candidates to review if the ablation shows names matter:**
   - Drop `engineering` from the 13 profiles, for example `go-profile` and `gcp-data-profile`. This saves 12 characters each and removes the `gcp-data-engineering-profile` ambiguity.
   - Separate the data-authority cluster so each name states its distinct act: ratifying a record, checking migration readiness, and mapping authority boundaries.
   - Shorten long explicit-only names, such as `research-to-publication-lifecycle`.
5. **Rename the catch-all plugin, not the marketplace.** A plugin named for its contents, such as evidence and quality workflows, would stop `measured-skills` from meaning three things. This is also a breaking change and needs its own migration record.
6. **Do not adopt the gerund form.** The published guidance lists noun phrases as acceptable and ranks consistency above form. A catalog-wide gerund rename would break every installed reference for no measured benefit.

## Evidence table

| Finding | Status | Source | Date | Limit |
| --- | --- | --- | --- | --- |
| EGM skill names use an `egm-` prefix inside an `egm` plugin, giving `/egm:egm-<skill>` | Observed | EGM `README.md` and `docs/claude.md` | Read 2026-10-28, head `05f8984` | Not run in a client |
| egm.dev shows the unprefixed `/egm-<skill>` form | Observed | [egm.dev](https://egm.dev) | Read 2026-10-28 | Static page text |
| EGM directories were renamed from underscores to hyphens because omp dropped mismatched skills | Source claim, from the commit message | EGM commit `e45f640` | 2026-10-27 | The omp behavior was not reproduced here |
| EGM persona `egm-design` lives in `design_critic.md` | Observed | EGM `docs/codex.md` and `agents/design_critic.md` | Read 2026-10-28 | None |
| All EGM skills are explicit-only | Observed | `skills/*/SKILL.md` frontmatter in the EGM repository | Read 2026-10-28 | None |
| "Thousands of Google engineers use EGM" | Source claim | EGM `README.md`, [egm.dev](https://egm.dev) | Read 2026-10-28 | Not independently verifiable |
| Name format, length, and directory-match rules | Primary rule | [Agent Skills specification](https://agentskills.io/specification) | Read 2026-10-28 | None |
| Gerund preferred; noun phrases acceptable; reserved words; consistency within a collection | Primary guidance | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Read 2026-10-28 | Guidance, not a validator |
| Plugin skills run as `/plugin-name:skill-name`; same-name precedence rules | Primary documentation | [Claude Code skills](https://code.claude.com/docs/en/skills), [plugin reference](https://code.claude.com/docs/en/plugins-reference) | Read 2026-10-28 | Claude Code only |
| Skill names survived the 0.17.0 marketplace and plugin rename | Observed | `catalog/plugin-migrations.json` | 0.17.0 | Local history is shallow; earlier skill renames were not checked |
| No routing failure in this repository traces to a skill name | Observed absence | `docs/client-candidate-v0.13.0.md`, `docs/authoring.md` | Read 2026-10-28 | No name ablation has been run, so the absence is weak evidence |

## Open questions

- How much weight do Claude, Codex, and Antigravity give the name compared with the description? Only the ablation in proposal 3 can answer this for this catalog.
- Does any supported client offer aliases for plugin skills? If one does, renames become much cheaper on that client.
- Were any skills renamed before the history available in this clone? The clone is shallow.
