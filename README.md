Bihar Constituency Viewer and Map

Overview
- `index.html`: Constituency viewer with results by year and trends.
- `map.html`: Interactive Bihar assembly map with search, color modes, and details panel.

Data Sources
- `parties.json`: Party metadata and alliances per year (2010/2015/2020/2025), with `code`, `name`, `color`.
- `bihar_election_results_consolidated.json`: Consolidated per‑constituency results (2010/2015/2020/2025) plus current MLA fields.
- `bihar_ac_all.geojson`: GeoJSON of assembly constituencies.

Hosted JSON (GitHub Pages)
- parties: https://suhastpml.github.io/Bihar_constituency_page/parties.json
- results: https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json
- geojson: https://suhastpml.github.io/Bihar_constituency_page/bihar_ac_all.geojson

Both `index.html` and `map.html` load these from GitHub Pages with a local fallback if the network source fails (no-store caching).

End‑User Guide
- Viewer (`index.html`)
  - Displays constituency name, district, and results blocks for 2010/2015/2020/2025 when available.
  - Vote bars compare winner and runner‑up; margin is shown in votes.
  - A trends section summarizes party holds/gains across years.

- Map (`map.html`)
  - Interactions: Click/tap a constituency to view details; search by number/name/district to select.
  - Color Modes: Alliance/Party by year. Legend shows alliance counts or top parties depending on mode.
  - Details Panel: Bottom sheet shows the selected constituency’s winner/MLA, party, and alliance for the active mode/year.

URL Parameters
- `enable2025` (on `map.html`)
  - Controls whether 2025 color modes and winner details are enabled.
  - Values: `1`/`true` to enable, `0`/`false` to disable.
  - Default when absent: disabled (map starts in 2020 modes).

- `ac` (on `map.html`)
  - Preselects a constituency on load, if valid.
  - Example: `map.html?ac=001`.

- `source` (on `index.html`, optional)
  - Implementation detail for switching data source (e.g., sandbox vs GitHub Pages) when supported.

Data Pipeline (Google Sheets → JSON)
- See `docs/sheets-to-json.md` for publishing flow:
  - Apps Script web app to serve JSON.
  - Scripted publishing of static JSON to this repo for fastest loads.

Local Development
- Serve files over HTTP to avoid `file://` CORS issues.

  python -m http.server 8000
  # then open http://localhost:8000/index.html or /map.html

Notes
- Party `IND` (independent) is gray by design. To change a seat’s color in Party modes, update `yYYYY_winner_party` in the consolidated JSON.
- If explicit margin is missing in the data, the viewer computes it as `winner_votes - runner_up_votes`.
