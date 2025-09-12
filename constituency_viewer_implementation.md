# Constituency Viewer — Implementation Overview

This document outlines the current implementation of `constituency_viewer.html` in this folder.

## Purpose
- Single‑file, client‑side viewer for Bihar Assembly constituency details and results.
- Lets users enter a seat number (1–243) and view current MLA, party, trends, and election results for 2010/2015/2020.

## How To Run
- Serve the folder over a local web server so `fetch(...)` can load local JSON files.
  - Example: `python -m http.server` and open `http://localhost:8000/constituency_viewer.html`.
- Enter a constituency number and click “Load”.

## Files and Dependencies
- HTML/JS/CSS: All inline in `constituency_viewer.html` (no external libraries).
- Data JSON files expected alongside the HTML:
  - `bihar_constituencies.json` — seat metadata (name, district, reservation)
  - `parties.json` — party code → { name, color }
  - `2010_results.normalized.json` — results (per district array collections)
  - `2015_results.normalized.json` — results (per district array collections)
  - `2020_results.normalized.json` — results (per district array collections)
  - `current_mla.json` — current MLA data (per district arrays)

The file paths are configured via the `FILES` constant inside the HTML script.

## Data Contracts (what the viewer reads)
- `bihar_constituencies.json`
  - Shape: object keyed by string seat number → `{ name, district, reserved? }`.
  - Used fields: `name`, `district`, `reserved`.
- `parties.json`
  - Array of `{ code, name, color }`.
  - Indexed by `code` for display names and color bars.
- `20xx_results.normalized.json` (2010, 2015, 2020)
  - Shape: object keyed by district → array of records for each seat.
  - Used fields in each seat record:
    - `#` (seat number)
    - `Winner` → `{ Candidate, Party, Votes }`
    - `Runner up` → `{ Candidate, Party, Votes }`
    - `Margin` (string/number, commas tolerated)
- `current_mla.json`
  - Shape: object keyed by district → array of rows with columns:
    - `No.` (seat number), `Constituency`, `Name`, `Party`, `Alliance`, `Remarks`

## UI Structure (major sections)
- Header bar: title and placeholder icons.
- Search section: numeric input for seat no. and Load button; status text.
- Output area:
  - Constituency header card: title, district, reservation type.
  - Current MLA card: name, party, alliance, party badge color.
  - Political Trends card: horizontal timeline (2010 → 2015 → 2020) with HOLD/GAIN connectors.
  - Three election result cards (2020, 2015, 2010) with winner/runner details, vote bars, and margin classification.

## Core Logic Flow
1. `loadAll()`
   - Fetches all JSON files in parallel (`FILES`), converts to JSON.
   - Builds `partiesIdx` (map by party `code`).
   - Builds `byNo(n)` to look up constituency metadata by seat number.
   - Builds `mlaIdx` (map seat no. → MLA row) from `current_mla.json`.
   - Returns `{ partiesIdx, byNo, r2010, r2015, r2020, mlaIdx }`.
2. `renderSeat(seatNo, data)`
   - Gets base metadata via `byNo(seatNo)`; if missing, shows an error.
   - Locates seat records in `r2010`, `r2015`, `r2020` by scanning districts and matching `'#'`.
   - Renders:
     - Header + current MLA using `enrichParty()` for name/color.
     - Trends via `renderEnhancedTrends(...)` (2010→2015→2020 with HOLD/GAIN labels).
     - Year blocks via `renderYearBlock(year, rec, partiesIdx)`.
3. `renderYearBlock(...)`
   - Extracts winner/runner, normalizes party, parses votes and margin.
   - Computes bar widths as percent of max(winnerVotes, runnerVotes).
   - Classifies margin: Close (≤5k), Moderate (≤20k), Comfortable (>20k).
4. `computeTrend(...)` and `renderEnhancedTrends(...)`
   - Normalize party codes and derive HOLD/GAIN between adjacent elections.
   - Timeline shows per‑year candidate and party badge, with connectors.

## Party Normalization
- `normalizeParty(code)` maps common variants to canonical codes via `PARTY_NORMALIZE`:
  - Examples: `JDU` → `JD(U)`, `CPM` → `CPI(M)`, `HAM` → `HAM(S)`, `Ind` → `IND`.
- `enrichParty(code, partiesIdx)` returns `{ code, name, color }` with a fallback color if unknown.

## Styling and Responsiveness
- Mobile‑first layout with responsive grids at `768px` and `1024px` breakpoints.
- Cards, badges, and bars styled with inline CSS variables; no external CSS.
- Horizontal timeline is scrollable on small screens, with snap alignment.

## Known Limitations / Notes
- Must be served over HTTP(S) to load local JSON via `fetch`.
- If any JSON is missing or malformed, status shows failure and a helpful message renders in output.
- Minor text artifacts may exist in separators/labels due to special characters; worth reviewing if seen in UI.
- Results are limited to 2010/2015/2020; additional years require extending the data and rendering logic.

## Extending / Customizing
- Add more elections: extend `FILES`, fetch logic, trend computation, and year blocks.
- Additional datasets (e.g., turnout) can be added as new cards under the results grid.
- Expand `PARTY_NORMALIZE` and `parties.json` to cover more aliases and define consistent colors.

