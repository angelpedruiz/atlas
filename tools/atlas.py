#!/usr/bin/env python3
"""atlas — search, create, lint and inspect the Atlas.

Standard library only, so it runs anywhere Python 3.9+ does.

  atlas find "kalman"            ranked matches on slug/title/aliases/headings/body
  atlas new "Particle filter"    create from template (refuses likely duplicates)
  atlas show kalman-filter       typed neighbourhood, incl. computed inverse edges
  atlas list --status seed       filter notes
  atlas domains                  domain vocabulary with counts
  atlas stubs                    unresolved links ranked by in-degree (the to-do list)
  atlas dupes                    candidate duplicate / equivalent concepts
  atlas rename old-slug new-slug move file, rewrite links, keep old title as alias
  atlas lint [--strict]          schema + link checks (used by the pre-commit hook)
  atlas graph                    JSON export of nodes and typed edges
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCEPTS = ROOT / "concepts"
TEMPLATE = ROOT / "templates" / "concept.md"

# relation -> inverse name; symmetric relations map to themselves
RELATIONS = {
    "requires": "required_by",
    "special_case_of": "generalizes",
    "equivalent_to": "equivalent_to",
    "analogous_to": "analogous_to",
    "contrasts_with": "contrasts_with",
}
SYMMETRIC = {k for k, v in RELATIONS.items() if k == v}
STATUSES = {"seed", "draft", "stable"}
REQUIRED = ["title", "essence", "aliases", "domains", "status"]
LIST_KEYS = {"aliases", "domains", "sources", *RELATIONS}
KNOWN_KEYS = {"title", "essence", "status", *LIST_KEYS}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# [[target]], [[target|label]], [[target#heading]], [[target^block]], ![[embed]]
WIKILINK = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
# embedded files such as ![[figure.svg]] are not concept links
ATTACHMENT = re.compile(r"\.(?!md$)[a-z0-9]+$", re.I)
DUP_THRESHOLD = 0.75

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- parsing

def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _split_inline_list(s: str) -> list[str]:
    items, buf, quote = [], "", None
    for ch in s:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf += ch
        elif ch in "\"'" and not buf.strip():
            quote = ch
        elif ch == ",":
            items.append(buf.strip())
            buf = ""
        else:
            buf += ch
    items.append(buf.strip())
    return [i for i in items if i]


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Parse the restricted YAML subset used here: scalars, [inline, lists], block lists."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text
    data: dict = {}
    key = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and not line[0].isspace():
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                data[key] = []
            elif val.startswith("[") and val.endswith("]") and not val.startswith("[["):
                data[key] = _split_inline_list(val[1:-1])
            else:
                data[key] = _unquote(val)
        elif line.lstrip().startswith("- ") and key is not None:
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(_unquote(line.lstrip()[2:]))
        else:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
    return data, "\n".join(lines[end + 1:])


def link_target(raw: str) -> str:
    """Normalise a wikilink target to a slug-like key (Obsidian resolves by file name)."""
    return raw.strip().split("/")[-1].removesuffix(".md").lower()


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def slugify(s: str) -> str:
    return normalize(s).replace(" ", "-")


class Note:
    def __init__(self, path: Path):
        self.path = path
        self.slug = path.stem
        text = path.read_text(encoding="utf-8")
        meta, self.body = parse_frontmatter(text)
        self.meta = meta or {}
        self.has_frontmatter = meta is not None
        self.title = str(self.meta.get("title") or self.slug)
        essence = self.meta.get("essence")
        self.essence = essence if isinstance(essence, str) else ""
        self.aliases = _as_list(self.meta.get("aliases"))
        self.domains = _as_list(self.meta.get("domains"))
        self.status = self.meta.get("status")
        self.relations: dict[str, list[str]] = {}
        self.bad_relation_values: list[tuple[str, str]] = []
        for rel in RELATIONS:
            targets = []
            for v in _as_list(self.meta.get(rel)):
                m = WIKILINK.fullmatch(v.strip())
                if m:
                    targets.append(link_target(m.group(1)))
                else:
                    self.bad_relation_values.append((rel, v))
            if targets:
                self.relations[rel] = targets
        self.body_links = {link_target(t) for t in WIKILINK.findall(self.body)
                           if not ATTACHMENT.search(t.strip())}
        self.headings = re.findall(r"^#{1,6}\s+(.+)$", self.body, re.M)

    @property
    def names(self) -> list[tuple[str, str]]:
        return [("slug", self.slug.replace("-", " ")), ("title", self.title)] + [
            ("alias", a) for a in self.aliases
        ]

    @property
    def typed_targets(self) -> set[str]:
        return {t for ts in self.relations.values() for t in ts}

    @property
    def all_targets(self) -> set[str]:
        return (self.typed_targets | self.body_links) - {self.slug}


def _as_list(v) -> list[str]:
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def load() -> tuple[dict[str, Note], list[tuple[str, str]]]:
    notes, errors = {}, []
    for p in sorted(CONCEPTS.glob("*.md")):
        try:
            notes[p.stem.lower()] = Note(p)
        except Exception as e:  # noqa: BLE001
            errors.append((p.name, f"cannot parse: {e}"))
    return notes, errors


def resolve(notes: dict[str, Note], key: str) -> Note | None:
    """Resolve a slug, title or alias to a note."""
    k = key.lower()
    if k in notes:
        return notes[k]
    nk = normalize(key)
    for n in notes.values():
        if any(normalize(name) == nk for _, name in n.names):
            return n
    return None


# ---------------------------------------------------------------- search

def _name_score(q: str, name: str) -> float:
    n = normalize(name)
    if not n or not q:
        return 0.0
    if n == q:
        return 1.0
    scores = [difflib.SequenceMatcher(None, q, n).ratio() * 0.8]
    if len(q) >= 3 and (q in n.split() or q in n):
        scores.append(0.6 + 0.3 * len(q) / len(n))
    if len(n) >= 3 and n in q:
        scores.append(0.6 + 0.3 * len(n) / len(q))
    qt, nt = set(q.split()), set(n.split())
    if qt and nt:
        scores.append(0.85 * len(qt & nt) / len(qt | nt))
    return min(max(scores), 0.99)


def search(notes: dict[str, Note], query: str) -> list[tuple[float, Note, str]]:
    q = normalize(query)
    results = []
    for note in notes.values():
        best, why = 0.0, ""
        for kind, name in note.names:
            s = _name_score(q, name)
            if s > best:
                best, why = s, f"{kind}: {name}"
        for h in note.headings:
            if q and q in normalize(h) and best < 0.55:
                best, why = 0.55, f"heading: {h}"
        hits = normalize(note.body).count(q) if len(q) >= 3 else 0
        if hits and best < 0.5:
            best, why = min(0.3 + 0.05 * hits, 0.5), f"body: {hits} hit(s)"
        if best >= 0.3:
            results.append((best, note, why))
    return sorted(results, key=lambda r: -r[0])


# ---------------------------------------------------------------- commands

def cmd_find(a):
    notes, _ = load()
    query = " ".join(a.query)
    res = search(notes, query)[: a.n]
    # unresolved link targets that match: reuse these slugs instead of inventing new ones
    q = normalize(query)
    stubs: dict[str, int] = {}
    for n in notes.values():
        for t in n.all_targets - notes.keys():
            if _name_score(q, t.replace("-", " ")) >= 0.6:
                stubs[t] = stubs.get(t, 0) + 1
    if not res and not stubs:
        print("no matches")
        return 1
    for s, n, why in res:
        print(f"{s:4.2f}  {n.slug:<34} {n.title}   ({why})")
    for t, c in sorted(stubs.items(), key=lambda kv: -kv[1]):
        print(f"stub  {t:<34} linked from {c} note(s), not written yet")
    return 0


def cmd_new(a):
    notes, _ = load()
    slug = a.slug or slugify(a.title)
    path = CONCEPTS / f"{slug}.md"
    if path.exists() or slug in notes:
        print(f"error: {path.relative_to(ROOT)} already exists")
        return 1
    if not SLUG_RE.match(slug):
        print(f"error: bad slug {slug!r}")
        return 1
    hits = {}
    for name in [a.title, *a.alias]:
        for s, n, why in search(notes, name):
            if s >= DUP_THRESHOLD and s > hits.get(n.slug, (0,))[0]:
                hits[n.slug] = (s, f"'{name}' ~ {why}")
    if hits and not a.force:
        print("possible existing concept(s) — extend them, or rerun with --force:")
        for slug_, (s, why) in sorted(hits.items(), key=lambda kv: -kv[1][0]):
            print(f"  {s:4.2f}  {slug_:<34} {why}")
        return 2
    text = TEMPLATE.read_text(encoding="utf-8").replace("{{title}}", a.title)

    def fmt(xs):
        return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in xs) + "]"

    text = text.replace('essence: ""', f"essence: {json.dumps(a.essence, ensure_ascii=False)}", 1)
    text = text.replace("aliases: []", f"aliases: {fmt(a.alias)}", 1)
    text = text.replace("domains: []", f"domains: {fmt(a.domain)}", 1)
    path.write_text(text, encoding="utf-8")
    print(f"created {path.relative_to(ROOT)}")
    return 0


def _incoming(notes: dict[str, Note], slug: str):
    typed, untyped = [], []
    for n in notes.values():
        if n.slug.lower() == slug:
            continue
        for rel, ts in n.relations.items():
            if slug in ts:
                typed.append((RELATIONS[rel], n.slug))
        if slug in n.body_links and slug not in n.typed_targets:
            untyped.append(n.slug)
    return typed, untyped


def cmd_show(a):
    notes, _ = load()
    note = resolve(notes, a.slug)
    if not note:
        print(f"no note for {a.slug!r}; try `atlas find`")
        return 1
    key = note.slug.lower()
    print(f"{note.title}  [{note.slug}]  status={note.status}")
    if note.essence:
        print(f"  essence: {note.essence}")
    if note.aliases:
        print(f"  aliases: {', '.join(note.aliases)}")
    if note.domains:
        print(f"  domains: {', '.join(note.domains)}")
    edges: dict[str, set[str]] = {}
    for rel, ts in note.relations.items():
        edges.setdefault(rel, set()).update(ts)
    typed_in, untyped_in = _incoming(notes, key)
    for rel, src in typed_in:
        edges.setdefault(rel, set()).add(src.lower())
    print("  typed:")
    for rel in sorted(edges):
        for t in sorted(edges[rel]):
            mark = "" if t in notes else "  (stub)"
            print(f"    {rel:<16} {t}{mark}")
    out = sorted(note.body_links - note.typed_targets - {key})
    if out:
        print("  links out: " + ", ".join(t + ("" if t in notes else "*") for t in out))
    if untyped_in:
        print("  linked from: " + ", ".join(sorted(untyped_in)))
    if any(t not in notes for t in note.all_targets):
        print("  (* / stub = note not written yet)")
    return 0


def cmd_list(a):
    notes, _ = load()
    for n in notes.values():
        if a.status and n.status != a.status:
            continue
        if a.domain and a.domain not in n.domains:
            continue
        print(f"{n.slug:<34} {str(n.status):<7} {', '.join(n.domains)}")
    return 0


def cmd_domains(a):
    notes, _ = load()
    counts: dict[str, int] = {}
    for n in notes.values():
        for d in n.domains:
            counts[d] = counts.get(d, 0) + 1
    for d, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{c:4d}  {d}")
    return 0


def cmd_stubs(a):
    notes, _ = load()
    refs: dict[str, set[str]] = {}
    for n in notes.values():
        for t in n.all_targets:
            if t not in notes:
                refs.setdefault(t, set()).add(n.slug)
    for t, srcs in sorted(refs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"{len(srcs):3d}  {t:<34} <- {', '.join(sorted(srcs))}")
    return 0


def cmd_dupes(a):
    """Heuristic duplicate detection; the place to plug in embeddings later."""
    notes, _ = load()
    nbrs = {k: n.all_targets for k, n in notes.items()}
    for k, n in notes.items():  # make neighbourhoods undirected
        for t in n.all_targets:
            if t in nbrs:
                nbrs[t] = nbrs[t] | {k}
    out = []
    for (ka, na), (kb, nb) in combinations(notes.items(), 2):
        if kb in na.typed_targets or ka in nb.typed_targets:
            continue  # a typed edge means someone already judged the pair
        name_sim, pair = 0.0, ""
        for _, x in na.names:
            for _, y in nb.names:
                nx, ny = normalize(x), normalize(y)
                sm = difflib.SequenceMatcher(None, nx, ny)
                if sm.quick_ratio() > name_sim:
                    r = sm.ratio()
                    if r > name_sim:
                        name_sim, pair = r, f"'{x}' ~ '{y}'"
        A, B = nbrs[ka] - {kb}, nbrs[kb] - {ka}
        jac = len(A & B) / len(A | B) if len(A | B) >= 3 else 0.0
        if name_sim >= a.name or jac >= a.jaccard:
            out.append((max(name_sim, jac), na.slug, nb.slug, name_sim, jac, pair))
    for s, x, y, ns, j, pair in sorted(out, reverse=True):
        print(f"{s:4.2f}  {x} <-> {y}   names {ns:.2f} {pair}   shared-neighbours {j:.2f}")
    if not out:
        print("no candidates")
    return 0


def cmd_rename(a):
    notes, _ = load()
    old = resolve(notes, a.old)
    if not old:
        print(f"no note {a.old!r}")
        return 1
    new = a.new
    if not SLUG_RE.match(new) or (CONCEPTS / f"{new}.md").exists():
        print(f"error: bad or existing slug {new!r}")
        return 1
    src, dst = old.path, CONCEPTS / f"{new}.md"
    in_git = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--error-unmatch", str(src)],
                            capture_output=True).returncode == 0
    if in_git:
        subprocess.run(["git", "-C", str(ROOT), "mv", str(src), str(dst)], check=True)
    else:
        src.rename(dst)
    pat = re.compile(r"\[\[" + re.escape(old.slug) + r"(?=[\]|#^])", re.I)
    changed = 0
    for p in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in p.relative_to(ROOT).parts):
            continue
        t = p.read_text(encoding="utf-8")
        t2 = pat.sub(f"[[{new}", t)
        if t2 != t:
            p.write_text(t2, encoding="utf-8")
            changed += 1
    print(f"renamed {old.slug} -> {new}; rewrote links in {changed} file(s)")
    if normalize(old.title) not in {normalize(x) for x in old.aliases}:
        print(f"note: add the old name {old.title!r} to aliases if it is still a valid name")
    return 0


def cmd_lint(a):
    notes, load_errors = load()
    errs = list(load_errors)
    warns: list[tuple[str, str]] = []
    for k, n in notes.items():
        f = n.path.name
        if not SLUG_RE.match(n.slug):
            errs.append((f, "file name must be a kebab-case slug"))
        if not n.has_frontmatter:
            errs.append((f, "missing frontmatter"))
            continue
        for key in REQUIRED:
            if key not in n.meta:
                errs.append((f, f"missing key '{key}'"))
        if "essence" in n.meta and not n.essence:
            errs.append((f, "essence must be a one-sentence string"))
        for key in n.meta:
            if key not in KNOWN_KEYS:
                warns.append((f, f"unknown frontmatter key '{key}' (relation types: {', '.join(RELATIONS)})"))
        for key in LIST_KEYS & n.meta.keys():
            if not isinstance(n.meta[key], list):
                errs.append((f, f"'{key}' must be a list"))
        if n.status not in STATUSES:
            errs.append((f, f"status must be one of {sorted(STATUSES)}"))
        for rel, v in n.bad_relation_values:
            errs.append((f, f"{rel}: {v!r} is not a quoted wikilink like \"[[slug]]\""))
        if k in n.typed_targets:
            errs.append((f, "note relates to itself"))
        for d in n.domains:
            if not SLUG_RE.match(d):
                warns.append((f, f"domain {d!r} should be kebab-case"))
        existing = [t for t in n.all_targets if t in notes]
        if len(existing) < 2:
            warns.append((f, f"only {len(existing)} link(s) to existing notes (aim for >= 2)"))
        if not any(h.strip().lower() == "intuition" for h in n.headings):
            warns.append((f, "no '## Intuition' section"))

    # name collisions: the core duplicate guard
    owner: dict[str, str] = {}
    for n in notes.values():
        for kind, name in n.names:
            nn = normalize(name)
            if nn in owner and owner[nn] != n.slug:
                errs.append((n.path.name, f"name {name!r} is used by both '{owner[nn]}' and "
                                          f"'{n.slug}' — duplicate concept? (link equivalent_to, or merge)"))
            owner.setdefault(nn, n.slug)

    for n in notes.values():
        for t in n.all_targets:
            if t in notes:
                continue
            nt = normalize(t.replace("-", " "))
            if nt in owner:
                errs.append((n.path.name, f"[[{t}]] is a name of '{owner[nt]}'; link [[{owner[nt]}|...]] instead"))
                continue
            close = difflib.get_close_matches(t, list(notes), n=1, cutoff=0.88)
            if close:
                warns.append((n.path.name, f"stub [[{t}]] is very close to existing '{close[0]}' — typo?"))

    for f, m in errs:
        print(f"ERROR  {f}: {m}")
    for f, m in warns:
        print(f"warn   {f}: {m}")
    print(f"{len(notes)} notes, {len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs or (a.strict and warns) else 0


def cmd_graph(a):
    notes, _ = load()
    nodes, edges, seen = [], [], set()
    for k, n in notes.items():
        nodes.append({"id": k, "title": n.title, "essence": n.essence, "aliases": n.aliases,
                      "domains": n.domains,
                      "status": n.status, "exists": True})
        seen.add(k)
        for rel, ts in n.relations.items():
            edges += [{"source": k, "target": t, "type": rel} for t in ts]
        edges += [{"source": k, "target": t, "type": "link"}
                  for t in sorted(n.body_links - n.typed_targets - {k})]
    for e in edges:
        if e["target"] not in seen:
            nodes.append({"id": e["target"], "exists": False})
            seen.add(e["target"])
    json.dump({"nodes": nodes, "edges": edges}, sys.stdout, indent=1 if a.pretty else None,
              ensure_ascii=False)
    print()
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="atlas", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("find", help="ranked search over names, aliases, headings, body")
    s.add_argument("query", nargs="+")
    s.add_argument("-n", type=int, default=10)
    s.set_defaults(fn=cmd_find)

    s = sub.add_parser("new", help="create a concept from the template")
    s.add_argument("title")
    s.add_argument("--slug")
    s.add_argument("--essence", default="", help="one-sentence summary")
    s.add_argument("--alias", action="append", default=[])
    s.add_argument("--domain", action="append", default=[])
    s.add_argument("--force", action="store_true", help="create despite likely duplicates")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("show", help="typed neighbourhood of a concept")
    s.add_argument("slug")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("list", help="list notes")
    s.add_argument("--status", choices=sorted(STATUSES))
    s.add_argument("--domain")
    s.set_defaults(fn=cmd_list)

    sub.add_parser("domains", help="domain vocabulary").set_defaults(fn=cmd_domains)
    sub.add_parser("stubs", help="unresolved links by in-degree").set_defaults(fn=cmd_stubs)

    s = sub.add_parser("dupes", help="candidate duplicate concepts")
    s.add_argument("--name", type=float, default=0.8, help="name-similarity threshold")
    s.add_argument("--jaccard", type=float, default=0.5, help="shared-neighbour threshold")
    s.set_defaults(fn=cmd_dupes)

    s = sub.add_parser("rename", help="rename a concept and rewrite links")
    s.add_argument("old")
    s.add_argument("new")
    s.set_defaults(fn=cmd_rename)

    s = sub.add_parser("lint", help="check schema and links")
    s.add_argument("--strict", action="store_true", help="fail on warnings too")
    s.set_defaults(fn=cmd_lint)

    s = sub.add_parser("graph", help="export graph as JSON")
    s.add_argument("--pretty", action="store_true")
    s.set_defaults(fn=cmd_graph)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
