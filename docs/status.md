# Status

Where the repo stands against [purpose.md](purpose.md). Update this in the same
commit as any change that moves a line here.

## In place

- One Markdown file per concept in `concepts/`, in house notation (`notation/`).
- Frontmatter with essence, aliases, domains, status and typed relations, checked by
  `atlas lint`.
- Inline wikilinks with display text, resolved to the canonical slug.
- Notes open with their main object: large, centred, with labelled terms.
- Plain-text Git repo, with history as the record of understanding, public at
  <https://github.com/angelpedruiz/atlas>.
- Obsidian vault configuration for editing.
- CLI (`tools/atlas.py`) to search, create, inspect and rename concepts, with a
  JSON export (`atlas graph`). It has no command yet to add a link or edit a note.

## Not built

- Implementations and `viz` code blocks in notes.
- Build step from `viz` blocks to static SVGs and interactive widgets.
- Obsidian reading view that hides plotting code and shows the static pictures.
- Atlas site: reading mode, live plots, graph, install to phone home screen.
- Obsidian on the phone (no sync route set up or documented).

## To agree

- **Required core.** The purpose makes relations prose optional, while `AGENTS.md`
  (invariants 3 and 6) relies on `## Connections`. Keep it as a convention, or move
  the prose requirement to `equivalent_to` links only?

## Agreed

- **Agents and intuition.** Agents may draft the intuition in new `seed` notes, but
  never rewrite an existing one. Angel verifies and corrects agent changes before
  they reach `main`.

## Known problems

- Stray ref `refs/heads/main:Zone.Identifier` breaks `git log --all` and `git fetch`.
