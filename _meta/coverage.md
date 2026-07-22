---
kind: coverage
updated: 2026-07-22
---

# Coverage

What has been looked for, where, by what method — so that an absence can be read.

An absent record means one of three different things, and they need three
different responses:

- **out of scope** — nobody looked there yet. Fix: widen a scope below.
- **not in the source** — looked, and the source does not have it. Fix: field authoring.
- **unwritten** — in scope, in the source, nobody has made the note. Fix: a quest.

Without this file all three look identical, which is how วัดศรีดอนมูล sat
"missing" while nothing was actually broken.

```yaml
scopes:
  - {id: wat.th.lanna, what: "Buddhist temples (wat)", method: "OSM Overpass, admin_level=4 by ISO3166-2", status: active, records: 1466, last_crawled: 2026-07-22, regions: "TH-50 TH-51 TH-52 TH-55 TH-56 TH-57 TH-58", region_names: "Chiang Mai, Lamphun, Lampang, Nan, Phayao, Chiang Rai, Mae Hong Son"}
  - {id: wat.th.lanna.cm-bbox-caveat, what: "Chiang Mai is a bbox around city + inner suburbs, NOT the whole changwat", method: none, status: known-limit, note: "Temples in outer CM districts are OUT OF SCOPE, not missing"}
  - {id: wat.th.lanna.compound-structures, what: "Structures inside one compound tagged as separate places of worship in OSM", method: none, status: in-review, records: 7, note: "A bare Chedi or Viharn; flagged in the near-duplicate queue, never auto-merged"}
  - {id: wat.th.absent-from-osm, what: "Temples that exist but are absent from OpenStreetMap at any tagging", method: "field authoring only", status: open, note: "Wat Si Don Mun Saraphi (Khruba Noi): zero matches for the name among place_of_worship in all Chiang Mai province, checked 2026-07-22"}
  - {id: sacred.th.lanna.non-wat, what: "City pillars, sunken cities, sacred and prehistoric caves, mosques, churches, monumental Buddha images", method: "Wikidata by class, 250km radius filtered to the Lanna bbox", status: active, records: 28, last_crawled: 2026-07-21}
  - {id: spirit-house.th, what: "San phra phum, san chao thi and kin - the household sacred landscape", method: "field only", status: not-started, records: 0, note: "OSM Thailand 2026-07-22: 23825 wats but 20 named san phra phum and 2 san chao thi. No crawl closes this."}
  - {id: spirit-house.seasia, what: "Ho phi (Laos), nat sin (Myanmar), neak ta (Cambodia) and neighbours", method: "field only", status: planned, records: 0, note: "NOT translations of each other; each needs its own vocabulary entry and sources"}
```

## How to read a gap

A quest generator should only ever draw from `status: active` scopes. Asking a
contributor to photograph something in an out-of-scope region is asking them to
do the crawler's job by hand; asking for something in `absent-from-osm` is
exactly right, because a person is the only instrument that reaches it.
