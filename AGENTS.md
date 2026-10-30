# Agent rules — Atlas

This repo is Angel's personal, atemporal knowledge graph. Each concept has exactly
one canonical note in `concepts/`, written in Angel's words and notation, linked
to related concepts across disciplines. Git history is the record of how
understanding evolved; notes themselves never carry dates or "updated" logs.

Tooling: `python3 tools/atlas.py <command>` (stdlib only). Run `--help` for details.

`docs/` holds what Angel and agents have agreed: `purpose.md` is the goal, and
`status.md` tracks the repo against it. Change `purpose.md` only with Angel's agreement.

## Invariants

1. **One concept, one file.** `concepts/<slug>.md`, slug = kebab-case of the
   canonical name (`kalman-filter`). No subfolders, no course or date folders,
   no index/MOC notes. The graph is the structure.
2. **Search before you create.** Run `atlas find "<name>"` for the name *and every
   synonym you know* (other fields' names, acronyms, notation-based names).
   If anything scores ≥ 0.75, extend that note (add an alias, a section, a
   connection) instead of creating a new one. `atlas new` enforces this.
3. **Equivalence is a link, not a merge.** If the same idea appears under a different
   name in another field, link it with `equivalent_to` (or `analogous_to` if the
   match is structural rather than exact) and write the translation in
   `## Connections`: the symbol map and the scope of the equivalence. Merge two
   notes only if they are the same object *and* the same framing, and only after
   Angel approves. A merge keeps the surviving slug, moves the other name to
   `aliases`, and rewrites links (`atlas rename`).
4. **Notation follows `notation/notation.md`.** Translate source notation into it;
   never copy a textbook's symbols verbatim. If a new symbol is needed, add it to
   the table in the same commit. Record unavoidable collisions there too.
5. **Angel owns the voice.** The `## Intuition` section is Angel's. Agents may draft
   it only in new notes (`status: seed`). In `draft`/`stable` notes, never rewrite
   Intuition; leave a suggestion as an Obsidian comment
   `%% agent: ... %%` (hidden in reading view) or in the commit message.
   Other sections may be extended, but do not delete Angel's text without asking.
   Agent changes are proposals: work on a branch, and Angel verifies and corrects
   them before they reach `main`.
6. **Link densely, type the important edges.** Every new note links to ≥ 2 existing
   notes. Typed relations go in frontmatter (vocabulary below); the prose in
   `## Connections` says *why*. Declare each typed edge once, on either side —
   `atlas show` computes inverses.
7. **Stubs are welcome.** `[[some-concept]]` may point to a note that does not exist
   yet. Unresolved links are the to-do list (`atlas stubs`). Never create an empty
   file just to resolve a link.
8. **Don't duplicate content.** Reuse with an embed (`![[gaussian-conditioning#Definition]]`)
   or a link, never a copied derivation.
9. **Links target slugs, not aliases.** Write `[[kalman-filter|KF]]`, not `[[KF]]`
   (Obsidian resolves by filename). `atlas lint` catches this.

## Frontmatter schema

```yaml
---
title: Kalman filter                 # canonical display name
essence: "The exact Bayesian filter for linear-Gaussian models."   # one sentence, required
aliases: [KF, "linear quadratic estimator"]   # other names, incl. other fields' names
domains: [estimation, control]       # reuse existing values: `atlas domains`
status: seed                         # seed (agent draft) | draft (Angel edited) | stable
requires: ["[[gaussian-conditioning]]"]      # typed relations: list of quoted wikilinks
special_case_of: ["[[bayesian-filtering]]"]
sources:                              # provenance, not organisation
  - "Särkkä & Svensson, Bayesian Filtering and Smoothing (2023)"
---
```

Relation keys are optional; omit empty ones except `requires`.

## Relation vocabulary

| key | meaning (A → B) | inverse shown as | symmetric |
|---|---|---|---|
| `requires` | understanding A needs B | `required_by` | no |
| `special_case_of` | A is B with extra assumptions | `generalizes` | no |
| `equivalent_to` | same mathematical content under a translation; state scope in Connections | `equivalent_to` | yes |
| `analogous_to` | shared structure, not identical (dualities, same recursion in another semiring) | `analogous_to` | yes |
| `contrasts_with` | alternative approaches worth comparing | `contrasts_with` | yes |

Add a new relation type only with Angel's approval, and register it in
`tools/atlas.py` (`RELATIONS`) and this table in the same commit.

## Note body skeleton

```
# <title>
$$ \Large ... $$   — the main object, centred, each term labelled
## Intuition        — 2–5 sentences, Angel's words; the picture to keep in mind
## Definition       — formal statement in house notation
## Key results      — the facts worth remembering, each one line + equation if needed
## Connections      — prose for each typed edge and notable untyped link
## Open questions   — what isn't understood yet
```

Open with the concept's main object when it has one: a display math block right
under the title, using `\Large` (`\large` if it would overflow) and `\underbrace`
to label each term in plain words. It should be visible on opening the note.

This skeleton is a starting point, not a schema, and the template stays deliberately
loose for now: add, rename, drop or reorder sections to fit the concept. Only
`## Intuition` and `## Connections` are worth keeping, because the invariants above
refer to them. Sections may be empty. Keep notes focused: if a section grows into its
own concept that would be linked from ~3 other places, split it out.

## Workflows

- **Capture → concept.** Raw material lands in `_inbox/` (any format). To process:
  identify the concepts, `atlas find` each, extend or create notes, add links,
  then delete the inbox file in the same commit.
- **Find equivalents.** `atlas dupes` lists likely duplicates (name similarity,
  shared neighbourhood). Investigate each; propose `equivalent_to` links or merges.
- **Rename.** `atlas rename <old> <new>` moves the file, rewrites links across
  the vault, and keeps the old title as an alias.
- **Before committing.** `atlas lint` must pass (the pre-commit hook runs it).

## Commits

Commit every change, and update `docs/`, `README.md` and this file in the same commit
if the change affects them, so the docs always describe the current project.

One logical change per commit. Message format: `<verb>(<slug>): <summary>`, with
verbs `add`, `refine`, `link`, `merge`, `rename`, `notation`, `tools`.
Agents append a trailer `Agent: <name>` so agent edits are separable from Angel's
in `git log`. Never rewrite history.
