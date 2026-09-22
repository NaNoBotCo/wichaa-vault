---
kind: vocabulary
axis: class
updated: 2026-07-22
---

# Class — the ontological *kind* of a sacred object

The emic term is the identity. English is a gloss offered for convenience and
carries no authority.

This axis records the one thing a sale listing almost never states and a model
trained on sale listings cannot recover: **does this object house a resident
entity, and if so of what tier?** A พระสมเด็จ and a กุมารทอง are sold on the same
page, in the same price band, with the same reverent language — and they are not
the same *kind of thing*. One is impersonal sacredness you may adopt blind. The
other is a bound spirit that must be fed, named, and released properly. That
difference is the whole of why provenance mattered two questions ago, and it is
exactly what flattens to "amulet" when the tradition is learned from the market.

Three fields do the load-bearing work, and they are what make the axis
queryable rather than merely descriptive:

- **resident** — `none` · `deva` · `raised_spirit` · `ghost` · `animated`.
  What, if anything, lives in the vessel.
- **upkeep** — `none` · `veneration` · `feeding` · `feeding_and_closing`.
  What the keeper owes it. This is the operational answer to "can I set it down?"
- **provenance_sensitivity** — `low` · `medium` · `high`. How much an unknown
  history should worry you. Derived from the two fields above, stated explicitly
  so a consumer need not derive it.

`members` lists the object-type terms that belong to each class — this is what
the scanner (`manuscript-crawler/tag_classes.py`) searches for in both corpora.
Boundaries are genuinely fuzzy in places; where a term could sit in two classes
it is flagged, not forced. Adding a class or moving a member is normal — see
[[project_taxonomy_nodes]].

Every entry declares its own `confidence`. `needs_verification: true` means it
was written from model training knowledge and has not been checked against a
Thai-language source.

---

## Impersonal-sacred — nobody home to feed

Power is held in consecration, inscription, or the material itself. No resident
entity, no relationship, no upkeep. **Safe to adopt with unknown provenance** —
this is the class the second-hand market is built on.

```yaml
- key: phra_khrueang
  term: พระเครื่อง
  roman: phra khrueang
  en_gloss: Buddhist amulet
  confidence: high
  resident: none
  upkeep: none
  provenance_sensitivity: low
  definition: >
    A votive Buddha image or famous-monk amulet. Power = the barami of the maker
    plus the consecration (ปลุกเสก). No occupant. Its provenance question is
    purely one of authenticity and market value, never of spiritual safety.
  members: [สมเด็จ, พระพุทธ, พระปิดตา, พระผง, พระกริ่ง, เหรียญหลวง, พระสมเด็จ]
  # สมเด็จ is both an amulet and the highest honorific in Thai. The amulet is
  # พระสมเด็จ; the honorific is องค์สมเด็จพระ… (the Buddha) and พระบาทสมเด็จพระ…
  # (the King). Word ORDER separates them, and 438 of 1,004 matches — 44% — were
  # the honorific before this existed.
  excludes: [องค์สมเด็จ, บาทสมเด็จ]

- key: yantra_wattu
  term: วัตถุมงคล (ยันต์)
  roman: wattu mongkhon
  en_gloss: blessed/inscribed object
  confidence: high
  resident: none
  upkeep: none
  provenance_sensitivity: low
  definition: >
    Takrut, yantra cloth, blessed medallions — power in the inscription and the
    rite. Impersonal.
  members: [ตะกรุด, ผ้ายันต์, ยันต์, วัตถุมงคล, ล็อกเกต]
  note: >
    ONE EXCEPTION worth flagging: a ตะกรุดหนังหน้าผากผีตายโหง (takrut of skin from
    a violent-death corpse) is a spirit-bearing object wearing this class's form.
    Form does not settle class; the making does. See [[prai]].

- key: khong_thammachat
  term: เครื่องรางธรรมชาติ
  roman: khrueang rang thammachat
  en_gloss: natural talisman
  confidence: medium
  needs_verification: true
  resident: none
  upkeep: none
  provenance_sensitivity: low
  definition: >
    Power inherent in a rare natural object rather than conferred by rite:
    เหล็กไหล (leklai, a living metal), กะลาตาเดียว (a one-eyed coconut), certain
    woods, stones and animal parts. Impersonal but NOT consecration-based — a
    third thing, neither Buddha-amulet nor spirit-vessel.
  # คด (the natural concretion) was carried as a bare member and was ~98% noise:
  # it sits inside โชคดี "good luck", โบราณคดี "archaeology", คดี "lawsuit",
  # พระโคดม "Gautama" and คนใจคด "crooked-hearted" — 474 of 484 matches. No set of
  # excludes rescues a two-character term that common, so it is carried only in
  # the one compound the corpus actually contains, the same call made for นาค on
  # the material axis. Add compounds here as they are attested.
  members: [เหล็กไหล, กะลาตาเดียว, คดกะลา, เขี้ยว, งาช้าง]
```

## Spirit-bearing — someone is home, and it eats

A discrete entity has been invited in and bound. It acts; it must be maintained;
it has a relationship with one keeper. **Provenance matters** here in kind, not
just in value — you are adopting a stranger's relationship on its existing terms.

```yaml
- key: thep_thewada
  term: เทพ / เทวดา
  roman: thep / thewada
  en_gloss: deva-tier resident
  confidence: high
  resident: deva
  upkeep: veneration
  provenance_sensitivity: medium
  definition: >
    A celestial or Hindu-derived being is venerated through the object — Thao
    Wessuwan, Garuda (พญาครุฑ), Rahu, arguably Nang Kwak. Receives offerings and
    respect but is not a raised ghost; the relationship is closer to worship than
    to parenting. The "cleanest" spirit-bearing tier.
  members: [ท้าวเวสสุวรรณ, พญาครุฑ, ราหู, นางกวัก, เทพ]
  # เทพ is a deva, but it is also the middle of กรุงเทพ — Bangkok — and of
  # อาจารย์เทพย์ สาริกบุตร, the occult author the manuscript corpus cites heavily.
  # A city and a bibliography are not devas.
  excludes: [กรุงเทพ, เทพย์ สาร, เทพย สาร]
  distinct_from: [kuman, prai]

- key: kuman
  term: กุมารทอง
  roman: kuman thong
  en_gloss: raised child-spirit
  confidence: high
  resident: raised_spirit
  upkeep: feeding
  provenance_sensitivity: high
  definition: >
    A child-spirit bound to an effigy and RAISED — fed sweet red drink, rice and
    toys, named, spoken to, asked for help as a member of the household. A
    reciprocal, parental bond. Neglect is the failure mode: a hungry, ignored
    kuman turns mischievous or leaves. Not "dark" in itself, but a bound spirit
    of the dead, and its history — who raised it, what it was taught — travels
    with it.
  members: [กุมารทอง, กุมาร]
  distinct_from: [thep_thewada, prai]

- key: prai
  term: พราย
  roman: prai
  en_gloss: necromantic ghost-object
  confidence: high
  resident: ghost
  upkeep: feeding_and_closing
  provenance_sensitivity: high
  definition: >
    Houses or is rendered from the ghost of a violent or untimely death,
    classically a woman dead in childbirth (แม่นางพราย) — น้ำมันพราย (prai oil),
    นางพราย, some ลูกกรอก. The most powerful and most hazardous tier: hungry,
    coercive, and requiring both feeding AND correct closing when set down. THE
    class the tradition cautions hardest against acquiring without full history,
    and the one to keep out of the hands of a buyer who does not know how to keep
    it.
  members: [น้ำมันพราย, นางพราย, พราย, ลูกกรอก]
  distinct_from: [kuman, thep_thewada]
  note: >
    ลูกกรอก (a preserved-foetus spirit) sits on the kuman/prai line — raised like
    a kuman but made from untimely death like a prai. Listed here as the more
    cautious placement; a knower may split it.

- key: hun_phayon
  term: หุ่นพยนต์
  roman: hun phayon
  en_gloss: animated effigy / servant-golem
  confidence: high
  resident: animated
  upkeep: veneration
  provenance_sensitivity: medium
  definition: >
    An effigy — figure, cloth, or metal — ANIMATED by yantra and spell to act as
    a servant or guardian. The occupant is a compelled animation rather than a
    named ghost or venerated deva, which is what makes it its own class. Ms 6983
    gives the recipe outright: ตำราสร้างหุ่นพยนต์ แบบที่ ๑ / ๒, beside the ritual
    knife (มีดหมอ) used to make it. The courtroom Hanuman — held in the mouth,
    given commands — is one of these.
  members: [หุ่นพยนต์, พยนต์]
  distinct_from: [thep_thewada, kuman]
```

---

## The fuzzy edges, kept fuzzy on purpose

Three real ambiguities, recorded rather than resolved by fiat:

- **ปลัดขิก** (palad khik) — an impersonal phallic charm to some, a guardian-
  spirit vessel to others. NOT assigned a class here; it needs a knower.
- **ลูกกรอก** — kuman-adjacent in raising, prai-adjacent in origin. Placed in
  `prai` for caution; splittable.
- **ตะกรุดหนังหน้าผาก** — `yantra_wattu` by form, `prai` by making. Class follows
  the making.
- **ขุนแผน / พลายกุมาร** (khun phaen) — the sharpest seam, and a measured one: of
  389 listings naming กุมาร, **106 are ขุนแผน** — a pressed amulet in Buddha-amulet
  FORM (`phra_khrueang`) made with prai-kuman MATERIAL (`kuman`/`prai`). It is a
  true hybrid, not a free-standing kuman you raise and feed. The scanner tags it
  `kuman` because the term กุมาร is verbatim present, and that tag is honest about
  the WORD — but a consumer must not read those 106 as dolls-in-need-of-feeding.
  Its provenance-sensitivity is genuinely medium-to-high (it carries prai
  material) even though its upkeep is that of an amulet. A class that split
  `form` from `material` would resolve this cleanly; a real future move, not a
  decree to make now. Since 2026-08-08 the MARKET facet carries ขุนแผน as its
  own term (237 listings, back-filled by retag_market_term.py), labeled with
  this form-vs-material caveat rather than folded into `kuman` — the seam is
  now visible on /market, still unresolved here on purpose.

Forcing these into clean buckets would record a confidence that does not exist.
The desire-path stays visible until a curator who knows draws the line — the
folksonomy-to-ontology move, not a decree.

## Why the low-confidence entries stay

Deleting `khong_thammachat` because its members are hard to pin, or collapsing
the spirit tiers into one "spirit object" bucket because English has one word,
would make the axis look settled and would erase the exact distinction it exists
to hold. A term marked `needs_verification` is a standing invitation. See
[[user_wichaa_purpose]].
