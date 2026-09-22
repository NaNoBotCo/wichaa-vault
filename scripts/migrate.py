#!/usr/bin/env python3
"""migrate.py — bring the compiled atlas into the vault as one note per place.

    python3 scripts/migrate.py            # dry run, prints what it would write
    python3 scripts/migrate.py --write

The point of this script is what it REFUSES to flatten. Each record is a
composite — coordinates from OSM, a heritage number from Wikidata, a photograph
from a Commons contributor, prose from Wikipedia — and the naive migration
stamps one `source:` on the note and loses which part came from where. That is
unrecoverable: afterwards you cannot tell what a machine asserted from what a
person witnessed, and the whole archive becomes as trustworthy as its weakest
field.

So: values are plain scalars (Obsidian-friendly, Dataview-queryable), and
`provenance:` records the origin of any field whose source differs from the
record default. Fields the crawl never supplied — gate_hours, driver_notes,
story_hook — are emitted empty and unprovenanced, which is honest: nobody has
said anything about them yet.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
WIKI = HERE.parent / "manuscript-wiki"
SRC = Path(os.environ.get("WATS_JSON", WIKI / "data" / "wats.geojson"))
DETAIL = Path(os.environ.get("WATS_DETAIL", WIKI / "data" / "wats-detail.json"))
OUT = HERE / "places"
# The temple register bridge (WW-1). A FRESH note for a bridged place is born
# with the register's facts; an EXISTING note gets them from enrich_registry.py,
# because this script never touches a note a person has edited. Both go through
# vaultlib's registry_* helpers, so they cannot disagree on names or provenance.
BRIDGE = Path(os.environ.get("WAT_BRIDGE", WIKI / "data" / "wat_bridge.json"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vaultlib import load_bridge, registry_facts, registry_provenance, registry_source  # noqa: E402
_BRIDGE_PLACES, _BRIDGE_FETCHED = load_bridge(BRIDGE)

# Which source a field came from, when the crawl produced it. Anything not listed
# inherits the record default; anything a human later edits gets `field`.
FIELD_SOURCE = {
    "heritage_reg": "wikidata",
    "founded": "wikidata",
    "summary": "wikipedia",
}
# Authored-only fields. Emitted empty so the note shows what is unanswered,
# never guessed at.
# Authored-only. `gate_hours` is deliberately separate from the crawled
# `opening_hours`: one is what a person observed at the gate, the other is what a
# mapper typed. Merging them would make a field observation indistinguishable
# from an OSM tag, which is the whole thing this schema refuses to do.
AUTHORED = ["parking", "gate_hours", "access", "driver_notes",
            "walk_cluster", "story_hook", "visit_minutes"]


def yaml_scalar(v):
    if v is None or v == "":
        return '""'
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    # A STRING that looks like a number must be quoted, or vaultlib.scalar reads
    # it back as int and the leading zero is gone: `phone: 0815955951` compiled to
    # the integer 815955951 in wats.geojson (found 2026-08-19 while adding the
    # temple register's `wat_code`, which is eleven digits starting with 0).
    if re.fullmatch(r"-?\d+(\.\d+)?", s) or s in ("true", "false", "null", "~"):
        return '"' + s + '"'
    if re.search(r'[:#\-\[\]{},&*?|>%@`"\n]', s) or s.strip() != s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def yaml_list(items, indent=2):
    if not items:
        return " []"
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}- {i}" for i in items)


def note_for(p, det, kind):
    pid = p["id"]
    sources = p.get("sources") or []
    default_src = (sources[0] or {}).get("type") if sources else "crawled"

    # per-field provenance, only where it differs from the record default
    prov = {}
    for field, src in FIELD_SOURCE.items():
        present = {"heritage_reg": p.get("heritage"), "founded": p.get("founded"),
                   "summary": (p.get("summary") or {}).get("text")}.get(field)
        if present and src != default_src:
            ref = next((s.get("ref") for s in sources if s.get("type") == src), None)
            prov[field] = {"source": src, "ref": ref, "confidence": "crawled"}

    photos = det.get("photos") or p.get("photos") or []
    art = det.get("article") or {}

    # The Wikipedia article was cited in provenance but never declared in
    # sources[] — its URL and licence lived inside the summary object. A cited
    # source that isn't a declared source is exactly the traceability hole this
    # schema exists to close, so declare it.
    summ0 = p.get("summary") or {}
    if summ0.get("title"):
        sources = list(sources) + [{"type": "wikipedia", "ref": summ0.get("title"),
                                    "lang": summ0.get("lang"), "url": summ0.get("url")}]

    # The temple register, for a bridged place: four facts, a declared source,
    # per-field provenance. Same shape enrich_registry.py merges into old notes.
    breg = _BRIDGE_PLACES.get(pid) or {}
    reg_facts = registry_facts(breg) if breg else {}
    if reg_facts:
        sources = list(sources) + [registry_source(breg, _BRIDGE_FETCHED)]
        prov.update(registry_provenance(breg, _BRIDGE_FETCHED))

    L = ["---"]
    L.append(f"id: {yaml_scalar(pid)}")
    # Only put Thai in the Thai field. Several OSM records carry a romanised
    # string in `name` with no Thai at all; writing that into name_th would
    # assert a vernacular name we do not have.
    raw_name, raw_roman = p.get("name"), p.get("nameRoman")
    has_thai = bool(raw_name and re.search(r"[\u0E00-\u0E7F]", raw_name))
    name_th = raw_name if has_thai else ""
    name_roman = raw_roman or (raw_name if not has_thai else "")
    L.append(f"name_th: {yaml_scalar(name_th)}")
    L.append(f"name_roman: {yaml_scalar(name_roman)}")
    if not name_th:
        L.append("needs: [name_th]   # no vernacular name recorded — a contributor can add it")
    # Aliases start with what we have; the field exists so variants can be added
    # the moment anyone meets one. This is what stops a second spelling becoming
    # a second temple.
    al = [yaml_scalar(x) for x in {name_th, name_roman} if x]
    L.append("aliases:" + yaml_list(al))
    L.append(f"type: {yaml_scalar('wat' if kind == 'wat' else (p.get('siteType') or 'sacred_site').split(';')[0].strip().replace(' ', '_'))}")
    L.append(f"type_en: {yaml_scalar('Buddhist temple (monastery)' if kind == 'wat' else (p.get('siteType') or 'sacred site'))}")
    L.append(f"lat: {yaml_scalar(p.get('lat'))}")
    L.append(f"lng: {yaml_scalar(p.get('lng'))}")
    L.append(f"geo_precision: {yaml_scalar(p.get('geoPrecision') or 'block')}")
    L.append(f"province: {yaml_scalar(p.get('province'))}")
    L.append(f"district: {yaml_scalar(p.get('district'))}")
    L.append(f"subdistrict: {yaml_scalar(p.get('subdistrict'))}")
    L.append(f"street: {yaml_scalar(p.get('street'))}")
    L.append(f"heritage_reg: {yaml_scalar(p.get('heritage'))}")
    L.append(f"founded: {yaml_scalar(p.get('founded'))}")
    for rf, rv in reg_facts.items():          # wat_code / wat_sect / wat_rank / wat_founded_ce
        L.append(f"{rf}: {yaml_scalar(rv)}")
    L.append(f"status: {yaml_scalar(p.get('status') or 'active')}")
    # The one-line Wikidata gloss (CC0). Distinct from `summary`, which is the
    # Wikipedia lead and carries share-alike.
    L.append(f"description: {yaml_scalar(p.get('description'))}")
    # Contact and hours: recorded where a mapper bothered, never inferred.
    # Coverage is thin by nature — Thai wats are open dawn to dusk and mostly
    # publish nothing — so an empty value here means "not recorded", not "none".
    L.append(f"phone: {yaml_scalar(p.get('phone'))}")
    L.append(f"email: {yaml_scalar(p.get('email'))}")
    L.append(f"website: {yaml_scalar(p.get('website'))}")
    L.append(f"opening_hours: {yaml_scalar(p.get('openingHours'))}")
    L.append(f"confidence: {yaml_scalar(p.get('confidence') or 'crawled')}")
    L.append("restricted: false")
    L.append('restricted_reason: ""')
    for f in AUTHORED:
        L.append(f'{f}: ""')
    L.append("sources:")
    for s in sources:
        bits = ", ".join(f"{k}: {yaml_scalar(v)}" for k, v in s.items() if v)
        L.append(f"  - {{{bits}}}")
    if prov:
        L.append("provenance:")
        for f, v in prov.items():
            bits = ", ".join(f"{k}: {yaml_scalar(x)}" for k, x in v.items() if x)
            L.append(f"  {f}: {{{bits}}}")
    L.append(f"photo_count: {len(photos)}")
    L.append(f"article_langs:" + yaml_list(sorted(art.keys())))
    L.append("---")
    L.append("")
    L.append(f"# {name_roman or name_th or pid}")
    if name_th and name_th != name_roman:
        L.append(f"*{name_th}*")
    L.append("")

    summ = (p.get("summary") or {})
    if summ.get("text"):
        L.append(summ["text"])
        L.append("")
        L.append(f"> Source: [{summ.get('title')}]({summ.get('url')}) — {summ.get('license')}")
        L.append("")

    if photos:
        L.append("## Photographs")
        for m in photos:
            L.append(f"- [{m.get('author')}]({m.get('source')}) — {m.get('license')}"
                     + (" *(public domain)*" if m.get("publicDomain") else ""))
        L.append("")

    # The body is the narrative layer. Everything above is machine-derived; this
    # is where a person writes what a crawl cannot reach.
    L.append("## Notes")
    L.append("")
    L.append("<!-- Field notes go here. Anything you write below is yours, not the")
    L.append("     crawler's — set confidence: verified and add a field source when")
    L.append("     you have stood in front of it. -->")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    if not SRC.exists():
        print(f"ERROR: {SRC} not found — run sync_wats.py in manuscript-wiki first", file=sys.stderr)
        return 1
    d = json.loads(SRC.read_text(encoding="utf-8"))
    detail = json.loads(DETAIL.read_text(encoding="utf-8")) if DETAIL.exists() else {}

    records = [(w, "wat") for w in d.get("wats", [])] + \
              [(x, "sacred") for x in d.get("sacred", [])]
    if a.limit:
        records = records[:a.limit]

    OUT.mkdir(parents=True, exist_ok=True)
    written = skipped = 0
    for p, kind in records:
        pid = p.get("id")
        if not pid:
            continue
        path = OUT / f"{pid}.md"
        # Never clobber a note a human has touched. The vault is the system of
        # record for authored fields; re-running migration must not overwrite them.
        if path.exists() and "field" in path.read_text(encoding="utf-8"):
            skipped += 1
            continue
        body = note_for(p, detail.get(pid) or {}, kind)
        if a.write:
            path.write_text(body, encoding="utf-8")
        written += 1

    print(f"{'wrote' if a.write else 'would write'} {written} notes"
          + (f", skipped {skipped} with field edits" if skipped else ""))
    if not a.write:
        print("  (dry run — pass --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
