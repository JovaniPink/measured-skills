# Editorial Style

Use this guide for repository documentation, canonical skills, focused references, evaluations, code comments, generated distributions, and project-authored pull request text.

## Use ASCII text

Use ASCII characters only. Do not use emojis, curly quotation marks, long dash characters, Unicode ellipses, decorative bullets, or symbols that require a special character. Use straight quotation marks, the ordinary hyphen, three periods when an ellipsis is necessary, and plain words in place of symbols.

Keep exact URLs, command flags, identifiers, protocol fields, and source paths unchanged when accuracy depends on their spelling. They must still be safe to publish.

## Use US English

Use US spelling and punctuation in reader-facing text. Keep an external proper name or exact identifier unchanged when changing it would make the reference inaccurate.

Prefer the following project terms:

- explicit-only
- read-only
- skill-level
- source-grounded
- cross-client
- multi-agent
- near-miss
- output-quality
- repository

## Write for an approachable reader

Aim for an eighth-grade reading level in setup guides and daily-use docs. Keep exact commands and needed technical terms. Explain those terms where they first appear. A reading score is a warning sign to review the text, not a reason to remove facts.

- Lead with what the reader can do or what the check found.
- Prefer "check" to "validate", "file hash" to "immutable identity", and "app or CLI" to "surface" in everyday guidance.
- Put advanced details in linked notes after the main steps.
- Use one action per step and name the expected result.

- Use active voice and concrete nouns.
- State the requested outcome before supporting details.
- Explain an acronym the first time it appears unless the audience will clearly know it.
- Explain why a safety boundary exists so it reads as useful guidance, not a reprimand.
- Prefer short sentences when a sentence contains several decisions.
- Avoid calling a task, question, or mistake obvious, easy, trivial, or simple when that wording could dismiss the reader.
- Avoid exaggerated claims, promotional filler, scolding language, and role-play personas.
- Preserve necessary uncertainty and technical precision. Friendly language must not weaken a security or authority boundary.

## Keep claims precise

Treat local, committed, pushed, reviewed, merged, deployed, and live as separate states. Name the evidence for a claim and distinguish observation from inference, proposal, and unresolved work.

## Edit the source of truth

Author skills only under `skills/`. Regenerate the Codex and Claude plugin trees and Claude.ai archives after a canonical change. Do not repair generated files by hand.

Third-party bot messages and external source text are outside the repository's editorial control. Do not copy their decorative formatting into project documentation.

## Final review

Before a pull request:

1. Run the checks in [Testing and Validation](testing.md).
2. Read the changed text as a new user would.
3. Confirm that pull request text follows this guide.
