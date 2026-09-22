---
kind: vocabulary
axis: material
updated: 2026-07-27
---

# Material — เนื้อ, the first thing a sian names

The emic term is the identity. English is a gloss offered for convenience and
carries no authority.

A sian does not open with what an amulet is *for*. They open with **เนื้อ** — what
it is made of — because material is the first gate on age, on workshop, and on
whether the piece can be what the seller says it is. A พระรอด that is not fired
clay is not a พระรอด, whatever else is true about it. Function and class describe
what an object *does* and what *lives in it*; this axis describes what it *is*,
and it is the axis on which the expert trade actually turns.

Two fields carry the working weight, and they are why this axis is queryable
rather than merely descriptive:

- **dating_signal** — `none` · `patina` · `surface_crust` · `wear` · `shrinkage`.
  What the material lets a reader say about age. เนื้อชิน grows สนิมแดง (red rust);
  เนื้อผง takes คราบ, a surface crust; metals take patina. This field is the one a
  sale listing never states and a loupe exists to read.
- **counterfeit_pressure** — `low` · `medium` · `high`. How heavily the material
  is reproduced. This is a caution about the *category*, never a claim about any
  particular object. A high value means "expect careful comparison to be normal
  here," not "this is fake."

`family` groups the terms for display: `phong` (paste) · `din` (fired earth) ·
`chin` (tin-lead) · `loha` (metal) · `organic` · `relic`.

`members` lists the surface forms a scanner searches for in both corpora. **A tag
claims only that the emic term occurs VERBATIM** — not that the object is that
material, and certainly not that it is genuine.

`excludes` lists strings that contain a member as a substring but are not it.
Thai runs together without spaces, so short terms collide: `ว่าน` is contained in
`กว่าน` ("harder *than*…"), which accounted for **120 of 297** page matches
before the exclusion existed. The scanner removes excluded strings from the text
before testing, so a page holding both a real ว่าน and a stray กว่าน still tags
correctly. Where a term cannot be disambiguated this way it is carried only in
its unambiguous compound forms, and the vocab says so.

`seen` records occurrences in the 13,020-listing commerce corpus as measured on
2026-07-27. It is evidence that the term is *live in the vernacular*, nothing
more. Terms are kept even at low counts when they name something the tradition
distinguishes.

**This axis runs across the seam, and that was not the first answer.** Searching
manuscript *titles* returned zero hits for every term, and the draft of this note
concluded that material was a market-side axis only — that the treatises assume
the material and name the purpose. Searching the transcribed *pages* overturned
it. The treatises name materials constantly, and operationally:

> แผ่นทองแดง แผ่นตะกั่ว หรือแผ่นทอง แผ่นเงิน แผ่นนาค
> *(sheet of copper, sheet of lead, or sheet of gold, sheet of silver, sheet of naak)*

That is a treatise specifying which metal to inscribe a yantra on — the same
choice a sian reads off a finished object four centuries later. Material is the
axis where the two corpora speak the *same* vocabulary about the *same* decision,
which makes it the natural spine for a register that has to join them.

The clearest instance is ผงใบลาน, where the corpus holds the recipe itself:

> ท่านให้ลงใบลาน ๕ ใบ ใบละพระคาถา เผาเป็นสมุกผสมกับขี้รักปั้นเป็นลูกประคำ
> *(inscribe five palm leaves, one formula to each; burn them to ash, mix with
> lacquer, roll into rosary beads)*

The ใบลาน this archive catalogues as text, and the ผงใบลาน the market sells as
material, are the same object at two moments of its life. The seam is not a
join we imposed; it is written down.

Every entry declares its own `confidence`. `needs_verification: true` means it
was written from model training knowledge and has not yet been checked against a
Thai-language printed reference. Occurrence in the corpus verifies that the term
is *used*; it does not verify that the definition here is right.

---

## ผง — paste and powder

Ground sacred matter bound into a paste and pressed in a mould. The สมเด็จ family
and most modern temple issues. Reads its age through คราบ, the surface crust, and
through shrinkage away from the mould edge.

```yaml
- key: nuea_phong
  term: เนื้อผง
  roman: nuea phong
  en_gloss: sacred-powder paste
  confidence: high
  needs_verification: false
  family: phong
  dating_signal: surface_crust
  counterfeit_pressure: high
  seen: 228
  definition: >
    Consecrated powder bound with a binder (traditionally banana sap, lime, oil)
    and pressed. The material of the พระสมเด็จ and of most temple issues since.
    Because the recipe is reproducible and the mould is copyable, this is the
    most heavily reproduced material in the trade — which is precisely why the
    reference literature on it is the deepest.
  members: [เนื้อผง, พระผง, ผงพุทธคุณ, เนื้อผงเกสร]

- key: phong_phuttakhun
  term: ผงพุทธคุณ
  roman: phong phuttakhun
  en_gloss: powder of the Buddha's qualities
  confidence: medium
  needs_verification: true
  family: phong
  dating_signal: surface_crust
  counterfeit_pressure: high
  seen: 105
  definition: >
    Powder produced by writing and erasing sacred formulae on a slate, the chalk
    dust collected and re-written many times. The named powders — ปถมัง, อิทธิเจ,
    ตรีนิสิงเห, มหาราช, พุทธคุณ — are distinguished by which formula was written.
    A listing that says only "ผงพุทธคุณ" is naming a family, not a recipe.
  members: [ผงพุทธคุณ, ผงปถมัง, ผงอิทธิเจ, ผงตรีนิสิงเห, ผงมหาราช]

- key: phong_bai_lan
  term: ผงใบลาน
  roman: phong bai lan
  en_gloss: burnt palm-leaf manuscript ash
  confidence: medium
  needs_verification: true
  family: phong
  dating_signal: surface_crust
  counterfeit_pressure: medium
  seen: 25
  definition: >
    Paste incorporating the ash of burnt palm-leaf manuscripts — scripture that
    has been consumed and re-embodied as an object of veneration. This is the
    seam between the two corpora made literal: the same ใบลาน this archive
    catalogues as text appears in the market as material. Where a listing names
    a specific manuscript or temple source, that is a provenance claim worth
    recording separately.
  members: [ใบลาน, ผงใบลาน, เนื้อผงใบลาน]
```

## ดิน — fired earth

Clay, fired. The oldest surviving votive material in the region and the body of
several of the canonical types. Reads its age through shrinkage, through the
fire colour, and through wear that follows the clay's own grain.

```yaml
- key: nuea_din
  term: เนื้อดิน
  roman: nuea din
  en_gloss: clay body
  confidence: high
  needs_verification: false
  family: din
  dating_signal: shrinkage
  counterfeit_pressure: high
  seen: 68
  definition: >
    Clay pressed in a mould and fired. The body of พระรอด, พระนางพญา and
    พระผงสุพรรณ — the last of which is named ผง but is fired earth, a naming trap
    worth knowing. Fire colour ranges widely within a single kiln load, so colour
    alone settles nothing.
  members: [เนื้อดิน, ดินเผา, เนื้อดินเผา]
```

## ชิน — tin-lead alloy

The material of the votive tablets recovered from stupa deposits. Its patina is
the most-read surface in the whole trade, because tin-lead corrodes in ways that
are slow and characteristic.

```yaml
- key: nuea_chin
  term: เนื้อชิน
  roman: nuea chin
  en_gloss: tin-lead alloy
  confidence: high
  needs_verification: true
  family: chin
  dating_signal: patina
  counterfeit_pressure: high
  seen: 39
  definition: >
    A tin-lead alloy cast or pressed into votive tablets, characteristic of
    pieces recovered from กรุ (stupa deposits). Conventionally divided by patina
    into ชินเงิน (silvery), ชินตะกั่ว (lead-heavy) and ชินสนิมแดง (red-rust).
  members: [เนื้อชิน, ชินเงิน, ชินตะกั่ว]

- key: sanim_daeng
  term: สนิมแดง
  roman: sanim daeng
  en_gloss: red rust patina
  confidence: medium
  needs_verification: true
  family: chin
  dating_signal: patina
  counterfeit_pressure: high
  seen: 13
  definition: >
    The red lead-oxide crust that forms on ชิน over long burial. Named as a
    material in the market but functioning as an age claim — which is why it is
    both prized and reproduced. Recorded here as a surface state, not as a
    verdict on age.
  members: [สนิมแดง, ชินสนิมแดง]

- key: takua
  term: ตะกั่ว
  roman: takua
  en_gloss: lead
  confidence: high
  needs_verification: false
  family: chin
  dating_signal: patina
  counterfeit_pressure: medium
  seen: 106
  definition: >
    Lead, used both as an alloy component in ชิน and on its own — most visibly as
    the sheet rolled into ตะกรุด. Soft enough to take an inscription with a
    stylus, which is the whole reason it is used for rolled amulets.
  members: [ตะกั่ว, เนื้อตะกั่ว]
```

## โลหะ — metal

Cast metal, from plain brass to the nine-metal alloy. The family where the
recipe itself is the claim: นวโลหะ is prized because of what went into the
crucible, and that is unreadable from the finished surface.

```yaml
- key: nawaloha
  term: นวโลหะ
  roman: nawaloha
  en_gloss: nine-metal alloy
  confidence: medium
  needs_verification: true
  family: loha
  dating_signal: patina
  counterfeit_pressure: high
  seen: 26
  definition: >
    An alloy of nine metals cast to a prescribed recipe, each metal contributed
    for its own quality. Highly regarded, and the claim cannot be read off the
    finished object — which makes the record of the casting (which foundry, which
    ceremony, which year) the actual asset. A register entry is worth more here
    than a photograph.
  members: [นวโลหะ, เนื้อนวโลหะ]

- key: nuea_loha
  term: เนื้อโลหะ
  roman: nuea loha
  en_gloss: metal (unspecified)
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: patina
  counterfeit_pressure: medium
  seen: 92
  definition: >
    Metal, unspecified. Common in listings precisely because it commits to
    nothing. Recorded as its own term rather than resolved, because the vagueness
    is itself the datum — a seller who can name the alloy usually does.
  members: [เนื้อโลหะ, เนื้อทองผสม, โลหะผสม]

- key: samrit
  term: สัมฤทธิ์
  roman: samrit
  en_gloss: bronze
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: patina
  counterfeit_pressure: medium
  seen: 25
  definition: >
    Bronze. The body of most พระบูชา (altar images) as distinct from the small
    worn amulet. Spelled both สัมฤทธิ์ and สำริด in the market.
  members: [สัมฤทธิ์, สำริด, เนื้อสัมฤทธิ์]

- key: thonglueang
  term: ทองเหลือง
  roman: thonglueang
  en_gloss: brass
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: patina
  counterfeit_pressure: low
  seen: 414
  definition: >
    Brass. The most-named metal in the corpus by a wide margin — the everyday
    material of altar goods, pendant frames and mass issues. High occurrence here
    reflects volume at the low end of the market, not regard.
  members: [ทองเหลือง, เนื้อทองเหลือง]

- key: thongdaeng
  term: ทองแดง
  roman: thongdaeng
  en_gloss: copper
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: patina
  counterfeit_pressure: low
  seen: 133
  definition: >
    Copper. Common as the base metal of struck เหรียญ (medal-form amulets), where
    the issue is often distinguished by which metals the same die was struck in.
  members: [ทองแดง, เนื้อทองแดง]

- key: ngoen
  term: เนื้อเงิน
  roman: nuea ngoen
  en_gloss: silver
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: patina
  counterfeit_pressure: medium
  seen: 32
  definition: >
    Silver. Usually the middle tier of a struck issue — a รุ่น commonly runs
    ทองแดง, เงิน, ทองคำ from the same die, in descending quantity and ascending
    regard.
  members: [เนื้อเงิน, เงินแท้]

- key: thongkham
  term: เนื้อทองคำ
  roman: nuea thongkham
  en_gloss: gold
  confidence: high
  needs_verification: false
  family: loha
  dating_signal: none
  counterfeit_pressure: high
  seen: 93
  definition: >
    Gold. Thin in this corpus — 93 of 13,020 listings, and most of those name it
    for a frame or a plating rather than for the body of the piece. Gold issues
    are not rare in the tradition; they do not circulate on an open retail
    platform. That thinness measures what this corpus can and cannot see, and is
    among the clearest arguments for seeding the register from competition and
    association records rather than from listings.
    **Correction of record:** an earlier draft put this at 1 occurrence, having
    searched only the compound เนื้อทองคำ. The bare term is the one the market
    uses.
  members: [ทองคำ, เนื้อทองคำ, ทองคำแท้]

- key: naak
  term: เนื้อนาค
  roman: nuea naak
  en_gloss: copper-gold alloy (rose gold)
  confidence: medium
  needs_verification: true
  family: loha
  dating_signal: patina
  counterfeit_pressure: medium
  seen: 0
  definition: >
    A copper-and-gold alloy of reddish cast, ranked in the treatises alongside
    gold and silver as one of the sheets a yantra may be inscribed on — the
    corpus phrase is แผ่นทอง แผ่นเงิน แผ่นนาค. Added to this axis *because of* that
    passage, not from the market: the compound forms return zero listings, so
    this is a material the treatises name and the retail corpus does not carry.
    **Carried only in unambiguous compounds.** Bare นาค returns 553 pages and 132
    listings, but nearly all of those are the naga serpent — a being, not an
    alloy — which belongs to the class and motif axes. Scanning the bare term
    here would import a bestiary into a materials list.
  members: [เนื้อนาค, แผ่นนาค, ทองนาค]

- key: mekphat
  term: เมฆพัด
  roman: mekphat
  en_gloss: alchemical dark alloy
  confidence: low
  needs_verification: true
  family: loha
  dating_signal: patina
  counterfeit_pressure: high
  seen: 1
  definition: >
    A dark, near-black alloy produced by a repeated smelting-and-quenching
    process treated as an alchemical operation rather than a metallurgical one.
    One occurrence in the corpus. Kept at low confidence and low count because
    the tradition names it clearly even where the market does not carry it —
    the same reason ถ้อยความ is kept on the function axis.
  members: [เมฆพัด, เนื้อเมฆพัด, เมฆสิทธิ์]
```

## ว่าน และ อินทรีย์ — herb and organic

Plant and animal matter. The family where provenance is not only a question of
value but of what the object is — and where the class axis should always be
consulted alongside this one.

```yaml
- key: nuea_waan
  term: เนื้อว่าน
  roman: nuea waan
  en_gloss: sacred-herb paste
  confidence: high
  needs_verification: true
  family: organic
  dating_signal: shrinkage
  counterfeit_pressure: medium
  seen: 64
  definition: >
    Paste of ว่าน — the sacred tubers and herbs gathered under prescribed
    conditions. Northern practice is particularly rich here. Ages by drying and
    shrinking rather than by patina. The manuscripts carry ว่าน heavily —
    คาถาเสกว่าน, formulae for consecrating the herb — so this term joins the two
    corpora directly, once the กว่าน collision is excluded.
  members: [เนื้อว่าน, ว่าน, ว่านสบู่เลือด, ว่านดอกทอง, เสกว่าน]
  excludes: [กว่าน]

- key: kala
  term: กะลา
  roman: kala
  en_gloss: coconut shell
  confidence: high
  needs_verification: true
  family: organic
  dating_signal: wear
  counterfeit_pressure: low
  seen: 281
  definition: >
    Coconut shell, most often the single-eyed shell (กะลาตาเดียว) carved and
    inscribed. High occurrence in the corpus. Note that many กะลา hits are the
    carved ปลัดขิก form — cross-check the class axis, which deliberately leaves
    ปลัดขิก unassigned.
  members: [กะลา, กะลาตาเดียว]

- key: nga
  term: งาช้าง
  roman: nga chang
  en_gloss: elephant ivory
  confidence: high
  needs_verification: true
  family: organic
  dating_signal: wear
  counterfeit_pressure: medium
  seen: 9
  definition: >
    Elephant ivory. Recorded because the tradition uses it and the corpus
    contains it. **Legal caution, not a value judgement:** ivory is regulated in
    Thailand under the Elephant Ivory Act B.E. 2558 and internationally under
    CITES. Any register entry naming this material should carry that notice, and
    the register should never facilitate its movement across a border.
  members: [งาช้าง, เนื้องา, งาแกะ]

- key: khao
  term: เขาสัตว์
  roman: khao sat
  en_gloss: horn
  confidence: medium
  needs_verification: true
  family: organic
  dating_signal: wear
  counterfeit_pressure: low
  seen: 8
  definition: >
    Horn, most often buffalo — เขาควาย, and in the strongest form เขาควายเผือก
    (albino buffalo horn), gathered under conditions that are themselves part of
    the claim.
  members: [เขาควาย, เขาสัตว์, เขาควายเผือก]
```

## บริขาร — relic and contact material

Matter that touched a specific person. Here the material is a provenance claim
in its own right: the value is not the substance but whose it was.

```yaml
- key: kesa
  term: เกศา
  roman: kesa
  en_gloss: hair of the master
  confidence: medium
  needs_verification: true
  family: relic
  dating_signal: none
  counterfeit_pressure: high
  seen: 20
  definition: >
    Hair of a named monk, incorporated into a paste or sealed into the piece.
    The material is unremarkable; the attribution is everything. Unverifiable
    from the object, which makes the temple's own issue record the only thing
    that could ever support it — exactly the record a register should hold.
  members: [เกศา, เส้นเกศา, ผงเกศา]

- key: chiwon
  term: จีวร
  roman: chiwon
  en_gloss: robe cloth
  confidence: medium
  needs_verification: true
  family: relic
  dating_signal: none
  counterfeit_pressure: high
  seen: 46
  definition: >
    A fragment of a monk's robe, set into or behind the piece. As with เกศา, the
    claim rests entirely on the issue record.
  members: [จีวร, ผ้าจีวร, เศษจีวร]

- key: pha_yan
  term: ผ้ายันต์
  roman: pha yan
  en_gloss: inscribed cloth
  confidence: high
  needs_verification: false
  family: relic
  dating_signal: wear
  counterfeit_pressure: medium
  seen: 330
  definition: >
    Cloth bearing a drawn or stamped yantra. Strictly a form rather than a
    material, kept on this axis because the market names it in the material slot
    and a reader looking for "what is it made of" will look here. Cross-reference
    the motif axis for the yantra itself.
  members: [ผ้ายันต์, ผ้ายันต์รอยเท้า]
```

---

## Not carried

- **ไม้ตะเคียน** (takhian wood) — proposed and measured at **0 occurrences** in
  13,020 listings, despite the tree being among the most storied in Thai spirit
  belief. Recorded here rather than dropped: an absence measured is a finding.
  Where it appears it is likely as นางตะเคียน, a resident rather than a material —
  which is the class axis's business, not this one.

## Open

- **พิมพ์ (mould-type) is not on this axis and should not be forced onto it.**
  พิมพ์ is only meaningful relative to a specific รุ่น of a specific วัด, so it
  belongs to the register's record schema (วัด × รุ่น × พิมพ์ × เนื้อ), with this
  axis hanging off it as one field. Building พิมพ์ as a flat vocabulary would
  produce thousands of context-free "พิมพ์ใหญ่" tags that mean different objects
  at different temples.
- Sub-recipes of ผง (ปถมัง, อิทธิเจ, ตรีนิสิงเห, มหาราช) are listed as members
  rather than promoted to their own keys, pending a Thai printed reference.
- `counterfeit_pressure` is written from training knowledge throughout and every
  value should be checked against the reference literature before the field is
  shown to a reader who might act on it.
