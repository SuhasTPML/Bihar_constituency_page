# CSV Widgets Architecture

This document describes how the CSV embed widgets are produced by the generator in `generate_widgets_csv.py`, what each widget contains, and how they are intended to be used in a CMS.

## Overview

- Entry point: `generate_widgets_csv.py` (run with `python3 generate_widgets_csv.py`).
- Input data: `bihar_election_results_consolidated.json` (and optionally `parties.json` in other tools; CSV widgets currently use consolidated only).
- Output: `constituency_widgets_export.csv` containing one row per constituency and five widget columns:
  - `widget_2025_results` (dynamic 2025 card)
  - `widget_current_mla` (dynamic MLA block; auto‑hides if 2025 exists)
  - `widget_timeline` (dynamic three‑card past results: 2020/2015/2010)
  - `widget_grid` (static three‑card past results)
  - `widget_map` (iframe to the universal map)

All dynamic widgets are self‑contained HTML strings with inline, scoped CSS and a small `<script>` to fetch consolidated data and render markup. They are designed to be pasted into a CMS “Raw HTML/Embed” block.

## Data + Environment Detection

- Data source switching is based on the page host:
  - Sandbox/quintype hosts → `https://dh-sandbox-web.quintype.io/...`
  - Otherwise → GitHub Pages `https://suhastpml.github.io/Bihar_constituency_page/...`
- Dynamic widgets fetch:
  - `bihar_election_results_consolidated` (JSON array)
- The generator uses consolidated values for winner/runner/margin/votes, formatting integers via `toLocaleString('en-IN')` in JS.

## CSV Generation Flow

1. Load consolidated JSON and iterate constituencies.
2. For each constituency, compute:
   - `headline` and `body_text` (using the same wording style as `generate_constituency_writeups.py`).
3. Build widget strings via helper functions:
   - `generate_2025_widget_v2`
   - `generate_mla_widget_v2`
   - `generate_timeline_widget_v2`
   - `generate_grid_widget`
   - `generate_map_widget`
4. Write a CSV row with all columns.

CSV writer is configured with `QUOTE_MINIMAL` to avoid double‑quoting HTML when copying from spreadsheet views.

## Widget Templates (Structure)

All dynamic widgets share a similar pattern:

- A unique, per‑row host `<div>` id (e.g., `bihar-2025-<slug>`, `bihar-mla-<slug>`, `bihar-pastresults-<slug>`).
- A `<style>` block with CSS scoped under the host id (so styles don’t leak).
- A placeholder HTML block (e.g., loader card) for graceful initial state.
- A `<script>` that:
  - Detects host to pick data endpoint.
  - Fetches consolidated JSON.
  - Finds the row by `slug` (hardcoded in the widget string).
  - Computes bars, margins, formatted numbers.
  - Injects final HTML into the host element.

To make pasting safe into CMS:
- Attributes use single quotes.
- Special characters use entities (`&mdash;`, `&bull;`).
- Markup includes `.candidate-info` wrappers to align with the CMS generator visuals.

### 2025 Results (dynamic)

- Function: `generate_2025_widget_v2`.
- Renders two bars (winner/runner) and a margin line.
- Hides placeholder when 2025 data exists.

### Current MLA (dynamic)

- Function: `generate_mla_widget_v2`.
- Title: `<name> Current MLA`.
- Displays MLA name, party, and `Alliance: ...`.
- Auto‑hides when 2025 results exist (so the 2025 card becomes the primary block).

### Past Results (dynamic three‑card)

- Function: `generate_timeline_widget_v2`.
- Renders 2020, 2015, 2010 as three cards with winner/runner bars and margin.

### Historical Grid (static)

- Function: `generate_grid_widget`.
- Pure HTML; no JS; always renders 2020/2015/2010 with formatted numbers present in consolidated JSON.

### Map (iframe)

- Function: `generate_map_widget`.
- Emits an iframe pointing to `map.html` hosted on GitHub Pages.
- The map handles its own query params/state.

## Differences vs CMS Generator Widgets

- Slug handling: CSV widgets hardcode slug per row; the CMS generator uses a constant id and extracts slug from the URL, making it universal. CSV widgets are intended to be unique per article (copy the one for that constituency).
- Party enrichment: CMS widgets also fetch `parties.json` for canonical names/colors. CSV dynamic widgets currently render parties as in consolidated data; adding enrichment is possible if needed.
- Robustness: CMS widgets retry initialization and watch DOM changes; CSV widgets perform a single render on load.

## Usage Guidelines

- Paste CSV widgets into a **Raw HTML/Embed** block (not rich text). Do not paste surrounding CSV quotes.
- Verify on page:
  - `!!document.getElementById('<host-id>')` is `true`.
  - Data fetch returns `200`.
- If inline scripts are sanitized by the CMS, switch to iframe embeds or use the CMS‑generator dynamic snippet.

## Error Handling

- If the host element is not found, the script aborts.
- If the fetch fails or the slug is missing in data, the placeholder remains (or an inline error appears for past results widget).
- All dynamic widgets use defensive parsing for numeric fields.

## Extensibility Roadmap

- Add `static_2025` widget column (no JS) for pre‑/post‑results.
- Add party enrichment (fetch `parties.json`) to mirror CMS visuals exactly.
- Switch dynamic CSV widgets to universal mode (extract slug from URL) when embedding across multiple pages.
- Add optional canonical `<title>`/`<link rel="canonical">` injection hooks when used as standalone embeds.

## Files

- Generator: `generate_widgets_csv.py`
- Input data: `bihar_election_results_consolidated.json`
- Output CSV: `constituency_widgets_export.csv`
- Related docs: `docs/cms_implementation_plan.md`, `constituency_writeups/` (for narrative content style)

