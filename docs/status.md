# Status

Where the repo stands against [purpose.md](purpose.md). Update this in the same
commit as any change that moves a line here.

## In place

- One Markdown file per concept in `concepts/`, in house notation (`notation/`).
- Frontmatter with aliases, domains, status and typed relations, checked by
  `atlas lint`.
- Inline wikilinks with display text, resolved to the canonical slug.
- Plain-text Git repo, with history as the record of understanding.
- Obsidian vault configuration for editing.
- CLI (`tools/atlas.py`) to search, create, inspect and rename concepts, with a
  JSON export (`atlas graph`). It has no command yet to add a link or edit a note.

## Not built

- One-sentence essence in frontmatter. `essence` is not in the schema, the template
  or any note, and `atlas lint` would warn about it as an unknown key.
- Implementations and `viz` code blocks in notes.
- Build step from `viz` blocks to static SVGs and interactive widgets.
- Obsidian reading view that hides plotting code and shows the static pictures.
- Atlas site: reading mode, live plots, graph, install to phone home screen.
- Obsidian on the phone (no sync route set up or documented).

## To agree

- **Required core.** The purpose makes relations prose optional, while `AGENTS.md`
  (invariants 3 and 6) relies on `## Connections`. Keep it as a convention, or move
  the prose requirement to `equivalent_to` links only?
- **Agents and intuition.** The purpose says agents never rewrite the intuition.
  `AGENTS.md` invariant 5 lets agents draft it in new `seed` notes. Is a first draft
  allowed, or should agents leave it blank?

## Known problems

- `atlas lint` fails: `concepts/kernel-ridge-regression.md` is empty and untracked.
- `tools/atlas.py` and `tools/hooks/pre-commit` have lost their executable bit in the
  working tree, so Git skips the pre-commit hook.
- Stray ref `refs/heads/main:Zone.Identifier` breaks `git log --all`.
