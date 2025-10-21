# Bihar Election Widgets - State Documentation

This document maps out what users see for each widget based on data availability (2025 leading/winner data). Widgets are ordered as they appear on the page.

## Page Structure

Headline (static)
Subtitle (static)
Author (static)
W1: 2025 Results Widget (W1-2025 results.html)
Body Content from CMS (static)
W2: Map Iframe Widget (W2-map iframe.html)
W3: Current MLA Widget (W3-Current mla.html)
W4: Timeline Widget (W4-timeline.html)
W5: Historical Grid Widget (W5-historical grid.html)

---

## Data States Overview

**No 2025 Data**: Neither y2025_winner_name nor y2025_leading_name populated

**Leading Only**: y2025_leading_name populated, but y2025_winner_name empty

**Winner Data**: y2025_winner_name populated (final results declared)

---

## W1: 2025 Results Widget (W1-2025 results.html)

Shows 2025 election results with different states.

**No 2025 Data - Pre-Results State**

Card with semi-transparent overlay displaying: "Results not announced yet. Return on result day to see the outcome."

Skeleton showing grayed placeholder for winner/runner-up with neutral gray bars.

**Leading Only - Live Counting State**

Shows "LEADING: [Candidate Name]" with colored party badge.

Subtext: "(awaiting final result)".

Runner-up shows "To be announced".

Yellow banner at bottom: "Live update: Check back later for winners."

Gray placeholder bars (no actual vote data shown).

**Winner Data - Final Results State**

Shows "WINNER: [Candidate Name]" with colored party badge.

Vote count displayed below winner.

Shows "Runner-up: [Candidate Name]" with colored party badge.

Vote count displayed below runner-up.

Vote percentage bars (green for winner, red for runner-up).

Victory margin displayed at bottom: "MARGIN: [number] votes".

**Notes**: Most dynamic widget with 3 distinct states. Uses nonEmpty() function to validate data (checks for empty, null, "-", "NA"). Leading state includes aria-live="polite" for accessibility.

---

## W2: Map Iframe Widget (W2-map iframe.html)

Shows interactive constituency map in iframe (600px height).

**Widget Behavior**

Always loads and displays the map iframe regardless of 2025 data state. The widget itself does not conditionally render based on leading or winner data.

**Map Functionality Within Iframe (Internal Behavior)**

The map iframe may have its own internal logic to display different states. The iframe source URL passes the constituency name as a parameter.

**No 2025 Data**

Widget: Always displays iframe at 600px height.

Map (inside iframe): May show constituency boundary with neutral/default styling. Internal map logic determines exact display based on data availability.

**Leading Only**

Widget: Always displays iframe at 600px height.

Map (inside iframe): May highlight constituency with "leading" status or different color. Internal map logic handles live counting visualization.

**Winner Data**

Widget: Always displays iframe at 600px height.

Map (inside iframe): May show constituency with winner party color or final result indication. Internal map logic displays declared results.

**Notes**: The widget embed itself is static - it always renders the iframe. All state-dependent behavior happens inside the iframe content. The map URL receives constituency name: either from sandbox endpoint "/Bihar_map_csv?name=[name]" or GitHub Pages "map.html?name=[name]".

---

## W3: Current MLA Widget (W3-Current mla.html)

Shows current sitting MLA from 2020 election.

**No 2025 Data - VISIBLE**

Card titled "[Constituency Name] Current MLA".

Shows MLA name from 2020 election.

Party badge with color.

Alliance badge showing 2020 alliance.

**Leading Only - VISIBLE**

Same as "No 2025 Data" state.

Shows current sitting MLA (no change during counting).

**Winner Data - HIDDEN**

Widget completely removed from DOM.

Renders empty string.

Takes up no visual space on page.

**Notes**: This widget hides completely when 2025 winner is declared. Logic: "Current MLA" becomes outdated once new winner is known. Only checks y2025_winner_name - ignores leading data.

---

## W4: Timeline Widget (W4-timeline.html)

Shows horizontal timeline of election winners across years.

**No 2025 Data - Historical Timeline**

Shows 3 year badges: 2010, 2015, 2020 (left to right chronologically).

Each year shows candidate name and party badge.

Connection lines between years with "HOLD" or "GAIN" labels.

Timeline flows chronologically: 2010 → 2015 → 2020.

Scroll hint visible on mobile: "← Timeline can be scrolled horizontally →".

**Leading Only - Historical Timeline**

Same as "No 2025 Data" state.

Does NOT show 2025 in timeline.

Only displays years with winner data.

Timeline shows: 2010 → 2015 → 2020.

**Winner Data - Full Timeline REVERSED**

Shows 4 year badges: 2025, 2020, 2015, 2010 (left to right, newest first).

Includes 2025 winner with candidate name and party badge.

Timeline flows in reverse chronological order: 2025 → 2020 → 2015 → 2010.

Connection lines show transitions between all 4 elections with "HOLD" or "GAIN" labels.

**Notes**: Timeline reverses order when 2025 winner exists (shows newest first). Leading data is ignored - only processes winner data. Uses recFromConsolidated() which validates winner name before including year. If winner name is empty or null, that year is excluded from timeline.

---

## W5: Historical Grid Widget (W5-historical grid.html)

Shows past election results (2020, 2015, 2010) in card grid format.

**No 2025 Data**

Shows 2020, 2015, 2010 results in grid layout (3 cards).

Each card shows year, winner name, runner-up name, party badges, vote counts, vote percentage bars, and victory margin.

**Leading Only**

Shows 2020, 2015, 2010 results in grid layout (3 cards).

No change from "No 2025 Data" state.

**Winner Data**

Shows 2020, 2015, 2010 results in grid layout (3 cards).

No change from previous states.

**Notes**: This widget never displays 2025 data. Always shows the same historical results regardless of 2025 state. No conditional rendering based on 2025 data. Grid layout changes at breakpoints: mobile (1 column), tablet (2 columns), desktop (3 columns).

---

## User Journey Through Election Day

**Before Results (No Data Available)**

W1 - 2025 Results: Displays "Results not announced yet" overlay with placeholder skeleton.

W2 - Map: Shows constituency map (internal map styling may show neutral/default state).

W3 - Current MLA: Shows 2020 MLA with party and alliance info.

W4 - Timeline: Shows 2010 → 2015 → 2020.

W5 - Historical Grid: Shows 2020, 2015, 2010 results.

**During Counting (Leading Data Only)**

W1 - 2025 Results: Shows "LEADING: [Name]" with yellow "Live update" banner.

W2 - Map: Shows constituency map (internal map may highlight leading status).

W3 - Current MLA: Shows 2020 MLA (no change).

W4 - Timeline: Shows 2010 → 2015 → 2020 (no change, 2025 not included).

W5 - Historical Grid: Shows 2020, 2015, 2010 results (no change).

**After Declaration (Winner Data Available)**

W1 - 2025 Results: Shows full results - winner, runner-up, votes, margin, colored bars.

W2 - Map: Shows constituency map (internal map may show winner party color).

W3 - Current MLA: Widget completely hidden/removed.

W4 - Timeline: Shows 2025 → 2020 → 2015 → 2010 (reversed order, includes 2025).

W5 - Historical Grid: Shows 2020, 2015, 2010 results (no change).

---

## Summary of Widget Behavior

**Static Widgets (Never Change Based on 2025 Data)**

W5 - Historical Grid: Always shows 2020, 2015, 2010.

W2 - Map Iframe: Always displays iframe (internal map content may change).

**Conditional Display Widgets**

W1 - 2025 Results: 3 states (pre-results, leading, winner).

W3 - Current MLA: Show/hide (visible until winner declared, then hidden).

W4 - Timeline: Order reversal (chronological vs reverse chronological, includes/excludes 2025).

**Leading Data Usage**

Only W1 - 2025 Results widget uses y2025_leading_name and y2025_leading_party.

All other widgets ignore leading data completely.

**Winner Data Impact**

W1 - 2025 Results: Switches from skeleton/leading to full results display.

W3 - Current MLA: Hides widget completely.

W4 - Timeline: Adds 2025 to timeline and reverses order (newest first).

W5 - Historical Grid: No impact.

W2 - Map Iframe: Widget unchanged, internal map may update.

---

## Key Data Fields Reference

y2025_winner_name - Full winner name (triggers winner state)

y2025_winner_party - Winner's party code

y2025_winner_votes - Winner's vote count

y2025_runner_name - Runner-up name

y2025_runner_party - Runner-up party code

y2025_runner_votes - Runner-up vote count

y2025_margin - Victory margin in votes

y2025_leading_name - Leading candidate during counting

y2025_leading_party - Leading candidate's party during counting

---

## Empty Data Detection Methods

**W1-2025 results.html**: Uses nonEmpty() function that checks for null, empty string, "-", "NA" (case-insensitive).

**W3-Current mla.html**: Simple check - y2025_winner_name && y2025_winner_name.trim() !== ''.

**W4-timeline.html**: Checks !wName || wName.trim() === '' to exclude year from timeline.

---

## Page Layout Changes During Election Day

**Total Widgets Visible**

Before Results: 5 widgets (W1-2025 Results, W2-Map, W3-Current MLA, W4-Timeline, W5-Historical Grid)

During Counting: 5 widgets (same as before)

After Declaration: 4 widgets (W3-Current MLA hidden, others visible)

**Visual Impact**

The most visible changes users will notice:

1. W1 - 2025 Results widget transitions from skeleton → leading banner → full results
2. W3 - Current MLA widget disappears after winner declared
3. W4 - Timeline adds 2025 and reverses order after winner declared
4. W5 - Historical Grid and W2 - Map remain visually consistent throughout

---

## Appendix: Map CSV Behavior (map csv.html)

This section details how the map iframe content (map csv.html) processes and displays election data.

**Auto-Detection of 2025 Mode**

The map automatically enables 2025 mode if ANY constituency has 2025 data (winner OR leading).

Function: computeEnable2025() checks entire dataset at load time.

If at least one constituency has y2025_winner_name OR y2025_leading_name populated, 2025 modes are enabled.

URL override available: ?enable2025=true or ?enable2025=false forces mode regardless of data.

**Color Mode Dropdown Options**

When 2025 Mode Enabled (default if data exists):
- 2025 Alliance (default selection)
- 2025 Party
- 2020 Alliance
- 2020 Party
- 2015 Alliance
- 2015 Party
- 2010 Alliance
- 2010 Party

When 2025 Mode Disabled (no 2025 data in dataset):
- 2020 Alliance (default selection)
- 2020 Party
- 2015 Alliance
- 2015 Party
- 2010 Alliance
- 2010 Party

**Visual Styling for 2025 Mode**

The map uses three distinct visual patterns when displaying 2025 data:

Winner Declared (y2025_winner_name + y2025_winner_party populated):
Constituency fills with solid pastel color (25% white mix).
Color based on winner's alliance or party (depending on mode selected).
Clean, solid appearance indicates final result.

Leading Only (y2025_leading_name + y2025_leading_party populated, but no winner):
Constituency fills with horizontal stripe pattern (hatched).
Base color is 50% pastel (lighter than winner).
Pattern indicates live/provisional status.
Legend shows: "▤ Horizontal stripes = Leading (live)".

No 2025 Data (neither winner nor leading populated):
Constituency fills with vertical black stripes pattern.
Black base with white vertical lines (40% opacity).
Indicates awaiting results/no data yet.
Legend shows: "║ Vertical stripes = Awaiting results".

**Bottom Sheet Information Panel**

When user clicks/taps a constituency, bottom sheet displays:

Constituency name and district.

Winner-Else-Leading Logic (when 2025 mode enabled):
- If winner data exists: Shows "Winner: [Name]"
- If only leading data exists: Shows "Leading: [Name]"
- If neither exists: Shows "Result: Not available"

Party and Alliance cards with color swatches matching map colors.

"More details →" button (currently logs to console, ready for future implementation).

When 2025 Mode Disabled:
Shows "Current MLA: [Name]" with 2020 election data.

**Data Loading Process**

Map independently fetches same CSV files as other widgets:
- Parties CSV (party codes, names, colors, alliances)
- Results CSV (consolidated election results all years)
- Alliances CSV (alliance color overrides)

Uses identical CMS-safe CSV parser (character-by-character, handles quoted commas).

GeoJSON loaded separately for constituency boundaries.

All data cached in Maps for performance (colorCache, featureByAc, centroidCache).

**Search and Selection**

Search box allows filtering by:
- Constituency number (e.g., "001", "123")
- Constituency name (e.g., "Patna Sahib")
- District name (e.g., "Patna")

URL parameters supported:
- ?ac=001 (selects constituency by number)
- ?name=Patna+Sahib (selects constituency by name)
- Both update URL when user clicks constituencies

**Legend Display**

Alliance Mode Legends:
Shows all alliances present in dataset for selected year.
Each alliance shows count of constituencies won/leading.
Sorted by frequency (most seats first).

Party Mode Legends:
Shows top 6 parties only (to avoid clutter).
Each party shows count of constituencies.

2025 Mode Additions:
Legend includes pattern indicators if applicable:
- Horizontal stripes indicator shown if any constituency has leading-only data
- Vertical stripes indicator shown if any constituency has no 2025 data

**Color Processing**

Original alliance/party colors from CSV are "pastelized" (lightened) for map fill.

Pastelization levels:
- Winner data: 25% white mix (standard pastel)
- Leading data: 50% white mix (lighter/softer)
- Stroke colors use original non-pastelized colors for contrast

Deterministic fallback colors generated for alliances/parties without defined colors.

**Map Controls**

Zoom buttons: + and - for zoom in/out.

Cross button (×): Appears when zoomed or constituency selected. Resets view and clears selection.

Selection behavior:
- Selected constituency gets thicker stroke with original color
- All other constituencies dimmed (30% opacity)
- Zoom to fit selected constituency in view

**Performance Optimizations**

Pre-computed color cache: All color combinations calculated once at load.

Feature cache: O(1) lookup for constituency features by AC number.

Centroid cache: Pre-computed center points for all constituencies.

Lazy loading: Map iframe has loading="lazy" attribute in widget embed.

**Environment Detection**

Map detects two environments:
- Sandbox: Uses dh-sandbox-web.quintype.io endpoints
- GitHub Pages: Uses suhastpml.github.io endpoints

Fallback chain for all resources: Sandbox → GitHub Pages → Local files.

**Data Synchronization**

Map always shows current data from Google Sheets CSVs (no caching, cache: 'no-store').

If CSV data updated while map is open, user must refresh page to see changes.

Map state (selected constituency, zoom level) persisted in URL parameters for sharing.

**Key Behavioral Differences from Other Widgets**

Unlike other widgets, the map:
- Auto-detects 2025 mode based on dataset (not individual constituency)
- Shows ALL constituencies simultaneously with visual differentiation
- Uses patterns (stripes) to indicate data quality/status
- Provides interactive exploration (other widgets are passive displays)
- Switches default year shown based on data availability
