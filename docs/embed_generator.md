Great — no iframe wrapper, directly embeddable like your current generator snippets. Here’s a focused plan after reviewing CMS Widget generator.html.

**Approach**
- Keep the current data pipeline (fetch parties, consolidated, alliances) and templates.
- Add a new dynamic “script embed” snippet that:
  - Runs inside the host page (uses `window.location.href`).
  - Parses the page URL to derive the constituency slug (e.g., valmiki-nagar).
  - Fetches JSONs from the same sources and renders into a provided container.
- Keep the existing static exporters; add a new “Export Dynamic Embed” alongside them.

**URL → Constituency**
- Extract slug from last path segment; strip common tails:
  - Pattern: `-(assembly|vidhan-sabha)-(election|polls)(-by)?(-20\d{2})?(-\d+)?$` and trailing numeric ids.
  - Example: `valmiki-nagar-assembly-election-2025-1400072` → `valmiki-nagar`.
- Build a slug map once from consolidated: `slug(constituency_name) → seatNo`.
- Precedence to resolve constituency:
  - `data-constituency` on the embed container, or `?constituency=` in URL if present.
  - Else slug from `window.location.href`.
  - If still no match, show a clear error and instructions to set `data-constituency` or `?constituency=`.

**Code Changes (file: CMS Widget generator.html)**
- Refactor renderer to support custom root
  - Add `renderSeatInto(rootEl, seatNo, data)` and make current `renderSeat(seatNo, data)` call it with `#output` (CMS Widget generator.html:658).
- Add slug + URL helpers
  - `slugifyName(text)` (lowercase, de-accent, hyphenate, drop “(SC)/(ST)”).
  - `extractPageSlug(url)` implementing the regex tails removal.
  - Place near existing helpers (after color/normalize utilities).
- Build seat lookup
  - After `loadAll()` returns, derive `slugToSeatNo` from `consolidated` (CMS Widget generator.html:493).
- Dynamic embed bootstrap
  - `initDynamicEmbed(rootId, opts)`:
    - Resolve `source` (gh/sandbox) from `opts` or `data-source`.
    - Detect constituency using precedence above.
    - Map to `seatNo`; call `loadAll()` and then `renderSeatInto`.
    - Add loading skeleton + error states.
- New exporter for CMS
  - Add button “Export Dynamic Embed” in the controls bar near existing Export (same section as `exportBtn`).
  - Implement `buildDynamicScriptEmbedSnippet(state)` that yields:
    - `<div id="bihar-embed" data-source="gh"></div>`
    - `<style>…scoped styles for #bihar-embed…</style>` using `buildScopedStylesForId('bihar-embed')` (CMS Widget generator.html:906 area).
    - Inline `<script>(function(){ … loader code … })()</script>` that:
      - Computes slug from `window.location.href`.
      - Fetches JSONs via GitHub Pages (or sandbox if `data-source="sandbox"`).
      - Re-implements a minimal renderer or invokes `renderSeatInto` if we package it into the snippet.
- Maintain map behavior
  - Keep the internal map iframe inside the widget as-is (no outer iframe). It already loads `map.html?ac=…`.

**Embed Snippet Shape (inline, CMS-friendly)**
- Container: `<div id="bihar-embed" data-source="gh" data-constituency="valmiki-nagar"></div>` (data-constituency optional).
- Scoped styles: inline `<style>` produced from `buildScopedStylesForId('bihar-embed')`.
- Loader script: inline IIFE that:
  - Gets `constituency` from `data-constituency` or URL.
  - Fetches JSONs (Promise.all with timeout).
  - Builds `slugToSeatNo` and calls the renderer into `#bihar-embed`.

**Error/Resilience**
- Show a small “Loading…” placeholder immediately.
- Timeout fetches (e.g., 10s) with a retry once; then show a friendly error.
- If slug not found: instruct to set `data-constituency` or `?constituency=`.

**Tradeoffs and Defaults**
- Default to inline dynamic script (single snippet) since your CMS accepts current embed code.
- Optionally support an external `embed.js` for a smaller snippet; same API (`data-constituency`, `data-source`). We can add this later if desired.

**Validation**
- Test with real URLs like `…/valmiki-nagar-assembly-election-2025-1400072`.
- Test overrides: `?constituency=valmiki-nagar` and `data-constituency` attribute.
- Verify both sources: GitHub Pages and sandbox; confirm CORS.
