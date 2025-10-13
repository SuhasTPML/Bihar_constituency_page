# Bihar Assembly Elections Hub — Implementation Plan (with 2020 Results)

> Scope: Ship an Assembly-only, data-driven microsite with 243 constituency pages, an interactive constituency map, party/MLA directories, 2020 results, and voter-roll context (electors & shifted). Districts/LS seats are **out of scope** for UX navigation (but may exist in data).

---

## Status Update (Current)

- Constituency viewer (`constituency_viewer.html`) implemented with input box to load any seat (1–243).
- Integrated historical results: `2010_results.json`, `2015_results.json`, `2020_results.json` (district-keyed JSONs).
- Added CLI (`scripts/constituency_info.py`) to emit merged JSON per seat (base, current MLA, 2010/2015/2020 results). Output excludes Lok Sabha, electors, and percentages.
- Switched MLA source to JSON: using `current_mla.json` (district-keyed) instead of the previous CSV.
- Party code normalization in tooling (e.g., JDU→JD(U), CPM→CPI(M), HAM→HAM(S), Ind→IND) using `parties.json` metadata.
- Electors/shifted and turnout/percentages are not displayed at this time (data incomplete/out of scope).

## Plan Adjustments

- Constituency pages will show 2010/2015/2020 results (winner, runner‑up, votes, margin) and a trend text (2010→2015, 2015→2020 Hold/Gain). Vote percentages, turnout, and electors are deferred.
- Data sources revised to prefer JSON inputs for results (2010/2015/2020). CSV for electors removed from current scope.
- Optional future: generate a single `constituencies_full.json`; for now, the CLI and the viewer perform on‑demand/client‑side merges.

## 1) Product Modules & Pages

### 1.1 Hub (Landing)
- **Sections:** Hero, Snapshot cards, Assembly composition (party/alliance), Interactive constituency map, Constituency directory (search/filter), Reserved seats view, Party seat share, MLA directory CTA.
- **Primary CTAs:** Explore Constituencies, Party Seat Share, MLA Directory.
- **Data shown:**
  - Total seats: 243
  - Reserved seats: 38 SC, 2 ST
  - (Deferred) Electors/turnout until data is available
  - Composition (NDA/MGB/Others + party splits)
  - Map + tooltips: `{no, name, reserved, MLA/current/winner, margin}`

### 1.2 Constituency Page (243)
- **Header:** {No}. {Name} [{SC/ST badge if any}]
- **Key Widgets:**
  - 2020 Results summary: winner, runner-up, vote share %, margin, turnout
  - Current representation: MLA + party (as of latest)
  - Electors (2024 roll) + shifted voters (cleanup)
  - Trend mini-chart: 2015 vs 2020 vote share (optional)
- **Meta:** slug `/bihar/constituency/{slug}`
- **Future slots:** 2025 candidates & live results

### 1.3 Party View
- **Overview:** Party seat count, share of assembly, alliance mapping
- **List:** Constituencies held (link to each constituency page)
- **Charts:** Seat share bar, optional geography highlighting on map

### 1.4 MLA Directory
- **Table:** No | Constituency | MLA | Party | Alliance | Reserved
- **Filters:** Party, Alliance, Reserved
- **Link-outs:** Constituency Page, Party View

### 1.5 Reserved Seats View
- **Tabs/filters:** SC | ST
- **Table:** No | Constituency | 2020 winner (MLA) | Party | Electors | Margin

---

## 2) Data Ingestion & Model

### 2.1 Sources (assumed available)

Updated (available now):
- Constituencies base: `bihar_constituencies.json` — `{no, name, slug, district, reserved, lok_sabha_no, lok_sabha}`
- Constituency SVG: `Bihar_const.svg` — 243 `<path>` elements
- Results per seat (JSON): `2010_results.json`, `2015_results.json`, `2020_results.json` — district‑keyed arrays `{ "#", Name, Winner {Candidate, Party, Votes}, Runner up {Candidate, Party, Votes}, Margin }`
- MLAs current (Wikipedia): `mla_current.csv` — `{no, mla, party, alliance}` (sparse for some seats)
- Party metadata: `parties.json` — `{code, name, alliance, color}`
- **Constituencies base:** `bihar_constituencies.json` (243 rows) → `{no, name, slug, reserved}`
- **Constituency SVG:** `Bihar_const.svg` → 243 `<path>` elements
- **Voter roll (ECI PDF):** `electors_2024.csv` (derived) → `{no, electors, shifted}`
- **2020 Results per seat:** `results_2020.csv` → `{no, winner, winner_party, runner_up, runner_up_party, votes_winner, votes_runner_up, vote_share_winner, vote_share_runner_up, margin, turnout}`
- **MLAs current (Wikipedia):** `mla_current.csv` → `{no, mla, party, alliance}`
- **Party metadata:** `parties.json` → `{code, name, alliance}`

> Normalize party codes: `BJP, JD(U), RJD, INC, CPI, CPI(M), CPI(ML)L, HAM(S), AIMIM, VIP, BSP, IND`

### 2.2 Unified Schema (DB or static JSON build)
**Table: `constituency`**
```json
{
  "no": 178,
  "name": "Mokama",
  "slug": "mokama",
  "reserved": null,
  "mla": "Rajiv Lochan Narayan Singh",
  "mla_party": "JD(U)",
  "mla_alliance": "NDA",
  "electors_2024": 312456,
  "shifted_2024": 2987,
  "results_2020": {
    "winner": "Anant Kumar Singh",
    "winner_party": "RJD",
    "runner_up": "X",
    "runner_up_party": "Y",
    "votes_winner": 0,
    "votes_runner_up": 0,
    "vote_share_winner": 0.0,
    "vote_share_runner_up": 0.0,
    "margin": 0,
    "turnout": 0.0
  }
}
```

Minimal schema (current scope, no electors/percentages):
```json
{
  "no": 178,
  "name": "Mokama",
  "slug": "mokama",
  "reserved": null,
  "mla": "Rajiv Lochan Narayan Singh",
  "mla_party": "JD(U)",
  "mla_alliance": "NDA",
  "results_2010": { "winner": "…", "winner_party": "…", "runner_up": "…", "runner_up_party": "…", "votes_winner": 0, "votes_runner_up": 0, "margin": 0 },
  "results_2015": { "winner": "…", "winner_party": "…", "runner_up": "…", "runner_up_party": "…", "votes_winner": 0, "votes_runner_up": 0, "margin": 0 },
  "results_2020": { "winner": "…", "winner_party": "…", "runner_up": "…", "runner_up_party": "…", "votes_winner": 0, "votes_runner_up": 0, "margin": 0 }
}
```

**Table: `party_seats_2020` (optional precomp)**  
`{ party: "BJP", seats: 74 }` etc.

**Table: `party_current` (composition today)`**  
`{ party: "BJP", seats: 84, alliance: "NDA" }` etc.

> Prefer a **static build step** that merges sources into one `constituencies_full.json` for the app to consume.

### 2.3 Build Pipeline
1. Parse/validate `bihar_constituencies.json` (243 unique nos/slugs).
2. Join `electors_2024.csv` on `no`.
3. Join `results_2020.csv` on `no` (validate winner vs MLA when applicable).
4. Join `mla_current.csv` on `no`.
5. Output:
   - `constituencies_full.json` (243 objects)
   - `party_current.json` (party → seats, alliance)
   - `party_constituencies.json` (party → [nos])
   - `reserved_index.json` (SC/ST lists)

### 2.3 Build Pipeline (revised)
1. Parse/validate `bihar_constituencies.json` (243 unique nos/slugs).
2. Join results from JSON (2010/2015/2020) by seat number `#`.
3. Join `mla_current.csv` on `no` (apply party code normalization with `parties.json`).
4. Output:
   - `constituencies_full.json` (243 objects; identity + MLA + results for 2010/2015/2020)
   - `party_current.json` (party → seats, alliance)
   - `party_constituencies.json` (party → [nos])
   - `reserved_index.json` (SC/ST lists)

---

## 3) Map Integration (SVG → Interactivity)

### 3.1 Strategy
- **Inline** SVG for accessibility & CSS control; **don’t** use `<img>`.
- Ensure a **stable order** of `<path>` elements (1..243). If there’s a background path, skip it once.
- Attach data at runtime by index:
```js
const CONSTS = /* load constituencies_full.json */;
const paths = [...document.querySelectorAll('#bihar-const path')];
let idx = 1;
for (const p of paths) {
  if (!CONSTS[idx]) continue; // skip background if needed
  p.dataset.no = idx;
  p.setAttribute('tabindex','0');
  p.setAttribute('role','link');
  idx++;
}
```
- Tooltip on `mousemove` shows: `#{no} {name} — {reserved||'General'} — {mla_party||winner_party_2020} — margin`

### 3.2 Accessibility
- `role="img"` on `<svg>` with `<title>` and `<desc>`
- Each path focusable (`tabindex="0"`) + keyboard activation (`Enter/Space` → navigate)
- Sufficient hover/focus contrast; stroke highlight on focus

### 3.3 Performance
- Debounce tooltip position updates
- Avoid heavy filters; use `will-change: transform` sparingly
- Lazy-load chart bundles (code-splitting)

---

## 4) Frontend Architecture

- **Tech:** React/Next.js (or your stack), Tailwind for styles, lightweight chart lib (Recharts/Chart.js).
- **Routing:**
  - `/bihar` (Hub)
  - `/bihar/constituencies` (Directory)
  - `/bihar/constituency/[slug]` (Detail)
  - `/bihar/parties` (Seat share + list)
  - `/bihar/mlas` (Directory)
- **State/Data:**
  - Static JSON fetch at build-time (SSG) + client-side for map tooltips.
  - Optional ISR if you plan updates pre‑election.
- **Components:**
  - `ConstituencyMap` (SVG + tooltip)
  - `ConstituencyTable` (search/filter/sort)
  - `ReservedBadge` (SC/ST)
  - `PartySeatBar`
  - `ResultCard2020` (winner, margin, share, turnout)
  - `StatCard` (snapshot)
  - `MLATable`

---

## 5) SEO, Sharing, and Schema

- **Metadata per constituency:** title `"{Name} Assembly Constituency (Bihar) – 2025"`, description with 2020 result summary.
- **OpenGraph/Twitter cards:** basic summary + party winner color/icon.
- **Structured data (JSON-LD):** `Dataset` for the hub; `Article`/`Place`-like for seat pages (lightweight, avoid overfitting).

---

## 6) QA & Data Validation

- **Counts:** 243 constituencies, 38+2 reserved.
- **Slug resolution:** Every `slug` returns 200 + correct page.
- **Map binding:** Random sample click → slug matches page `no` and `name`.
- **Result math:** `votes_winner - votes_runner_up == margin` (or close if multi‑corner); vote shares sum sanity.
- **Accessibility:** Keyboard navigation across all map regions; skip-link to directory.
- **Mobile:** Hit targets ≥ 40px; tooltip position adjusted for touch (press to pin).

---

## 7) Analytics & Metrics

- Track: map interactions (hover/click), search usage, filter adoption (SC/ST), time on constituency pages, party view navigation.
- Event names: `map_hover`, `map_click`, `search_query`, `filter_reserved`, `nav_party_view`.

---

## 8) Security & Compliance

- Cite sources on “About Data” page (ECI PDF; Wikipedia current composition).  
- For 2020 results, include attribution to ECI press notes/data repository if used.

---

## 9) Delivery Plan & Milestones

**Week 1**
- Data pipeline: merge JSON + CSVs → `constituencies_full.json`
- Map integration (click/tooltip), Hub scaffold
- Constituency directory (search/filter)

**Week 2**
- Constituency pages with 2020 results + electors/shifted
- Party view + MLA directory
- SEO metadata + About Data page
- QA pass (map/slug/accessibility)

**Week 3 (buffer/Polish)**
- Charts (seat share, vote share trend)
- Perf + accessibility improvements
- Analytics events
- Content review & launch checks

---

## 10) Example Data Contracts

### 10.1 `constituencies_full.json` (excerpt)
```json
{
  "178": {
    "no": 178,
    "slug": "mokama",
    "name": "Mokama",
    "reserved": null,
    "electors_2024": 312456,
    "shifted_2024": 2987,
    "mla": "Rajiv Lochan Narayan Singh",
    "mla_party": "JD(U)",
    "mla_alliance": "NDA",
    "results_2020": {
      "winner": "Anant Kumar Singh",
      "winner_party": "RJD",
      "runner_up": "X",
      "runner_up_party": "Y",
      "votes_winner": 0,
      "votes_runner_up": 0,
      "vote_share_winner": 0.0,
      "vote_share_runner_up": 0.0,
      "margin": 0,
      "turnout": 0.0
    }
  }
}
```

### 10.2 Party composition (current)
```json
[
  {"party":"BJP","seats":84,"alliance":"NDA"},
  {"party":"JD(U)","seats":48,"alliance":"NDA"},
  {"party":"RJD","seats":72,"alliance":"MGB"}
]
```

### 10.3 MLA directory row
```json
{"no":184,"constituency":"Patna Sahib","mla":"Nand Kishore Yadav","party":"BJP","alliance":"NDA","reserved":null}
```

---

## 11) Implementation Tips

- Keep party colors in a config (`partyColors.ts`) and *don’t* encode them in data.
- Use **debounced** search and client-side fuzzy matching (e.g., fuse.js) for constituency names.
- Pre-generate **search index** (constituency name → no/slug) to keep bundle small.
- For map: add a **hit-area stroke** so small constituencies are tappable on mobile.

---

## 12) Cut-Line Options (if timelines slip)

- Defer trend charts; show text KPIs only.
- Defer MLA directory, keep only MLA on seat pages + hub composition.
- Use static tables before wiring the map; add interactivity later.

---

## 14) Artifacts Added (This Iteration)

- `constituency_viewer.html` — Browser viewer to explore any seat by number with 2010/2015/2020 results, current MLA, and trend (2010→2015, 2015→2020).
- `scripts/constituency_info.py` — CLI to emit merged JSON per seat with party code normalization via `parties.json`.
- Results inputs: `2010_results.json`, `2015_results.json`, `2020_results.json` (district‑keyed JSONs).
- Party metadata: `parties.json` (names, alliance, colors; used for labeling and bars).

---

## 13) Launch Checklist

- [ ] 243 pages build without errors
- [ ] Hub map → each page navigation OK
- [ ] Reserved filters SC/ST correct counts
- [ ] Party seat share equals sum of constituency winners (2020) or current comp (clearly labeled)
- [ ] Accessibility audit: keyboard map navigation, alt text, ARIA
- [ ] About Data page with attributions
- [ ] Analytics events verified
