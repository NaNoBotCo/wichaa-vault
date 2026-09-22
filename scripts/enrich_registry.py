#!/usr/bin/env python3
"""enrich_registry.py — carry the temple register's facts into the vault notes.

    python3 scripts/enrich_registry.py            # dry run: what would change
    python3 scripts/enrich_registry.py --write    # merge into places/*.md

WW-1 step 3 of manuscript-wiki/WORKORDERS-GEMBA-2026-08.md. The ONAB register
(B.E. 2567) is stamped on 6,203 manuscripts as `wat_code`; bridge_wat_registry.py
joined 58 of those codes to vault places and wrote
manuscript-wiki/data/wat_bridge.json. This script puts the register's own facts
— code, nikaya, rank, founding year — onto those 58 notes, with a declared
`onab_register` source and per-field provenance, so compile.py carries them into
wats.geojson / api/wats.json and the vault stays the system of record.

WHY NOT migrate.py. migrate.py regenerates a note wholesale from the crawl and
refuses to touch any note a person has edited (it looks for `field` provenance).
Every one of the 58 bridged notes is such a note — they all carry the 2026-08-09
province fix — so migrate reaches none of them. This script is the other half:
a MERGE that edits only the lines it owns and leaves every other byte alone.
migrate.py emits the same fields for fresh notes; both read vaultlib's
registry_* helpers, so the field names and provenance shape cannot drift.

RULES
  - Idempotent: a second run changes nothing.
  - Owns exactly: wat_code / wat_sect / wat_rank / wat_founded_ce lines, one
    `{type: onab_register, …}` item in sources[], and the four matching
    provenance entries. Never rewrites, reorders or reformats anything else.
  - A note that is not in the bridge is not opened.
  - Run validate.py --strict afterwards (the publish gate does too).
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from vaultlib import (REGISTRY_FIELDS, REGISTRY_SOURCE, load_bridge,  # noqa: E402
                      registry_facts, registry_provenance, registry_source)
from migrate import yaml_scalar  # noqa: E402  (the vault's one scalar formatter)

VAULT = HERE.parent
PLACES = VAULT / "places"
BRIDGE = VAULT.parent / "manuscript-wiki" / "data" / "wat_bridge.json"


def inline_map(d):
    return "{" + ", ".join(f"{k}: {yaml_scalar(v)}" for k, v in d.items() if v not in (None, "")) + "}"


def split_frontmatter(lines):
    """→ (start, end) indexes of the frontmatter body (exclusive of the --- fences),
    or None if the note has no frontmatter."""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 1, i
    return None


def merge(text, rec, fetched):
    """Return the merged note text (unchanged text if nothing to do)."""
    lines = text.split("\n")
    span = split_frontmatter(lines)
    if not span:
        return text, ["no frontmatter — skipped"]
    a, b = span
    fm = lines[a:b]
    notes = []

    facts = registry_facts(rec)
    if not facts:
        return text, ["bridge record carries no register facts — skipped"]

    # ---- 1. the four scalar fields ---------------------------------------------
    def top_idx(key):
        for i, ln in enumerate(fm):
            if re.match(rf"^{re.escape(key)}:", ln):
                return i
        return None

    want = {f: f"{f}: {yaml_scalar(v)}" for f, v in facts.items()}
    missing = []
    for f in REGISTRY_FIELDS:
        if f not in want:
            continue
        i = top_idx(f)
        if i is None:
            missing.append(want[f])
        elif fm[i] != want[f]:
            notes.append(f"update {f}")
            fm[i] = want[f]
    if missing:
        # insert as one block after `founded:` (every migrate-born note has it);
        # fall back to just before `status:`, then before `sources:`, then the end
        at = top_idx("founded")
        at = at + 1 if at is not None else None
        if at is None:
            for anchor in ("status", "sources"):
                j = top_idx(anchor)
                if j is not None:
                    at = j
                    break
        if at is None:
            at = len(fm)
        fm[at:at] = missing
        notes.append("add " + ", ".join(m.split(":")[0] for m in missing))

    # ---- 2. sources[] gains (or refreshes) the register entry --------------------
    src_line = "  - " + inline_map(registry_source(rec, fetched))
    si = top_idx("sources")
    if si is None:
        # no sources block at all — create one before provenance/photo_count/end
        at = top_idx("provenance")
        if at is None:
            at = top_idx("photo_count")
        if at is None:
            at = len(fm)
        fm[at:at] = ["sources:", src_line]
        notes.append("add sources[] with onab_register")
    else:
        j = si + 1
        found = None
        while j < len(fm) and fm[j].startswith("  - "):
            if f"type: {REGISTRY_SOURCE}" in fm[j]:
                found = j
            j += 1
        if found is None:
            fm[j:j] = [src_line]
            notes.append("add onab_register to sources[]")
        elif fm[found] != src_line:
            fm[found] = src_line
            notes.append("refresh onab_register source")

    # ---- 3. provenance entries, one per register field ---------------------------
    prov = registry_provenance(rec, fetched)
    want_p = {f: f"  {f}: {inline_map(v)}" for f, v in prov.items()}
    pi = top_idx("provenance")
    if pi is None:
        at = top_idx("photo_count")
        if at is None:
            at = len(fm)
        fm[at:at] = ["provenance:"] + [want_p[f] for f in REGISTRY_FIELDS if f in want_p]
        notes.append("add provenance block")
    else:
        # the block is every following line that is indented and not a list item
        j = pi + 1
        idx = {}
        while j < len(fm) and re.match(r"^\s+\S", fm[j]) and not fm[j].lstrip().startswith("- "):
            m = re.match(r"^\s+([A-Za-z_][\w]*):", fm[j])
            if m:
                idx[m.group(1)] = j
            j += 1
        end = j
        added = []
        for f in REGISTRY_FIELDS:
            if f not in want_p:
                continue
            if f in idx:
                if fm[idx[f]] != want_p[f]:
                    fm[idx[f]] = want_p[f]
                    notes.append(f"update provenance[{f}]")
            else:
                added.append(want_p[f])
        if added:
            fm[end:end] = added
            notes.append("add provenance for " + ", ".join(x.strip().split(":")[0] for x in added))

    new = lines[:a] + fm + lines[b:]
    return "\n".join(new), notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="apply (default is a dry run)")
    ap.add_argument("--bridge", default=str(BRIDGE))
    ap.add_argument("--only", help="one place id, for a look")
    a = ap.parse_args()

    places, fetched = load_bridge(Path(a.bridge))
    if not places:
        print(f"no bridge at {a.bridge} — nothing to merge (run manuscript-wiki/scripts/"
              f"bridge_wat_registry.py first)", file=sys.stderr)
        return 1

    changed = unchanged = absent = 0
    for pid, rec in sorted(places.items()):
        if a.only and pid != a.only:
            continue
        path = PLACES / f"{pid}.md"
        if not path.is_file():
            absent += 1
            print(f"  ✗ {pid}: bridged but no vault note")
            continue
        text = path.read_text(encoding="utf-8")
        new, notes = merge(text, rec, fetched)
        if new == text:
            unchanged += 1
            continue
        changed += 1
        print(f"  · {pid}: " + "; ".join(notes))
        if a.write:
            path.write_text(new, encoding="utf-8")

    verb = "merged into" if a.write else "would merge into"
    print(f"enrich_registry: {verb} {changed} note(s); {unchanged} already current"
          + (f"; {absent} bridged place(s) have no note" if absent else "")
          + f"  [register B.E. 2567 via bridge of {fetched}]")
    if not a.write and changed:
        print("  (dry run — pass --write, then run scripts/validate.py --strict)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
