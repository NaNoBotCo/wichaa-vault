---
kind: vocabulary
axis: place-type
updated: 2026-07-22
---

# Place types

The emic term is the identity. English is a gloss offered for convenience and
carries no authority. Adding a term is normal; merging two because English lacks
the distinction is not.

Every entry declares its own `confidence`. Terms marked `needs_verification`
were written from model training knowledge and have **not** been checked against
a source — they are a starting point for someone who knows, not an assertion.
Treat them as you would any `crawled` field.

---

## Thai

```yaml
- key: san_phra_phum
  term: ศาลพระภูมิ
  roman: san phra phum
  en_gloss: spirit house (guardian of the land)
  confidence: high
  definition: >
    Shrine to Phra Phum, the guardian deity of the ground a property stands on.
    Characteristically raised on a single pillar. Its siting follows geomantic
    rules — notably that the shrine should not fall under the shadow of the
    building it serves.
  distinct_from: [san_chao_thi]
  note: >
    Deva-tier and Hindu-derived in origin, which is why it is not
    interchangeable with the earth-spirit shrines below even when the two stand
    side by side.

- key: san_chao_thi
  term: ศาลเจ้าที่
  roman: san chao thi
  en_gloss: spirit house (lord of the place)
  confidence: high
  definition: >
    Shrine to the chao thi — the spirit of the place itself. Commonly a
    house-shaped shrine on several posts rather than one, and set lower than a
    san phra phum where both are present.
  distinct_from: [san_phra_phum]
  note: >
    Animist rather than deva-tier. The two frequently occupy the same forecourt
    a metre apart and take different offerings. Any schema that renders both as
    "spirit house" has destroyed the only thing that distinguishes them.

- key: san_ta_yai
  term: ศาลตายาย
  roman: san ta yai
  en_gloss: grandparents' shrine
  confidence: medium
  needs_verification: true
  definition: >
    Shrine to ancestral spirits — literally grandfather/grandmother — often for
    the previous custodians of the ground.

- key: wat
  term: วัด
  roman: wat
  en_gloss: Buddhist temple (monastery)
  confidence: high
  definition: >
    A monastic complex, not a single building: typically ubosot, wihan, chedi,
    sala and monks' quarters within a wall.

- key: lak_mueang
  term: หลักเมือง
  roman: lak mueang
  en_gloss: city pillar
  confidence: high
  definition: >
    The pillar housing the guardian spirit of a mueang — the town's axis. In
    Chiang Mai, Sao Inthakhin.
```

## Neighbouring traditions

Related, **not** translations of one another. Each needs its own sources before
it is used in anger.

```yaml
- key: ho_phi
  term: ຫໍຜີ
  roman: ho phi
  lang: lo
  en_gloss: spirit house
  confidence: low
  needs_verification: true

- key: nat_sin
  term: နတ်စင်
  roman: nat sin
  lang: my
  en_gloss: nat shrine
  confidence: low
  needs_verification: true
  note: For the nats; the 37 in particular. Orthography unverified.

- key: neak_ta
  term: អ្នកតា
  roman: neak ta
  lang: km
  en_gloss: territorial guardian shrine
  confidence: low
  needs_verification: true
```

---

## Why the low-confidence entries stay in the file

Deleting them would make the vault look more certain than it is, and would hide
the very gaps a contributor could close. A term marked `needs_verification` is a
standing invitation. A term silently omitted is invisible — which is the whole
failure mode this archive is built against.

## Non-wat sacred site types

Emitted by the Wikidata sacred-sites harvest. Listed here so the validator stops
reporting them as unknown — and so each can be given a proper definition and its
own sources rather than staying a bare English label.

```yaml
- key: cave
  term: ถ้ำ
  roman: tham
  en_gloss: cave (sacred or prehistoric)
  confidence: medium
  needs_verification: true
  note: >
    Covers both meditation caves in active religious use and prehistoric
    archaeological caves. Those are different things and should probably split
    into two terms once someone who knows has looked.

- key: ancient_city
  term: เวียง
  roman: wiang
  en_gloss: walled settlement / sunken city
  confidence: medium
  needs_verification: true
  note: Wiang Kum Kam, Wiang Tha Kan. A wiang is a walled mueang, not a ruin per se.

- key: mosque
  term: มัสยิด
  roman: matsayit
  en_gloss: mosque
  confidence: high

- key: church
  term: โบสถ์คริสต์
  roman: bot khrit
  en_gloss: church
  confidence: medium
  needs_verification: true

- key: buddha_image
  term: พระพุทธรูป
  roman: phra phuttharup
  en_gloss: monumental Buddha image
  confidence: high

- key: city_pillar
  term: หลักเมือง
  roman: lak mueang
  en_gloss: city pillar
  confidence: high
  same_as: lak_mueang

- key: statue
  term: อนุสาวรีย์
  roman: anusawari
  en_gloss: statue / monument
  confidence: medium
  needs_verification: true

- key: sacred_site
  term: ""
  en_gloss: sacred site (unclassified)
  confidence: low
  note: >
    A holding pen, not a category. Anything landing here needs a real term —
    treat its presence as a gap to be closed, not an answer.
```
