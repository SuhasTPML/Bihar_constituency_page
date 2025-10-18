# Bihar Constituency Pages — CMS Implementation Plan

## Overview

- Goal: Publish one CMS story per constituency using a self-contained, static embed of the preview generated from `Generator.html` (with pre/post-results modes), while keeping the map as an internal iframe with a fixed `ac` param.
- Output: A DIV-only embed snippet (scoped CSS under a unique container id) pasted into the CMS “HTML” element. No external runtime dependencies beyond the map iframe.

## Two Sheet States (Content Columns Order)

Maintain two tabs/sheets to reflect the two rendering modes. Both share base metadata columns, then state-specific content columns in a strict order.

Base Metadata Columns (placed first, common to both tabs)
1. Constituency Name
2. OG
3. NOT FOR USE
4. Template
5. Author
6. Tags
7. Keywords
8. Primary Section
9. Secondary Section
10. Hero Image URL
11. Published URL

Pre-Results Tab (Before 2025 results are declared)
- Generator mode: `?announced=0` before loading a seat.
- Append these Content Columns after the base metadata:
12. Body Copy
13. Map Iframe (Pre-Results) — use `enable2025=0`
14. Current MLA Embed Code
15. Past Results Timeline Embed Code
16. Actual Past Results Embed Code (2010/2015/2020 cards)

Post-Results Tab (After official 2025 results data available)
- Generator mode: default (or `?announced=1`).
- Append these Content Columns after the base metadata:
12. 2025 Results Embed Code
13. Body Copy
14. Map Iframe (Post-Results) — use `enable2025=1`
15. Past Results Timeline Embed Code
16. Actual Past Results Embed Code (2010/2015/2020 cards)

## Authoring Workflow

1. Open `Generator.html` in the browser.
2. Choose data source if needed (`source=gh` recommended) and optionally force pre-results with `?announced=0`.
3. Enter constituency number and click `Load`.
4. Click `Export Embed` to copy the DIV-only embed snippet to clipboard.
5. Create a new story in the CMS (Quintype) and fill the sheet per the state (Pre or Post) using the content blocks columns below.
6. For each content block, paste the specific embed code (map, MLA, timeline, results) into the corresponding column.
7. Save, preview, and publish.

Notes
- Pre-results: use `Generator.html?announced=0` before loading a seat; export will omit the 2025 block and set `enable2025=0` inside the map iframe.
- Post-results: default mode when 2025 data exists; export will include 2025 block and set `enable2025=1`.
- The embed uses a unique wrapper id and scoped CSS to avoid style interference with the parent page.
- If the CMS sanitizes `<style>` tags, request an allowlist for the story’s HTML element. Fallback option: we can provide a “style-inlined” variant on request (heavier markup).

## Sheet Fields (to share with Quintype)

Provide a Google Sheet with the following columns in this exact order:

1. Constituency Name
2. OG
3. NOT FOR USE
4. Template
5. Author
6. Headline
7. Sub-headline
8. Body Copy
9. Tags
10. Keywords
11. Primary Section
12. Secondary Section
13. Hero Image URL
14. Published URL

Field Guidance
- Constituency Name: Exact display name (matches consolidated data where possible).
- OG: Open Graph title/description notes or overrides.
- NOT FOR USE: Internal flag; leave blank or “No”.
- Template: Use the standard constituency story template.
- Author: CMS author name/ID.
- Headline: See “Two Sheet States” for pre/post suggestions.
- Sub-headline: See “Two Sheet States” for pre/post suggestions.
- Body Copy: Optional intro/context. Keep short; the embed conveys main info.
- Tags/Keywords: SEO and internal tagging.
- Content Blocks (see Two Sheet States): Paste individual blocks rather than a single full embed.
- Primary/Secondary Section: CMS section slugs (e.g., “Elections”, “Bihar”).
- Hero Image URL: Optional image; should be neutral if results not declared.
- Published URL: Filled by the desk after publish.

Preset Rows (recommended usage)
- Pre-Results preset: Fill row per “Pre-Results” guidance; paste pre-results embed; keep Hero neutral; omit explicit 2025 outcomes.
- Post-Results preset: Duplicate the pre-results row when results arrive, update headline/sub-headline/body for outcome, replace Embed Code with post-results embed.

## Embed Code Placement

- CMS Element: Use “HTML” elements (or equivalent raw HTML blocks) for each content block.
- Placement: Recommended order follows the sheet columns for the chosen state.
- Do not wrap inside additional containers that add overflow or padding which could clip the timeline.

## Pre/Post-Results Handling

- Pre-results stories: Force pre-results via `?announced=0` in `Generator.html` before loading and exporting. This shows context, MLA info, map, and past results without 2025.
- Post-results stories: Default mode if 2025 is present in data; export then includes 2025 results, margin block, and updated CMS sections.

## Obtaining Each Content Block from Generator

Run `Generator.html`, load the constituency, then use these selectors to copy specific blocks (open DevTools console and run the snippet to copy to clipboard):

- Map Iframe (Pre/Post)
  - Selector: `#mapEmbed iframe`
  - Snippet: `navigator.clipboard.writeText(document.querySelector('#mapEmbed iframe').outerHTML)`
  - Ensure `enable2025=0` for pre, `1` for post.

- Current MLA Embed Code (Pre only)
  - Selector: `.current-mla-card`
  - Snippet: `navigator.clipboard.writeText(document.querySelector('.current-mla-card').outerHTML)`

- 2025 Results Embed Code (Post only)
  - Find the card where the title contains 2025:
  - Snippet:
    ```js
    (()=>{
      const card = [...document.querySelectorAll('.election-result')]
        .find(n => n.querySelector('.election-title')?.textContent.includes('2025'));
      if (card) navigator.clipboard.writeText(card.outerHTML);
    })();
    ```

- Past Results Timeline Embed Code
  - Selector: `.trends-container`
  - Snippet: `navigator.clipboard.writeText(document.querySelector('.trends-container').outerHTML)`

- Actual Past Results Embed Code (2010/2015/2020)
  - Selector: `.results-container`
  - Snippet: `navigator.clipboard.writeText(document.querySelector('.results-container').outerHTML)`

Notes
- If your browser blocks clipboard writes from the console, select the node in the Elements panel, right-click → Copy → Copy outerHTML.
- For pre vs post variants, re-load with `?announced=0` or `?announced=1` before copying blocks.

## Validation Checklist

- Verify the map loads with the correct fixed `ac` parameter (zero-padded, e.g., `021`).
- Confirm the “timeline scroll” hint appears per rules:
  - Mobile: Always shown.
  - Desktop: Shown when 4 timeline years are present; hidden for 3.
- Confirm styles do not affect, or get affected by, the parent page (scoped CSS inside the embed).
- Test both pre-results and post-results variants for 2–3 constituencies.

## Maintenance Notes

- Data updates (parties, alliances, consolidated results) automatically reflect in `Generator.html` preview; export a fresh embed if content changes.
- If Quintype restricts `<style>` tags:
  - Option A: Ask for an allowlist for the HTML block on this series.
  - Option B: Request a “style-inlined” export variant.

## Support

- For adjustments (font loading, color overrides, layout tweaks), open an issue or share edits to `Generator.html`. We can regenerate consistent embeds in bulk as needed.

## Feasibility Overview

- Feasible: The plan to populate CMS stories using discrete content blocks (map, current MLA, 2025 results, timeline, actual past results) is feasible.
- Styles: Each block must include scoped styles in a `<style>` tag targeting a unique container id to avoid relying on global CSS.
- Minimal JS: Only the past results timeline hint logic needs a small inline script to implement “mobile always, desktop show only for 4 years”. All other blocks are pure HTML/CSS (map is an iframe).

## Block Export Strategy

- Provide per-block exports from `Generator.html` via dedicated “Copy Block” buttons that produce:
  - A container `<div id="...">` with a unique id for the block and constituency.
  - A scoped `<style>` with selectors rewritten to target that id only.
  - The block’s static HTML markup.
  - For the timeline block only: a tiny inline script to toggle the hint according to current rules.
- Keep the existing full-page DIV-only export for teams who prefer a single embed.

## CMS Sanitization Considerations

- If CMS allows `<style>` and `<iframe>` in HTML blocks, the plan works as-is.
- If CMS blocks `<script>` tags:
  - Timeline hint falls back to CSS-only: “always show on mobile,” and pick one desktop policy (always show or always hide). Document the chosen fallback per environment.
- If CMS blocks `<style>` in content blocks, request an allowlist for this project. As a fallback, we can provide a style-inlined variant (converts CSS into `style="..."` on each element) at the cost of heavier markup.

## Implementation Steps in Generator (next changes)

1) Add "Copy Block" buttons with handlers:
   - Map (Pre) — copies iframe with `enable2025=0`
   - Map (Post) — copies iframe with `enable2025=1`
   - Current MLA (Pre)
   - 2025 Results (Post)
   - Past Results Timeline
   - Actual Past Results (2010/2015/2020)
2) Each handler builds a scoped block:
   - Wrap content in a unique container id.
   - Rewrite selectors to that id.
   - Inject inline script only for the timeline hint (if scripts allowed).
3) QA: Verify copied block renders correctly when pasted into a blank HTML page and in the target CMS preview.

## ✅ Static Widget Exporters Implementation (COMPLETED)

**Overview**: Added 5 static (crawlable) widget exporters to `CMS Generator for Embed.html` that generate pre-rendered HTML for SEO/crawlability. This provides an Option A solution where static HTML is pasted into CMS and is immediately crawlable by search engines.

**Implementation Details** (Commit: 46b1247):

### 1. User Interface (Lines 325-340)
Added 5 new static export buttons in a dedicated section:
- **Header (Static)** - Purple button - Exports constituency header with district/seat info
- **2025 Results (Static)** - Pink button - Exports winner/runner-up with vote bars (only when 2025 data exists)
- **Current MLA (Static)** - Purple button - Exports current MLA card (hides when 2025 data exists)
- **Timeline (Static)** - Teal button - Exports election timeline (auto-reverses when 2025 present)
- **Historical Grid (Static)** - Orange button - Exports 2020/2015/2010 results grid

All buttons start disabled and enable only after a constituency is loaded.

### 2. Static Builder Functions (Lines 2391-2615)
Five builder functions that generate standalone HTML with scoped CSS:

**`buildStaticHeaderHTML(state)`** - Generates constituency header
- Shows constituency name, district, and seat type (General/SC/ST)
- Uses unique ID: `bihar-static-header-{seatNo}`
- Returns empty string if no data

**`buildStatic2025ResultsHTML(state)`** - Generates 2025 results card
- Shows winner/runner-up with vote counts and percentage bars
- Displays victory margin
- Returns HTML comment `<!-- No 2025 data available -->` if no 2025 data
- Uses unique ID: `bihar-static-2025-{seatNo}`

**`buildStaticMLAHTML(state)`** - Generates current MLA card
- Shows incumbent MLA name, party, and term info
- Returns HTML comment `<!-- Current MLA hidden when 2025 results exist -->` if 2025 data present
- Uses unique ID: `bihar-static-mla-{seatNo}`

**`buildStaticTimelineHTML(state)`** - Generates election timeline
- Shows historical election results in vertical timeline format
- **Auto-reverses order when 2025 data exists** (newest→oldest)
- Uses existing `renderEnhancedTrends()` function
- Uses unique ID: `bihar-static-timeline-{seatNo}`

**`buildStaticGridHTML(state)`** - Generates historical grid
- Shows 2020, 2015, and 2010 results in card format
- Uses existing `renderYearBlock()` function
- Uses unique ID: `bihar-static-grid-{seatNo}`

### 3. Data Storage (Line 854)
```javascript
window.__lastRenderData = data; // Store data for static exporters
```
Stores constituency data globally when `renderSeat()` is called, allowing static builders to access the same data source.

### 4. Export Handler Functions (Lines 2791-2889)
Five async handler functions that:
- Validate that a constituency is loaded
- Call corresponding builder function
- Check for empty/comment results and show appropriate alerts
- Copy generated HTML to clipboard
- Update status message with success confirmation

**Error Handling**:
- `exportStatic2025()` - Alerts if no 2025 data available
- `exportStaticMLA()` - Alerts if hidden due to 2025 results
- All handlers show clear error if no constituency loaded

### 5. Event Listeners (Lines 2950-2969)
Wired up click event listeners for all 5 static export buttons in the `init()` function.

### 6. Auto-Enable Buttons (Lines 858-861)
```javascript
// Enable static export buttons
['exportStaticHeader','exportStatic2025','exportStaticMLA','exportStaticTimeline','exportStaticGrid'].forEach(id=>{
  const btn = document.getElementById(id);
  if (btn) btn.disabled = false;
});
```
Automatically enables all static buttons when a constituency is successfully loaded.

### How It Works

1. **User loads constituency** (e.g., seat #21 - Patna Sahib)
2. **Static buttons become enabled** automatically
3. **User clicks any static widget button** (e.g., "Timeline (Static)")
4. **Pre-rendered HTML is copied to clipboard** with scoped CSS
5. **User pastes into CMS HTML block** - content displays immediately
6. **Search engines can crawl** the content (no JavaScript required)

### Key Benefits

✅ **SEO Crawlable**: Search engines see actual HTML content in source, not empty divs
✅ **Self-contained**: Each widget has scoped CSS with unique IDs to prevent conflicts
✅ **No JavaScript Required**: Works without client-side code execution
✅ **Modular**: Each widget can be embedded independently
✅ **Timeline Intelligence**: Automatically reverses order when 2025 data exists
✅ **Conditional Rendering**: 2025 Results shows only with data, MLA hides when 2025 exists
✅ **Standalone**: Works exactly like existing "Export Embed" button

### Workflow Example

```
1. Open CMS Generator for Embed.html
2. Enter constituency number (e.g., 21) and click Load
3. Click "Header (Static)" → Copies to clipboard
4. Paste into CMS HTML block → Header appears
5. Click "Timeline (Static)" → Copies to clipboard
6. Paste into CMS HTML block → Timeline appears
7. Click "Historical Grid (Static)" → Copies to clipboard
8. Paste into CMS HTML block → Grid appears
9. Save and publish CMS page
10. Search engines can now crawl all widget content
```

### Technical Notes

- **Scoped CSS**: Uses `buildScopedStylesForId()` to generate CSS that only affects the specific widget
- **Unique IDs**: Each widget uses format `bihar-static-{widgetType}-{seatNo}` (e.g., `bihar-static-timeline-021`)
- **Data Access**: Reads from `window.__lastRenderData` set during `renderSeat()`
- **Reuses Existing Functions**: Leverages `renderYearBlock()`, `renderEnhancedTrends()`, and other existing rendering functions
- **Timeline Reversal Logic**: Checks for 2025 data existence and reverses array if found

### Comparison: Static vs Dynamic Widgets

| Feature | Static Widgets | Dynamic Widgets |
|---------|---------------|-----------------|
| **SEO Crawlable** | ✅ Yes (HTML in source) | ❌ No (JS-generated) |
| **JavaScript Required** | ❌ No | ✅ Yes |
| **Load Time** | ✅ Instant | ⏱️ Requires fetch |
| **Updates with JSON** | ❌ Must regenerate | ✅ Auto-updates |
| **CMS Workflow** | Load → Export → Paste | Paste once (works everywhere) |
| **Use Case** | SEO-critical pages | Flexible embeds |

### Maintenance

- **Data updates**: When JSON files change, regenerate static widgets by loading constituency and re-exporting
- **Bulk regeneration**: Can be scripted if needed (load each constituency and export programmatically)
- **No breaking changes**: Static widgets work independently of dynamic widget updates

## Next Steps

- ✅ **Static widget exporters implemented and tested** (Commit: 46b1247)
- Confirm CMS capabilities for `<style>` and `<script>` in HTML blocks.
- Test static widgets in actual CMS environment (Quintype).
- Consider adding bulk export functionality if many constituencies need static updates.
 - Optionally add a configuration toggle to choose CSS-only timeline hint behavior in strict CMS environments.

## CSV vs JSON widget approaches (summary)

- CSV-hosted widgets (`widget-embeds- csv hosted/`)
  - Pasteable DIV+SCRIPT widgets that fetch from published Google Sheets (Parties, Results, Alliances CSVs).
  - Pros: instant editorial updates from Sheets; no JSON hosting required; matches current CMS embed workflow.
  - Cons: depends on Google Sheets availability; CSV parsing on-page; ensure CMS allows inline `<style>` and `<script>`.

- JSON-hosted widgets (`widget-embeds-json hosted/`)
  - Widgets fetch from `parties.json` and `bihar_election_results_consolidated.json` (GitHub Pages or sandbox), with environment detection and fallbacks.
  - Pros: faster and more predictable loads; fewer parsing edge cases; easier CORS control.
  - Cons: requires republishing JSON to reflect data updates unless automated.

Recommendation: Use CSV widgets for live 2025 embeds and JSON widgets for stable historical content. Both approaches can be mixed per block.

## Live Results Staging (Before → During → After)

Goal
- Add “leading” fields in the Results CSV and support three stages across widgets: Before results, During results (live), and After results (final).
- Update the 2025 Results widget and the D3 Map to reflect the stage automatically.

Feasibility
- Yes. This is a CSV‑only schema addition with small, backward‑compatible changes in two widgets. No backend required beyond updating the Google Sheets.

Data Model (CSV)
- Add the following columns to the Results CSV (same sheet used today):
  - required: `y2025_leading_name`, `y2025_leading_party`
  - optional but recommended: `y2025_leading_votes`, `y2025_leading_margin`
- Existing winner fields remain unchanged: `y2025_winner_name`, `y2025_winner_party`, `y2025_winner_votes`, `y2025_margin`.

Stage Detection Logic (per seat)
- Before: no `y2025_winner_name` and no `y2025_leading_name` → render pre‑results view.
- During (live): `y2025_leading_name` present, `y2025_winner_name` empty → render live view using “Leading”.
- Mixed live: both present → Winner is primary (final), Leading can be shown as secondary where useful.
- After (final): `y2025_winner_name` present, `y2025_leading_name` empty → render final view with Winner only.
- Guardrails: trim values; treat "-", "NA", empty as absent; numeric parsing strips commas.

Global Enablement Rules (dataset‑level)
- 2025 modes are enabled only if every constituency has either a valid Leading (name+party) OR a valid Winner (name+party).
- If even one constituency has neither Leading nor Winner, 2025 modes remain disabled (map defaults to 2020 modes and the 2025 Results block shows the pre‑results overlay where embedded).
- When all constituencies have Leading (name+party) but Winners are not fully populated, 2025 modes use Leading across the map and widgets until Winners start appearing.

Widget Updates
- 2025 Results (CSV embed: `widget-embeds- csv hosted/2025 results.html`)
  - Parsing: include the leading columns listed above.
  - Rendering rules:
    - Before: show the existing pre‑results overlay message.
    - During (leading present, winner absent): render exactly three lines below the heading:
      1) Heading (as is)
      2) Leading: <Name> (<Party>)
      3) Message: “Check back later for winners.”
    - After (winner present): render the current final Winner/Runner layout (unchanged).
    - Mixed live: treat as After (winner takes precedence); optionally include a small “Earlier leading: …” line if desired.
  - Accessibility: add `aria-live="polite"` to the status area for live text (optional).

- Map (CSV page: `widget-embeds- csv hosted/map csv.html`)
  - Data: parse the leading fields into `electionData` alongside winners.
  - 2025 modes enablement: gate on the Global Enablement Rules above.
  - Visuals when enabled:
    - If all constituencies have Leading and some do not yet have Winners, compute fills in `party-2025`/`alliance-2025` from Leading (per seat) and label the UI as Live.
    - For each seat: choose Winner if present; otherwise choose Leading.
  - Legend: compute counts from the same attribute used to color (Winner first, else Leading), so legend matches the map exactly.
  - Bottom sheet (when 2025 mode enabled):
    - Winner present → show Winner (party, alliance colors) — current behavior.
    - Winner absent, Leading present → show “Leading: <Name> (<Party>, <Alliance>)”.
  - UI: optionally show a small “2025 Live” chip near the color selector when any seat is using Leading in 2025 modes.

Alliances and Colors
- Alliance colors remain driven by Alliances CSV overrides; party colors unchanged.
- When using leading, resolve alliance via party for 2025 the same way as winners.

URL Flags (optional)
- Auto‑detect the stage from data by default.
- Optional flag `forceLive=1` to always prefer leading when both exist (QA/testing).
- Existing `enable2025=1` still gates visibility of 2025 modes; staging logic sits behind it.

QA Scenarios
- Seat with only leading → map fills and legend count reflect leading; 2025 widget shows “Leading”.
- Seat with both leading and final → map and widget prefer final; legend shows final counts.
- Seat with neither → widget shows pre‑results overlay; map remains in 2020 modes unless explicitly switched.

Backward Compatibility
- If the new columns don’t exist, behavior is identical to today.
- Leading is ignored when empty; winner logic is unchanged.

Work Breakdown
- Data
  - Add columns to Google Sheets; publish CSV as before.
  - Populate a handful of seats for QA.
- 2025 Results widget (CSV)
  - Parse leading fields; compute stage; render per rules above.
  - Add badges (Leading/Final) and ensure skeleton still displays for Before.
- Map (CSV)
  - Parse leading fields; update color resolution for 2025 modes; update legend to match source attribute; bottom sheet supports leading text.
- Docs
  - Update README notes for live staging once shipped.

Acceptance Criteria
- When only leading is present, both the 2025 Results widget and the map reflect leading consistently (colors, labels, legend).
- When winner data arrives, both switch to final automatically without reload or with a simple refresh.
- No regressions for 2010/2015/2020 modes and non‑2025 widgets.

Estimate
- CSV changes: same‑day.
- Widget code updates: ~1–2 days including QA across a dozen seats.
