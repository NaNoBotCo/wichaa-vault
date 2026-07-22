#!/usr/bin/env python3
"""validate.py — QA over the vault. Zero dependencies.

    python3 scripts/validate.py            # summary + gap counts
    python3 scripts/validate.py --gaps     # list every note behind each gap
    python3 scripts/validate.py --strict   # exit 1 if any ERROR (for the publish gate)

Parses the frontmatter subset the vault actually uses (scalars, block lists,
inline maps) rather than pulling in PyYAML — the surrounding projects are
stdlib-only and a schema validator that itself needs installing is a validator
that stops being run.

Two classes of finding:
  ERROR — the note is malformed or asserts something impossible. Blocks publish.
  GAP   — the note is fine, something is simply not known yet. This is the
          useful output: gaps are the quest list, and a gap that nobody can see
          is indistinguishable from a fact nobody recorded.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PLACES = HERE / "places"
VOCAB = HERE / "_meta" / "vocab" / "place-types.md"

VALID_CONFIDENCE = {"verified", "reported", "crawled", "heuristic"}
VALID_PRECISION = {"exact", "block", "area"}
REQUIRED = ["id", "lat", "lng", "confidence"]
# Generous Lanna/SE-Asia envelope — a coordinate outside this is a bug, not a place.
LAT = (5.0, 29.0)
LNG = (92.0, 110.0)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "no frontmatter"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unterminated frontmatter"
    body = text[3:end]
    out, key = {}, None
    for raw in body.splitlines():
        line = raw.split("   #")[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^\s+- ", line):                    # block list item
            if key is None:
                return None, f"list item before any key: {raw!r}"
            out.setdefault(key, [])
            if isinstance(out[key], list):
                # list items may themselves be inline maps ({type: osm, ref: …});
                # parsing them as scalars made every source unreadable and
                # produced 485 phantom "provenance cites unknown source" errors.
                out[key].append(_inline(line.strip()[2:]))
            continue
        if re.match(r"^\s+\S+:", line):                  # nested map entry
            k, _, v = line.strip().partition(":")
            if isinstance(out.get(key), dict):
                out[key][k.strip()] = _inline(v.strip())
            continue
        m = re.match(r"^([A-Za-z_][\w]*):(.*)$", line)
        if not m:
            return None, f"unparseable line: {raw!r}"
        key, rest = m.group(1), m.group(2).strip()
        if rest == "":
            out[key] = {} if key in ("provenance",) else []
        else:
            out[key] = _inline(rest)
    return out, None


def _scalar(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('\\"', '"')
    if s in ("true", "false"):
        return s == "true"
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    return s


def _inline(s):
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        d = {}
        for part in re.split(r",\s*(?=[A-Za-z_]+:)", s[1:-1]):
            if ":" in part:
                k, _, v = part.partition(":")
                d[k.strip()] = _scalar(v)
        return d
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in inner.split(",")] if inner else []
    return _scalar(s)


def vocab_keys():
    if not VOCAB.exists():
        return set()
    return set(re.findall(r"^\s*-\s*key:\s*(\S+)", VOCAB.read_text(encoding="utf-8"), re.M))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    notes = sorted(PLACES.glob("*.md"))
    if not notes:
        print("no notes in places/ — run scripts/migrate.py --write", file=sys.stderr)
        return 1
    known_types = vocab_keys()

    errors, gaps = [], {}

    def gap(name, nid):
        gaps.setdefault(name, []).append(nid)

    for f in notes:
        fm, err = parse_frontmatter(f.read_text(encoding="utf-8"))
        if err:
            errors.append((f.name, err))
            continue
        nid = fm.get("id") or f.stem

        for k in REQUIRED:
            if fm.get(k) in (None, ""):
                errors.append((f.name, f"missing required field: {k}"))
        lat, lng = fm.get("lat"), fm.get("lng")
        if isinstance(lat, (int, float)) and not (LAT[0] <= lat <= LAT[1]):
            errors.append((f.name, f"lat out of range: {lat}"))
        if isinstance(lng, (int, float)) and not (LNG[0] <= lng <= LNG[1]):
            errors.append((f.name, f"lng out of range: {lng}"))
        if fm.get("confidence") not in VALID_CONFIDENCE:
            errors.append((f.name, f"bad confidence: {fm.get('confidence')!r}"))
        if fm.get("geo_precision") not in VALID_PRECISION:
            errors.append((f.name, f"bad geo_precision: {fm.get('geo_precision')!r}"))
        if not fm.get("sources"):
            errors.append((f.name, "no sources — every fact must be traceable"))
        if fm.get("restricted") is True and not fm.get("restricted_reason"):
            errors.append((f.name, "restricted with no restricted_reason"))
        t = fm.get("type")
        if known_types and t and t not in known_types:
            gap("type not in vocabulary", nid)
        # provenance must point at a source the note actually declares
        srcs = {s.get("type") for s in fm.get("sources", []) if isinstance(s, dict)}
        for field, pv in (fm.get("provenance") or {}).items():
            if isinstance(pv, dict) and pv.get("source") not in srcs | {"field"}:
                errors.append((f.name, f"provenance[{field}] cites '{pv.get('source')}' "
                                       f"which is not in sources"))

        # ---- gaps: not errors, but the quest list -------------------------
        if not fm.get("name_th"):
            gap("no vernacular name", nid)
        if not fm.get("photo_count"):
            gap("no photograph", nid)
        if not fm.get("district"):
            gap("no district", nid)
        if not fm.get("gate_hours"):
            gap("no opening hours", nid)
        if not fm.get("article_langs"):
            gap("no description", nid)
        if fm.get("confidence") == "crawled":
            gap("never visited", nid)

    print(f"vault: {len(notes)} notes\n")
    print(f"ERRORS: {len(errors)}")
    for name, msg in errors[:20]:
        print(f"  ✗ {name}: {msg}")
    if len(errors) > 20:
        print(f"  … and {len(errors)-20} more")

    print(f"\nGAPS (the quest list — these are not defects):")
    for name, ids in sorted(gaps.items(), key=lambda kv: -len(kv[1])):
        pct = 100.0 * len(ids) / len(notes)
        print(f"  {len(ids):5d}  ({pct:4.1f}%)  {name}")
        if a.gaps:
            for i in ids[:15]:
                print(f"            {i}")
            if len(ids) > 15:
                print(f"            … {len(ids)-15} more")

    if a.json:
        (HERE / "_meta" / "gaps.json").write_text(
            json.dumps({"notes": len(notes), "errors": len(errors),
                        "gaps": {k: v for k, v in gaps.items()}}, ensure_ascii=False),
            encoding="utf-8")
        print("\n→ _meta/gaps.json")

    return 1 if (a.strict and errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())
