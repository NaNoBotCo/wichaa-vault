#!/usr/bin/env python3
"""vaultlib — read the vault. Zero dependencies.

Shared by validate.py and compile.py. Two copies of a frontmatter parser is two
things to drift apart, and drift between the validator and the compiler is the
worst kind: the QA pass would bless notes the publisher then mangles.

Parses the YAML subset the vault actually emits — scalars, block lists, inline
maps, nested maps. Not general YAML, on purpose: a narrow parser that fails
loudly on anything unexpected beats a permissive one that guesses.
"""
import re
from pathlib import Path


def scalar(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if s in ("true", "false"):
        return s == "true"
    if s in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    return s


def inline(s):
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        d = {}
        for part in re.split(r",\s*(?=[A-Za-z_][\w]*\s*:)", s[1:-1]):
            if ":" in part:
                k, _, v = part.partition(":")
                d[k.strip()] = scalar(v)
        return d
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [scalar(x) for x in inner.split(",")] if inner else []
    return scalar(s)


def parse_frontmatter(text):
    """→ (dict, None) or (None, reason)."""
    if not text.startswith("---"):
        return None, "no frontmatter"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unterminated frontmatter"
    out, key = {}, None
    for raw in text[3:end].splitlines():
        line = raw.split("   #")[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^\s+- ", line):
            if key is None:
                return None, f"list item before any key: {raw!r}"
            out.setdefault(key, [])
            if isinstance(out[key], list):
                out[key].append(inline(line.strip()[2:]))
            continue
        if re.match(r"^\s+\S+:", line):
            k, _, v = line.strip().partition(":")
            if isinstance(out.get(key), dict):
                out[key][k.strip()] = inline(v.strip())
            continue
        m = re.match(r"^([A-Za-z_][\w]*):(.*)$", line)
        if not m:
            return None, f"unparseable line: {raw!r}"
        key, rest = m.group(1), m.group(2).strip()
        out[key] = {} if rest == "" and key == "provenance" else ([] if rest == "" else inline(rest))
    return out, None


def body_of(text):
    """Everything after the frontmatter — the narrative layer."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text[end + 4:].lstrip("\n") if end != -1 else ""


def load_notes(places: Path):
    """→ [(path, frontmatter, body, error)]. Never raises on a bad note; the
    caller decides whether a parse failure blocks publishing."""
    out = []
    for f in sorted(places.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, err = parse_frontmatter(text)
        out.append((f, fm or {}, body_of(text), err))
    return out


def vocab_terms(vocab_md: Path):
    """The place-type vocabulary as data. Parsed out of the fenced yaml blocks in
    the vocabulary note so the note stays the single human-editable source."""
    if not vocab_md.is_file():
        return []
    text = vocab_md.read_text(encoding="utf-8")
    terms, cur = [], None
    for block in re.findall(r"```yaml\n(.*?)```", text, re.S):
        for line in block.splitlines():
            m = re.match(r"^-\s+key:\s*(\S+)", line)
            if m:
                if cur:
                    terms.append(cur)
                cur = {"key": m.group(1)}
                continue
            m = re.match(r"^\s+([a-z_]+):\s*(.*)$", line)
            if m and cur is not None:
                k, v = m.group(1), m.group(2).strip()
                if v in (">", "|"):
                    cur[k] = ""            # folded block; body lines follow
                    cur["_folding"] = k
                elif v:
                    cur.pop("_folding", None)
                    cur[k] = scalar(v)
                continue
            if cur is not None and cur.get("_folding") and line.strip():
                k = cur["_folding"]
                cur[k] = (cur[k] + " " + line.strip()).strip()
    if cur:
        terms.append(cur)
    for t in terms:
        t.pop("_folding", None)
    return terms
