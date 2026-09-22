---
kind: vocabulary
axis: function
updated: 2026-07-22
---

# Function — what an amulet is *for*

The emic term is the identity. English is a gloss offered for convenience and
carries no authority.

This axis exists because **function is the one thing the sources never put in a
title**. Ms 6983 names its formulas by what is *made* — ตำราสร้างพระฉิมพลี
(making a Phra Sivali), ตำราปั้นรูปพระฤๅษี (moulding a lersi), ตำราหุงสีผึ้ง
(cooking love-wax) — and states its own shape as ๔๒ ชนิด / ๑๕๘ แบบ, forty-two
kinds in a hundred and fifty-eight forms. What each one *does* is buried in the
prose, usually in a single clause after the consecration. A reader can find it.
A catalogue cannot, until someone builds this.

The same vocabulary runs from the treatise to the marketplace: โชคลาภ appears in
566 Lazada listings, เมตตามหานิยม in 337, คงกระพัน in 73. That continuity is the
argument for a **single axis across both corpora** rather than one taxonomy for
manuscripts and another for commerce — see [[project_seamless_corpus]].

Every entry declares its own `confidence`. Terms marked `needs_verification`
were written from model training knowledge and have **not** been checked against
a Thai-language source; they are a starting point for someone who knows.

---

## The distinction English destroys

Thai names **three different theories of not being harmed**, and "protection"
flattens all three into one word. They are not intensities of each other — they
disagree about where the safety comes from:

- **คงกระพัน** — the blade arrives and does not cut. The body is changed.
- **มหาอุด** — the shot never leaves the barrel, or stops. The weapon is changed.
- **แคล้วคลาด** — you were not standing there. The circumstance is changed.

An amulet sold as all three is making three separate claims. A schema with one
"protection" bucket cannot record which one a given formula actually promises,
and every Thai speaker in the market knows the difference.

```yaml
- key: khong_kraphan
  term: คงกระพัน
  roman: khong kraphan
  en_gloss: invulnerability to blades
  confidence: high
  definition: >
    The body cannot be cut or pierced. Classically paired with ชาตรี in the
    martial compound คงกระพันชาตรี. Says nothing about firearms — that is มหาอุด.
  distinct_from: [maha_ut, khlaeo_khlat]

- key: maha_ut
  term: มหาอุด
  roman: maha ut
  en_gloss: stopping projectiles / misfire
  confidence: high
  definition: >
    Literally "greatly stopped-up". The gun jams, misfires, or the shot does not
    penetrate. The efficacy is located in the weapon, not the body.
  distinct_from: [khong_kraphan]

- key: khlaeo_khlat
  term: แคล้วคลาด
  roman: khlaeo khlat
  en_gloss: evasion, narrow escape
  confidence: high
  definition: >
    Harm passes by — the accident happens to the next vehicle, the bullet goes
    wide, you left the building early. Distinct in kind from คงกระพัน: nothing
    strikes you at all, so nothing needs to be resisted.
  distinct_from: [khong_kraphan, maha_ut]
```

## Favour, and the other thing English calls "charm"

```yaml
- key: metta_maha_niyom
  term: เมตตามหานิยม
  roman: metta maha niyom
  en_gloss: loving-kindness and wide popularity
  confidence: high
  definition: >
    Broad social favour — people are well-disposed, superiors are lenient,
    customers return. Built on เมตตา, the Buddhist virtue, and respectable to
    carry and to sell.
  distinct_from: [maha_saneh]
  note: >
    The single most common function claim in the modern market (337 listings).

- key: maha_saneh
  term: มหาเสน่ห์
  roman: maha saneh
  en_gloss: powerful attraction, allure
  confidence: high
  definition: >
    Personal and frequently erotic attraction, directed at a particular person
    rather than at a room. Overlaps the love-wax (สีผึ้ง) and น้ำมันพราย
    material tradition.
  distinct_from: [metta_maha_niyom]
  note: >
    Carries a faint edge of coercion that เมตตามหานิยม does not. Rendering both
    as "charm" erases exactly the line practitioners draw between them.

- key: maha_laluai
  term: มหาละลวย
  roman: maha laluai
  en_gloss: infatuation, bewitchment
  confidence: medium
  needs_verification: true
  definition: Stronger and more compelling than มหาเสน่ห์; the target is besotted.
```

## Fortune and trade

```yaml
- key: chok_lap
  term: โชคลาภ
  roman: chok lap
  en_gloss: luck and windfall
  confidence: high
  definition: >
    Fortune arriving from outside — lottery, gifts, unexpected gain. โชค is the
    luck, ลาภ the thing that turns up because of it.
  note: 566 listings — the most frequent function term in the commerce corpus.

- key: kha_khai
  term: ค้าขาย
  roman: kha khai
  en_gloss: trade, selling
  confidence: high
  definition: >
    Specifically commercial: custom comes to the shop, goods move. Distinguished
    from โชคลาภ because the gain is worked for rather than fallen into.
  distinct_from: [chok_lap]
```

## Contest, concealment, compulsion

```yaml
- key: thoi_khwam
  term: ถ้อยความ
  roman: thoi khwam
  en_gloss: legal dispute — made to retreat
  confidence: medium
  needs_verification: true
  definition: >
    The suit itself: literally the words of a dispute, the testimony. As a
    function it is always phrased as the dispute RETREATING —
    สรรพถ้อยความทั้งปวงก็ถอยไป, "all disputes whatsoever withdraw" — not as the
    bearer winning one. Ms 6983 places it, without comment, between going into
    battle and prize-fighting: a contest entered by someone who expects to be
    outmatched. The mechanism is not persuasion but silencing — the katha shuts
    the mouth, ears and eyes of the other side (ปิดปาก ปิดหู ปิดตา), after which
    "they cannot speak against you, and both plaintiff and judge greatly fear
    your power."
  note: >
    **This entry was corrected by the corpus.** It was first written as ชนะคดี
    "winning a lawsuit" — standard modern legal Thai, imported from model
    training knowledge. ชนะคดี and ชนะความ occur ZERO times in 170 transcribed
    pages and zero times in 14,653 listings; ถ้อยความ is what the source says.
    The imported term also carried the wrong idea: ชนะ is to win, ถอย is to
    retreat, and the formula promises the second. Kept here as a worked example
    of the failure mode this vocabulary exists to prevent — see
    [[user_wichaa_purpose]].
  market_absence: >
    0 of 14,653 commerce listings. Either the function has genuinely left the
    market, or sellers avoid naming it. A field check would settle it; until
    then the absence is recorded, not explained.

- key: kambang
  term: กำบัง
  roman: kambang
  en_gloss: concealment, going unseen
  confidence: medium
  needs_verification: true
  definition: >
    Not being perceived — passed over rather than literally transparent. In ms
    6983 the same Hanuman, steeped in scented oil, makes a household unable to
    see, hear or speak to the bearer.
  distinct_from: [long_hon]

- key: long_hon
  term: ล่องหน
  roman: long hon
  en_gloss: invisibility
  confidence: low
  needs_verification: true
  definition: Vanishing outright, as opposed to merely being overlooked.
  distinct_from: [kambang]

- key: sakot
  term: สะกด
  roman: sakot
  en_gloss: subduing, binding, putting to sleep
  confidence: medium
  needs_verification: true
  definition: >
    Compelling another to stillness or sleep — the household that cannot wake,
    the pursuer who cannot follow. Applied to people and to animals.

- key: chang_ngang
  term: จังงัง
  roman: chang-ngang
  en_gloss: stupefaction, being frozen
  confidence: low
  needs_verification: true
  definition: The target is rooted, dumbstruck, unable to act.
  distinct_from: [sakot]
```

## Warding and general protection

```yaml
- key: kan_phi
  term: กันผี
  roman: kan phi
  en_gloss: warding spirits
  confidence: high
  definition: >
    Against ผี specifically — the dead, the hungry, the malicious — not against
    human violence. A different threat model from คงกระพัน entirely.
  distinct_from: [khong_kraphan, khum_khrong]

- key: khum_khrong
  term: คุ้มครอง
  roman: khum khrong
  en_gloss: general protection, watching over
  confidence: high
  definition: >
    Unspecified guardianship. **A holding pen, not a category** — when a source
    says only คุ้มครอง it usually has not said which of the specific functions
    above it means. Treat its presence as a gap to close, not an answer.
```

---

## Why the low-confidence entries stay

Deleting them would make the axis look more settled than it is and would hide
the gaps a contributor could close. A term marked `needs_verification` is a
standing invitation. A term silently omitted is invisible — the failure mode
this archive exists to prevent. Same principle as
[[project_taxonomy_nodes]]: adding a term is normal, merging two because
English lacks the distinction is not.
