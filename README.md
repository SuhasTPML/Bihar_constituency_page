# Bihar Constituency Page

This repository powers the constituency viewer and interactive map for Bihar results.

- Live viewer: `index.html` (reads JSON from this repo’s GitHub Pages)
- Interactive map: `map.html` (2025-aware, remote-first with local fallback)

## Data Sources

- `parties.json`: per-year alliances under `alliances` (2010/2015/2020/2025) and `code`, `name`, `color`.
- `bihar_election_results_consolidated.json`: consolidated results per seat with 2010/2015/2020/2025 blocks + current MLA.

Both are served from GitHub Pages at:

- https://suhastpml.github.io/Bihar_constituency_page/parties.json
- https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json

## Wiring (Viewer and Map)

- Viewer (`index.html`)
  - Data source toggle: Sandbox vs GitHub Pages (persists with `?source=` param).
  - “Results announced” adds `enable2025=1` to the map iframe, so the map defaults to 2025 view.
  - Section title changed to “Past Results”.

- Map (`map.html`)
  - Reads `enable2025=1/0` from URL. When enabled, default is “2025 Alliance/Party”, and bottom sheet’s “Current MLA” reflects 2025 winner.
  - Data endpoints: parties/results/geojson all point to this repo’s GH Pages with local fallback; fetch uses `cache: 'no-store'`.
  - Legends: Alliance legends include counts; Party legends show top parties (including 2025).

## Drive JSON from Google Sheets

A complete guide for connecting Google Sheets → JSON (Apps Script Web App or publishing to this repo) is in:

- `docs/sheets-to-json.md`

It includes:
- Apps Script to serve JSON over HTTPS (`doGet?file=parties|results`).
- Publisher script to push static JSON to this repo via GitHub API for best performance.

## Local development

Serve files locally to avoid CORS issues (for `file://`):

```bash
# Python 3
python -m http.server 8000
# then open http://localhost:8000/index.html
```

## Notes

- Colors for party “IND” are grey by design (independents); to change a seat’s color in “Party” modes, update its `yYYYY_winner_party` to the desired party code.
- Margin displayed comes from JSON if present; otherwise computed as winner_votes − runner_votes.

