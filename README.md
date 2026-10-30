# Atlas

A personal, atemporal knowledge graph: one canonical note per concept, in my words
and notation, linked across disciplines. Obsidian for reading and the graph,
Markdown + LaTeX for content, Git for the history of how understanding evolved.

Repo: <https://github.com/angelpedruiz/atlas>

## Layout

```
docs/            agreed project docs: purpose.md (the goal), status.md (where we are)
concepts/        one file per concept: <slug>.md   (the whole graph lives here)
notation/        house notation every note follows
templates/       starter concept template, adapt per note (Obsidian core Templates plugin)
_inbox/          raw captures waiting to be turned into concepts
assets/          figures (theme-aware SVGs) and attachments
tools/atlas.py   CLI for search, creation, linting, graph export (stdlib Python)
tools/hooks/     pre-commit hook running `atlas lint`
AGENTS.md        rules for coding agents (CLAUDE.md imports it)
```

## Setup

1. Open this folder as a vault in Obsidian. Graph view colours nodes by domain and
   shows unwritten concepts (stubs) as faded nodes.
2. Enable the lint hook once per clone:
   ```sh
   git config core.hooksPath tools/hooks
   ```
3. Optional: put `tools/` on your PATH or alias `atlas="python3 tools/atlas.py"`.

## Daily use

```sh
atlas find "linear quadratic estimator"   # does this concept exist under any name?
atlas new "Particle filter" --alias SMC --domain estimation --essence "One sentence."
atlas show kalman-filter                  # typed neighbourhood incl. inverse edges
atlas stubs                               # linked-but-unwritten concepts, most wanted first
atlas list --status seed                  # agent drafts whose Intuition I haven't rewritten
atlas dupes                               # candidate duplicates / equivalences
atlas lint                                # schema and link checks
atlas graph > graph.json                  # for agents or a future custom viewer
```

Note lifecycle: `seed` (agent draft) → `draft` (I've verified and corrected it) →
`stable`. Agent changes stay on a branch until I've reviewed them. Typed relations (`requires`, `special_case_of`, `equivalent_to`,
`analogous_to`, `contrasts_with`) live in frontmatter; see `AGENTS.md`.

## How understanding is versioned

Notes are always the current state. The past lives in Git:

```sh
git log --follow -p concepts/kalman-filter.md   # how one concept evolved
git log --stat --since="1 month ago" concepts/   # what changed recently
```

## Deferred

Embedding-based equivalence search (plugs into `atlas dupes`), a custom
graph + concept viewer reading `atlas graph`, spaced repetition from notes,
scheduled agent passes for cross-domain links.
