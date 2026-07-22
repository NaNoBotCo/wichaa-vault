#!/usr/bin/env python3
"""compile.py — vault → the published JSON layer. Closes the loop.

    python3 scripts/compile.py                 # dry run, prints what would change
    python3 scripts/compile.py --write

Until this existed the vault was a mirror: notes were generated FROM the atlas
and nothing carried an edit back, so anything typed in Obsidian drifted silently
away from the site. After this, the vault is the system of record for identity
and for every authored field, and the site is downstream of it.

WHAT THE VAULT OWNS vs WHAT IT DOESN'T
The vault owns identity (id, names, aliases, type), place, status, and every
authored field — gate_hours, driver_notes, story_hook, restricted. Those are
things a person asserts.

It does NOT own the bulky regenerable payloads: 871 Commons photographs with
per-image licences, and 531 sections of Wikipedia prose. Nobody hand-authors
those, they are reproducible from a crawl at any time, and pasting them into
markdown would make every note unreadable while adding nothing. They stay in the
crawl sidecar and are joined here by id.

That split is worth stating plainly rather than letting "system of record" imply
more than it means: **the vault is authoritative for what a person asserts, the
crawl is authoritative for what it fetched, and a conflict resolves to the
vault** — because the only reason a human field differs from a crawled one is
that a human corrected it.

OUTPUTS
  wats.geojson        the map payload (lean: 2 photos, lead paragraph)
  wats-detail.json    full photos + full sectioned articles, per id
  coverage.json       scope as machine-readable data — what was looked for, where
  place-types.json    the emic vocabulary, with each term's own confidence

The last two are new. Scope and vocabulary have been prose in _meta/ that only a
human could read; publishing them means an agent can tell an absence from a gap,
and can see that san_phra_phum and san_chao_thi are different things, without
anyone explaining it.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vaultlib import load_notes, vocab_terms, parse_frontmatter  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
PLACES = HERE / "places"
META = HERE / "_meta"
WIKI = HERE.parent / "manuscript-wiki"

MAP_PHOTOS = 2
AUTHORED = ["parking", "gate_hours", "access", "driver_notes",
            "walk_cluster", "story_hook", "visit_minutes"]


def coverage_data():
    """The yaml block inside _meta/coverage.md, as data."""
    f = META / "coverage.md"
    if not f.is_file():
        return {}
    m = re.search(r"```yaml\n(.*?)```", f.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}
    # coverage.md's block is a list of scopes under one key; parse with the same
    # narrow reader by wrapping it as frontmatter.
    fm, err = parse_frontmatter("---\n" + m.group(1) + "\n---\n")
    if err:
        print(f"  ! coverage.md: {err}", file=sys.stderr)
        return {}
    return fm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=str(WIKI / "data"))
    ap.add_argument("--detail-src", default=str(WIKI / "data" / "wats-detail.json"))
    a = ap.parse_args()

    out_dir = Path(a.out)
    detail_src = Path(a.detail_src)
    crawl_detail = json.loads(detail_src.read_text(encoding="utf-8")) if detail_src.exists() else {}

    notes = load_notes(PLACES)
    if not notes:
        print("no notes — run scripts/migrate.py --write first", file=sys.stderr)
        return 1

    bad = [(f.name, e) for f, _, _, e in notes if e]
    if bad:
        print(f"✗ {len(bad)} note(s) failed to parse — refusing to compile:", file=sys.stderr)
        for n, e in bad[:10]:
            print(f"    {n}: {e}", file=sys.stderr)
        return 1

    wats, sacred, detail = [], [], {}
    n_restricted = n_authored = 0

    for f, fm, body, _ in notes:
        pid = fm.get("id") or f.stem

        # `restricted` withholds from publication without deleting. Anyone may set
        # it; nobody needs permission to make something less public.
        if fm.get("restricted") is True:
            n_restricted += 1
            continue

        det = crawl_detail.get(pid) or {}
        photos = det.get("photos") or []
        article = det.get("article") or {}

        rec = {
            "id": pid,
            "name": fm.get("name_th") or fm.get("name_roman") or "",
            "nameRoman": fm.get("name_roman") or "",
            "aliases": fm.get("aliases") or [],
            "type": fm.get("type") or "",
            "typeEn": fm.get("type_en") or "",
            "lat": fm.get("lat"),
            "lng": fm.get("lng"),
            "geoPrecision": fm.get("geo_precision") or "block",
            "province": fm.get("province") or "",
            "district": fm.get("district") or "",
            "subdistrict": fm.get("subdistrict") or "",
            "street": fm.get("street") or "",
            "heritage": fm.get("heritage_reg") or "",
            "founded": fm.get("founded") or "",
            "status": fm.get("status") or "active",
            "description": fm.get("description") or "",
            "phone": fm.get("phone") or "",
            "email": fm.get("email") or "",
            "website": fm.get("website") or "",
            "openingHours": fm.get("opening_hours") or "",
            "confidence": fm.get("confidence") or "crawled",
            "sources": fm.get("sources") or [],
            "photoCount": len(photos),
            "photos": photos[:MAP_PHOTOS],
        }
        if fm.get("provenance"):
            rec["provenance"] = fm["provenance"]

        # Authored fields ride in the payload only when someone has actually said
        # something. An empty string published as a value reads like an assertion
        # that the answer is blank.
        authored = {k: fm[k] for k in AUTHORED if fm.get(k)}
        if authored:
            rec.update(authored)
            n_authored += 1

        # the lead paragraph, taken from the note body (which migrate seeded and a
        # human may since have rewritten — the vault wins)
        # Accumulate prose paragraphs up to the budget rather than stopping at the
        # first blank line: 5 Wikipedia leads contain an internal paragraph break,
        # and taking only the first paragraph silently truncated them (one went
        # 625 → 238 characters).
        parts, used = [], 0
        for para in body.split("\n\n"):
            t = para.strip()
            if not t or t.startswith(("#", ">", "<!--", "-", "*")):
                if parts:
                    break                  # prose block has ended
                continue
            parts.append(t)
            used += len(t)
            if used >= 700:
                break
        lead = "\n\n".join(parts)
        art_any = article.get("th") or article.get("en") or {}
        if lead:
            rec["summary"] = {"text": lead[:700],
                              "title": art_any.get("title"), "url": art_any.get("url"),
                              "lang": art_any.get("lang"),
                              "license": art_any.get("license"),
                              "licenseUrl": art_any.get("licenseUrl")}
            rec["summary"] = {k: v for k, v in rec["summary"].items() if v}

        if photos or article:
            d = {}
            if photos:
                d["photos"] = photos          # complete list; map payload trims
            if article:
                d["article"] = article
            if d:
                detail[pid] = d

        (sacred if fm.get("type") not in ("wat",) and fm.get("type_en", "").lower().find("temple") < 0
         else wats).append(rec)

    wats.sort(key=lambda w: (0 if w["heritage"] else 1, w["nameRoman"] or w["name"]))
    sacred.sort(key=lambda w: (0 if w["photos"] else 1, w["nameRoman"] or w["name"]))

    payload = {
        "wats": wats,
        "sacred": sacred,
        "total": len(wats),
        "sacredTotal": len(sacred),
        "heritage": sum(1 for w in wats if w["heritage"]),
        "withPhotos": sum(1 for w in wats if w["photoCount"]),
        "photos": sum(w["photoCount"] for w in wats),
        "sacredPhotos": sum(w["photoCount"] for w in sacred),
        "download": True,
        "source": "wichaa-vault",
        "attribution": {
            "data": "© OpenStreetMap contributors, ODbL 1.0 (share-alike)",
            "dataUrl": "https://opendatacommons.org/licenses/odbl/1-0/",
            "facts": "Wikidata, CC0",
            "photos": "Wikimedia Commons — each image credited to its author under its own licence",
        },
    }

    cov = coverage_data()
    vocab = vocab_terms(META / "vocab" / "place-types.md")

    targets = {
        out_dir / "wats.geojson": payload,
        out_dir / "wats-detail.json": detail,
        out_dir / "coverage.json": cov,
        out_dir / "place-types.json": {"terms": vocab, "count": len(vocab),
                                       "note": "The emic term is the identity; en_gloss is a "
                                               "convenience translation and carries no authority."},
    }

    print(f"vault: {len(notes)} notes → {len(wats)} wats + {len(sacred)} sacred")
    print(f"  restricted, withheld from publication: {n_restricted}")
    print(f"  notes carrying an authored field:      {n_authored}")
    print(f"  vocabulary terms:                      {len(vocab)}")
    print(f"  coverage scopes:                       {len(cov.get('scopes') or [])}")
    for p, obj in targets.items():
        blob = json.dumps(obj, ensure_ascii=False)
        old = p.read_text(encoding="utf-8") if p.exists() else None
        state = "unchanged" if old == blob else ("new" if old is None else "CHANGED")
        print(f"  {'→' if a.write else ' '} {p.name:22s} {len(blob)//1024:>6} KB  {state}")
        if a.write:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(blob, encoding="utf-8")
    if not a.write:
        print("\n  (dry run — pass --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
