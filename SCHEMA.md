# The node schema

One shape for everything: **a thing, with provenance, with facets, in a place,
described in more than one language.** Manuscripts, market objects, saints'
shrines, wats and spirit houses are all this shape. Adapters differ; the node
does not.

Notes are plain Markdown with YAML frontmatter, so Obsidian edits them, Dataview
queries them, Claude Code edits them, and `scripts/compile.py` publishes them.
There is one set of files. There is no sync.

---

## The two decisions that are expensive to change later

### 1. The emic term is the primary type. English is a gloss.

```yaml
type: san_phra_phum          # what it IS, in the tradition
type_en: spirit house        # a translation, offered for convenience
```

**Not** `type: spirit_house` with a Thai label attached. A ศาลพระภูมิ houses the
guardian of the *land*; a ศาลเจ้าที่ houses the spirit of the *place*. They take
different offerings and frequently stand a metre apart in the same forecourt.
Laos has ຫໍຜີ, Myanmar နတ်စင်, Cambodia អ្នកតា — related, not identical.

Collapsing those into one English bucket is the precise failure this archive
exists to outrun: it is what makes a tradition legible to a machine only in the
shape the coloniser's language already had a word for. The vocabulary lives in
`_meta/vocab/place-types.md`, each term with its own definition and its own
sources. Adding a term is normal. Merging two because English lacks the
distinction is not.

### 2. Provenance is per field, not per record.

A record is usually a composite: coordinates from OSM, a heritage number from
Wikidata, opening hours from the abbot, a photograph from you. Recording one
`source` for the whole note throws that away, and once thrown away it cannot be
recovered — you can no longer tell which parts a machine asserted from which
parts a person witnessed.

Values stay plain scalars so they are pleasant to author and trivial to query:

```yaml
name_th: วัดศรีดอนมูล
lat: 19.3528096
gate_hours: "06:00-18:00"

sources:                       # record-level default
  - {type: osm, ref: way/550515471, fetched: 2026-07-22}
provenance:                    # per-field override, only where it differs
  gate_hours: {source: field, by: nan, date: 2026-07-22, confidence: verified}
```

Anything without an override inherits the record default. `scripts/validate.py`
flags a field whose value no longer matches the last compiled crawl while its
provenance still claims to be crawled — that is a human edit that forgot to say
so, and it is the quiet way a field-verified fact gets mislabelled as machine
output.

---

## Fields

### Identity
| field | notes |
|---|---|
| `id` | stable slug, the filename. Never regenerate from a name — names change. |
| `name_th` / `name_local` | the name in its own script |
| `name_roman` | romanisation |
| `aliases` | **every** variant seen in the wild: มูล/มูน, formal vs common, misspellings. Kills the variant-collapse bug structurally — see `_meta/coverage.md`. |
| `type` / `type_en` | see decision 1 |

### Place
`lat`, `lng`, `geo_precision` (`exact` \| `block` \| `area` — never fake it),
`province`, `district`, `subdistrict`, `address`

### Status
`confidence`: `verified` (someone stood there) \| `reported` (a person relayed it,
unvisited) \| `crawled` (machine-extracted) \| `heuristic` (inferred).

`restricted`: `true` withholds the record from publication without deleting it,
with `restricted_reason`. Any contributor may set it; nobody needs permission to
make something less public. Use it for shrines on private ground, sites a
community asks not be listed, anything you are unsure about.

### Description
`summary`, `sections` (compiled from articles), `article_refs` — external prose
with its own licence, referenced not absorbed.

### Media
`photos[]`: `{file|url, author, license, license_url, source, captured, consent}`.
`consent` is required for anything with a person in it.

### App-facing
For the driver app: `parking`, `gate_hours`, `driver_notes`, `access`.
For tours: `walk_cluster`, `story_hook`, `visit_minutes`.
These are *authored*, never crawled — that is why they live here and not in a
scraper.

---

## Coverage is an object, not an assumption

`_meta/coverage.md` declares what has been looked for, where, by what method.
Without it, an absent record is ambiguous between *out of scope*, *not in the
source*, and *nobody has written it yet* — and those need three different
responses.

This is not hypothetical. วัดศรีดอนมูล was "missing" for weeks. It was not
dropped by dedup or geocoding; Phayao province was simply never in the crawl
list. Nothing in the system could say so. Meanwhile the Saraphi temple of the
same name is absent from OpenStreetMap entirely — no crawl will ever produce it,
and only a person writing a note will.

Same symptom, three different causes, three different fixes. Coverage is what
tells them apart.
