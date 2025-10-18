# Bihar Constituency Pages — CMS Implementation (Final)

## Approach
- Use the CSV-hosted widgets only, from `widget-embeds- csv hosted/`.
- Widgets are constituency-agnostic: they resolve the constituency from the parent page URL where they are embedded (slug/name in URL), with fallbacks.
- The same embed code is used across all constituency pages; no per-seat customization is required.
- JSON-hosted widgets, dynamic script embeds, and static exporters are out of scope for CMS.

## Data Sources (Google Sheets CSV)
- Parties CSV: code, name, color, alliance_2010/2015/2020/2025 (published as CSV).
- Results CSV: per-constituency rows for 2010/2015/2020/2025 winner/runner and votes (published as CSV).
- Alliances CSV: alliance name and color overrides (published as CSV).
Widgets already point to the published CSV endpoints.

## Constituency Resolution
- Primary: derive slug from the parent page URL (e.g., `valmiki-nagar-assembly-election-2025-1400072` → `valmiki-nagar`).
- Fallbacks supported by widgets:
  - Query string: `?ac=021` or `?name=valmiki-nagar` where applicable.
  - If unmatched, widgets show a clear message prompting to provide `ac` or a valid slug in URL.

## Leading Support (2025 Live Staging) — CSV Widgets
We will implement “leading (name/party)” in the CSV widgets (map and 2025 results) and we will not show any leading vote counts or leading margins.

Data additions in Results CSV
- Required: `y2025_leading_name`, `y2025_leading_party`.
- Note: We will not parse or display leading votes or margins.
Existing winner fields remain: `y2025_winner_name`, `y2025_winner_party`, `y2025_winner_votes`, `y2025_margin`.

Stage detection (per seat)
- Before: no leading and no winner → show pre-results state.
- During (live): leading present, winner absent → render “Leading”.
- Mixed live: both present → Winner takes precedence; Leading can be shown as secondary where useful.
- After (final): winner present, leading absent → final state.
Treat "-", "NA", and empty as absent.

Global enablement (dataset level)
- Enable 2025 color modes only if every seat has either a valid Leading (name+party) or a valid Winner (name+party).
- If any seat has neither, default to 2020 modes and show pre-results overlay in the 2025 Results widget.

Widget behavior
- 2025 Results (CSV: `widget-embeds- csv hosted/2025 results.html`)
  - Parse leading columns and compute stage.
  - During: show “Leading: <Name> (<Party>)” and a short “Check back later for winners.” message. Do not show leading votes or margin.
  - After: render current Winner/Runner layout (unchanged).
  - Mixed: treat as After; optionally show a small “Earlier leading: …” (name/party only).
  - Accessibility: add `aria-live="polite"` for the live status line (optional).

- Map (CSV: `widget-embeds- csv hosted/map csv.html`)
  - Parse leading columns alongside winners.
  - In 2025 modes: for each seat choose Winner if present; otherwise choose Leading for fill color and legend counts.
  - Bottom sheet: when using leading, show “Leading: <Name> (<Party>, <Alliance>)”. Do not show leading votes or margin.
  - Optionally show a small “2025 Live” chip near the color selector when any seat is using Leading.
  - `enable2025` continues to gate visibility; dataset-level rule above governs defaulting.
  - Optional QA flag: `forceLive=1` to prefer leading when both exist.

## Embedding in CMS
- Use the CSV widget files in `widget-embeds- csv hosted/` (Results 2025, Current MLA, Timeline, Historical Grid, Map).
- Paste their provided embed snippet into CMS raw/HTML blocks.
- No per-seat parameters needed for normal usage; widgets auto-resolve seat from parent URL.
- Optional overrides: `?ac=` or `?name=` for specific cases.

## Acceptance Criteria / QA
- When only leading is present, both the 2025 Results widget and the map reflect leading consistently (labels, colors, legend) without showing leading votes/margins.
- When winner data arrives, both switch to final automatically with no regressions.
- 2010/2015/2020 views remain unchanged.

## Detailed Plan: Leading Implementation (CSV)

Phased Plan (execution order)
- Phase A: Sheets + Apps Script — Completed
  - Use `widget-embeds- csv hosted/gsheets_pipeline.gs` to seed dummy leading data.
  - Every action opens a sheet selector (results/parties as appropriate) before running.
  - New menu items under “2025 Placeholders”: “Seed 2025 Leading (from 2020 winners)” and “Clear 2025 Leading (name/party)”.
  - Columns `y2025_leading_name` and `y2025_leading_party` are ensured if missing; seeding populates blanks from 2020 winners.
- Phase B: 2025 Results widget (CSV)
  - Implement parsing and stage rendering with “Leading: Name (Party)” (no votes/margins) and pre-results/after states.
- Phase C: Map (CSV)
  - Implement 2025 coloring/legend using Winner else Leading; bottom-sheet label “Leading …”; optional “2025 Live” chip.

1) Data schema and validation
- Columns (Results CSV): `y2025_leading_name`, `y2025_leading_party` (required). We will not add or use leading vote or margin columns.
- Normalization: trim, treat `"-"`, `"NA"`, `""` as absent.
- Party code normalization: reuse existing map of party codes → names/colors; default color for unknown codes.

2) Parser changes (CSV widgets)
- Files: `widget-embeds- csv hosted/2025 results.html`, `widget-embeds- csv hosted/map csv.html`.
- Extend CSV row-to-object mapping to include the new leading fields.
- Helper: `parseLeading(row)` → `{ name, party } | null` (no votes/margin).

3) Stage detection (per seat)
- Helper: `stageForRow(row)` returns one of `before | live | mixed | final`:
  - `before`: no `winner` and no `leading`.
  - `live`: leading present, winner absent.
  - `mixed`: both present (winner takes precedence in UI).
  - `final`: winner present, leading absent.

4) Dataset-level enablement for 2025 modes
- Compute once after CSV load: `canEnable2025 = every(row => hasWinner(row) || hasLeading(row))`.
- If `false`, hide 2025 modes in map and show pre-results overlay in the 2025 Results widget.
- Keep honoring `enable2025` query flag; staging logic sits behind it.

5) Coloring and legend (map csv.html)
- Seat coloring in 2025 modes:
  - For each seat: use Winner party if available, otherwise Leading party.
  - Alliance resolution: same path (party → alliances CSV overrides) for both Winner/Leading.
- Legend counts: compute from the same source as fill (Winner first, else Leading) to keep legend aligned with map fills.
- UI chip: show a small `2025 Live` indicator near the color selector if any seat used Leading.

6) Bottom sheet details (map csv.html)
- When 2025 modes are active:
  - Winner present → show current behavior (winner details, party, alliance).
  - Winner absent and Leading present → show label `Leading:` and render `Name (Party, Alliance)`; do not show leading votes or margin.
- Ensure copy switches back to `Winner` automatically when winner data appears.

7) 2025 Results widget (2025 results.html)
- Compute `stage = stageForRow(row)` and render:
  - `before`: show existing pre-results overlay.
  - `live`: show `Leading: <Name> (<Party>)` and a short subtext `Check back later for winners.` Do not show leading votes or margin.
  - `final` or `mixed`: render the Winner/Runner layout (unchanged for final); optional small `Earlier leading: …` (name/party only) for mixed.
- Accessibility: add `aria-live="polite"` to the live status line to announce changes.

8) URL flags and overrides
- Continue to support `enable2025` to show/hide 2025 modes.
- Add optional `forceLive=1` (QA only): prefer Leading even when Winner exists; do not ship this surfaced in UI.
- Existing overrides (`?ac=`, `?name=`) keep working; they do not affect staging.

9) Edge cases and resilience
- Unknown party codes: fall back to neutral color and `code` label; alliance `Unknown`.
- Missing alliance override: derive from party alliances map; if absent, keep neutral styling.
- Data glitches: if both leading and winner are malformed, fall back to `before` stage for that seat.
- Independent (`IND`) color stays gray by design.
- Leading vote counts/margins, if present in source data, are ignored and never displayed.

10) QA checklist
- Datasets: craft samples with (a) all-leading, no-winner; (b) mixed; (c) all-final; (d) some missing both (to verify 2025 disabled).
- Verify: map fills, legend counts, bottom-sheet labeling (no leading vote/margin), and the `2025 Live` chip conditions.
- Verify 2025 Results widget renders the proper state texts and switches automatically when data changes (no leading vote/margin).
- Mobile/desktop layouts; keyboard focus for chip/toggles; `aria-live` announcements.

11) Performance and code hygiene
- Parse CSV once; build per-seat objects with both winner and leading.
- Avoid repeated string parsing in render loops; precompute normalized values.
- Guard DOM updates (only update changed parts to avoid jank on live updates).

12) Rollout
- Add columns in Sheets; publish updated CSVs.
- Implement widget changes; deploy.
- Editorial note: no per-seat parameters required; widgets resolve seat from page URL; 2025 behavior auto-detected from data.
