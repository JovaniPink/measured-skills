# Plugin identity

The repository root is a marketplace. Its `marketplace.json` points to the
11 generated Claude plugin packs under `plugins/claude/`. Each pack has its
own `.claude-plugin/plugin.json`; install the packs you need.

`icon.svg` is the original shared Measured Skills artwork. The distribution
builder copies it into every Claude pack and sets the pack's `icon` path.
The mark combines measurement ticks with a rising path: progress needs evidence.
The `icon` field supports Anthropic's directory listing. Claude Code ignores it
when loading the plugin; it does not add an icon to the CLI. See the official
[manifest reference](https://code.claude.com/docs/en/plugins-reference#directory-listing-fields).
No directory submission or display has been tested.

Run `python3 scripts/build_distributions.py` after changing the artwork or
manifest generator. Do not edit generated pack files by hand. The repository
uses per-pack manifests to preserve generated invocation controls.

The engineering-learning workflow remains a separate pilot. Branding does not
qualify or publish another catalog skill.
