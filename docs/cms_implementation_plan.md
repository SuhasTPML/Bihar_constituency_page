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

1) Add “Copy Block” buttons with handlers:
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

## Next Steps

- Confirm CMS capabilities for `<style>` and `<script>` in HTML blocks.
- If approved, implement the “Copy Block” exports in `Generator.html` and update this plan with button-to-column mapping.
- Optionally add a configuration toggle to choose CSS-only timeline hint behavior in strict CMS environments.
