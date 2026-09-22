---
kind: vocabulary
axis: motif
updated: 2026-07-22
---

# Motif — ลาย, the ornamental grammar

The emic term is the identity. English is a gloss offered for convenience and
carries no authority.

This axis exists because **ornament is how an object declares which workshop
tradition made it**, and no catalogue field currently records it. A manuscript
cover, an amulet's frame, a ho trai gable, the edge of a tung banner and a
Lazada listing photograph can all carry the same named unit. A record that says
`type: phap_sa manuscript` and stops has thrown away the one attribute that
would let a machine notice that two objects three centuries apart were drawn
from the same pattern book.

**Read the Central/Lanna caveat before using this file.** It opens with กระจัง
because a Central Thai teaching chart was contributed, and กระจัง is
Rattanakosin nomenclature — the vocabulary of the Bangkok craft schools. Whether
Lanna craftsmen name these same five forms, name them differently, or cut the
family at different joints is **unverified**, and it is the first and largest
gap on this axis. Do not let the Central terms become the default that Lanna
gets described as a deviation from. That is the exact failure
`_meta/coverage.md` and the place-type decision exist to outrun.

Every entry declares its own `confidence`. Terms marked `needs_verification`
were written from model training knowledge and have **not** been checked against
a source — a starting point for someone who knows, not an assertion.

---

## Structural terms

```yaml
- key: mae_lai
  term: แม่ลาย
  roman: mae lai
  en_gloss: mother-motif; the base pattern a family of variants derives from
  confidence: high
  definition: >
    The parent form of a motif family. Variants are understood as elaborations
    of one envelope rather than as separate designs — the teaching chart that
    opened this file is titled แม่ลายกระจัง, "the mother-motif krachang", and
    shows five fillings of a single silhouette.
  note: >
    This is itself a taxonomic term the tradition supplies about its own
    ornament, and it maps cleanly onto a parent/child node relation. Prefer it
    to any imported word like "family" or "genus" when modelling this axis.

- key: krong_lai
  term: โครงลาย
  roman: khrong lai
  en_gloss: the construction grid a motif is built inside
  confidence: medium
  needs_verification: true
  definition: >
    The ruled square or rectangle, halved and quartered, that fixes a motif's
    proportions before any curve is drawn. Visible under the chalk in every
    panel of the contributed chart.
  note: >
    Term recorded from training knowledge; the grid itself is observed directly
    in the source image. Confirm the word with a practising craftsman before
    relying on it.
```

---

## กระจัง — the krachang family

```yaml
- key: krachang
  term: กระจัง
  roman: krachang
  en_gloss: upright tapering border motif
  confidence: high
  parent: null
  members: [krachang_fan_pla, krachang_ta_oi, krachang_bai_thet, krachang_patiyan, krachang_ruan]
  definition: >
    A motif family whose unit is a single upright form, broad at the base and
    drawn to a point, built inside a square. Used in repeating runs along an
    edge or as a crest, and as a moulded register on pedestals and bases.
    Distinct from the กนก (kanok) flame-scroll family, which is a running curve
    rather than a discrete upright unit.
  distinct_from: [kanok]
  uses_reported:
    - moulded register on a Buddha image pedestal (ฐานกระจัง)
    - crest along a wall coping, boat prow, door and window frames
    - the toothed edge of a banner or applied metalwork
  note: >
    uses_reported is model knowledge, not catalogued observation — treat every
    line as needs_verification until an item in the corpus is tagged with it.
```

### Members

```yaml
- key: krachang_fan_pla
  term: กระจังฟันปลา
  roman: krachang fan pla
  en_gloss: fish-tooth krachang
  parent: krachang
  confidence: high
  definition: >
    The plainest member. A near-straight-sided triangle with a shallow notched
    skirt at the base and almost no interior articulation. Run in series it
    reads as a saw-tooth.
  literal: >
    ฟันปลา — "fish teeth", describing the silhouette of the repeated run rather
    than the single unit.

- key: krachang_ta_oi
  term: กระจังตาอ้อย
  roman: krachang ta oi
  en_gloss: sugarcane-eye krachang
  parent: krachang
  confidence: high
  definition: >
    A pointed hood enclosing one plain teardrop bud at the centre, with a small
    pair of lobes springing at the base. One interior element only — the step up
    from ฟันปลา is that the inside of the envelope is now occupied.
  literal: >
    ตาอ้อย — the "eye", the node on a sugarcane stalk, named for the shape of
    the central bud.

- key: krachang_bai_thet
  term: กระจังใบเทศ
  roman: krachang bai thet
  en_gloss: foreign-leaf krachang
  parent: krachang
  confidence: high
  definition: >
    A compound leaf form. The central bud is repeated at diminishing scale up
    the axis and flanked by paired outward-curling side lobes that fill the
    lower corners of the square.
  literal: >
    เทศ — "foreign", the standing Thai qualifier for an imported form. The
    conventional reading is that the leaf is acanthus-derived, arriving through
    Indian intermediaries.
  needs_verification: true
  note: >
    The name is certain; the acanthus derivation is the received account and is
    recorded here as such, not as fact. Worth chasing — if true it is a dated
    transmission event visible in the ornament itself.

- key: krachang_patiyan
  term: กระจังปฏิญาณ
  roman: krachang patiyan
  en_gloss: patiyan krachang
  parent: krachang
  confidence: medium
  needs_verification: true
  definition: >
    The fully developed symmetrical form: a tiered central axis of nested buds
    with two or more ranks of side branches curling out and down, the lowest
    ranks breaking outside the base line of the square.
  literal: >
    ปฏิญาณ — in ordinary Thai, "a vow, a pledge" (Pali paṭiññā). Why the motif
    carries the word is not established here.
  note: >
    Name and form both taken from the contributed chart. The etymology is the
    open question — do not repeat a guess about it in published copy.

- key: krachang_ruan
  term: กระจังรวน
  roman: krachang ruan
  en_gloss: leaning krachang
  parent: krachang
  confidence: medium
  needs_verification: true
  definition: >
    The asymmetric member. The same compound vocabulary as ปฏิญาณ, but the axis
    tilts and the tip hooks to one side, so the unit no longer sits square in
    its frame.
  literal: >
    รวน — "out of true, irregular, thrown out of order".
  use_claimed: >
    Reported use is at corners and along sloping runs, where a strictly upright
    unit would not follow the line. This is inference from the form, not a
    sourced claim.
```

---

## Lanna hook

```yaml
- key: lai_kham
  term: ลายคำ
  roman: lai kham
  en_gloss: gold-leaf stencil ornament on lacquer
  confidence: high
  tradition: lanna
  definition: >
    Northern gold-on-lacquer decorative work — designs laid in gold leaf over
    black or red lacquer on temple walls, pillars, panels, chests and
    manuscript boxes.
  anchor: >
    วิหารลายคำ at Wat Phra Singh, Chiang Mai, is named for the technique.
  note: >
    Recorded here as the entry point to the Lanna side of this axis. ลายคำ is a
    technique term rather than a motif name, so it is the wrong shape to sit
    beside กระจัง — which is itself evidence that the two traditions do not cut
    ornament along the same joint. Resolving that is the work.
```

---

## Sources

```yaml
- ref: chart-mae-lai-krachang
  type: contributed
  medium: chalkboard teaching chart, photographed
  credited_to: ปรีชา คำผาย
  channel: Facebook
  url: null
  received: 2026-07-22
  received_via: shared in conversation by the archivist
  covers: [krachang, krachang_fan_pla, krachang_ta_oi, krachang_bai_thet, krachang_patiyan, krachang_ruan]
  confidence: reported
  note: >
    A competent art teacher's board, not a published reference. It is sound
    evidence for the five names and their forms and is the sole source for
    ปฏิญาณ and รวน here. No URL was captured and the image is not yet in the
    vault — both are outstanding.
```

## Gaps on this axis

1. **Lanna nomenclature.** Whether these five forms are named in the North, and
   what the Northern ornament vocabulary cuts instead. Blocking — everything
   above is Central until answered.
2. **The chart image.** Not held. Capture the file and the original post URL
   before the post ages off.
3. **ปฏิญาณ etymology.** Unexplained.
4. **ใบเทศ derivation.** The acanthus account is received, not verified.
5. **No item is tagged yet.** This vocabulary is unattached — nothing in the
   catalogue points at it. It stays a wish list until a manuscript cover or an
   amulet frame carries `motif: krachang_bai_thet`.
