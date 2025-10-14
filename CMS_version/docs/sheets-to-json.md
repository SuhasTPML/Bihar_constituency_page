# Google Sheets → JSON for Bihar Constituency Map/Viewer

This note documents two practical ways to drive your site’s JSON from a Google Sheet while keeping the viewer and map fast and robust.

- Option A (quickest): Serve JSON directly from Google Apps Script (a Web App) backed by your sheet.
- Option B (recommended for production): Use Apps Script to publish static JSON to your domain (e.g., this GitHub Pages repo) so the site loads fast, cacheable assets.

The examples below assume two tabs in a single Google Sheet:

- `parties` — source for `parties.json`
- `results` — source for `bihar_election_results_consolidated.json`

Both tabs must have a header row (first row) followed by data rows.

---

## Data shapes used on the site

### parties.json (per-year alliances)

```jsonc
{
  "code": "INC",
  "name": "Indian National Congress",
  "color": "#3399ff",
  "alliances": {
    "2010": "UPA",
    "2015": "MGB",
    "2020": "MGB",
    "2025": "MGB"
  }
}
```

The sheet can provide columns like: `code, name, color, alliance_2010, alliance_2015, alliance_2020, alliance_2025`.

### bihar_election_results_consolidated.json

Array of 243 seat records. Keep your current headers (no, constituency_name, slug, district, reserved, lok_sabha_no, lok_sabha, y2010_*, y2015_*, y2020_*, y2025_*, current_mla_*, diff_*). The site reads these as-is.

---

## Option A: Serve JSON directly from Apps Script (Web App)

Pros: zero extra infrastructure; editors’ changes go live immediately. Cons: higher and more variable latency; not edge-cached; quotas apply.

1) In your Google Sheet, open `Extensions → Apps Script` and paste the code below.

```js
function sheetToObjects_(sheetName) {
  const sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  if (!sh) throw new Error('Missing sheet: ' + sheetName);
  const values = sh.getDataRange().getValues();
  if (!values.length) return [];
  const header = values[0].map(h => String(h).trim());
  return values.slice(1)
    .filter(r => r.some(c => String(c).trim() !== ''))
    .map(r => Object.fromEntries(header.map((h, i) => [h, r[i] == null ? '' : String(r[i])])));
}

function getPartiesJson_() {
  const rows = sheetToObjects_('parties');
  return rows.map(r => {
    const alliances = {
      '2010': (r.alliance_2010 || r.alliance_2020 || r.alliance || '').trim(),
      '2015': (r.alliance_2015 || r.alliance_2020 || r.alliance || '').trim(),
      '2020': (r.alliance_2020 || r.alliance || '').trim(),
      '2025': (r.alliance_2025 || r.alliance_2020 || r.alliance || '').trim(),
    };
    return {
      code: (r.code || '').trim(),
      name: (r.name || '').trim(),
      color: (r.color || '').trim(),
      alliances,
    };
  });
}

function getResultsJson_() { return sheetToObjects_('results'); }

// GET ?file=parties | results
function doGet(e) {
  try {
    const file = (e && e.parameter && e.parameter.file) || 'results';
    const payload = (file === 'parties') ? getPartiesJson_() : getResultsJson_();
    return ContentService
      .createTextOutput(JSON.stringify(payload, null, 2))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: true, message: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Menu to save JSON to Drive (optional)
function exportJsonToDrive_() {
  const folder = DriveApp.getRootFolder();
  const files = [
    { name: 'parties.json', data: getPartiesJson_() },
    { name: 'bihar_election_results_consolidated.json', data: getResultsJson_() },
  ];
  files.forEach(f => {
    const it = folder.getFilesByName(f.name);
    while (it.hasNext()) it.next().setTrashed(true);
    folder.createFile(f.name, JSON.stringify(f.data, null, 2), MimeType.JSON);
  });
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('JSON Export')
    .addItem('Export JSON to Drive', 'exportJsonToDrive_')
    .addToUi();
}
```

2) Deploy as a Web App (`Deploy → New deployment → Web app`).
   - Execute as: Me; Who has access: Anyone with the link.

3) Use the URLs in the viewer/map (or for testing):
   - `…/exec?file=parties`
   - `…/exec?file=results`

Tip: For cache busting while testing, add `?v=<timestamp>` or configure your fetch with `{ cache: 'no-store' }`.

Latency & quotas: Apps Script is convenient but can be 0.5–2s on cold starts and has burst limits; consider Option B for production.

---

## Option B: Publish static JSON to your domain (recommended)

Editors keep using the sheet; a script publishes JSON to this repo (GitHub Pages) so your site serves fast, cacheable files.

### a) Store a GitHub token in Script Properties

In Apps Script: `Project Settings → Script properties` add:

- `GH_TOKEN` — a GitHub personal access token with `repo` scope (fine-grained minimal content write scope recommended).
- `GH_REPO` — e.g., `SuhasTPML/Bihar_constituency_page`.
- `GH_BRANCH` — e.g., `main`.

### b) Apps Script publisher

```js
function _ghProps_() {
  const p = PropertiesService.getScriptProperties();
  return {
    token: p.getProperty('GH_TOKEN'),
    repo: p.getProperty('GH_REPO'),
    branch: p.getProperty('GH_BRANCH') || 'main'
  };
}

function _ghApi_(path, method, body) {
  const { token, repo } = _ghProps_();
  const url = `https://api.github.com/repos/${repo}/${path}`;
  const opts = {
    method,
    muteHttpExceptions: true,
    contentType: 'application/json',
    headers: { Authorization: `token ${token}`, 'User-Agent': 'apps-script' },
    payload: body ? JSON.stringify(body) : null
  };
  const res = UrlFetchApp.fetch(url, opts);
  if (res.getResponseCode() >= 300) throw new Error(res.getContentText());
  return JSON.parse(res.getContentText());
}

function _ghGetSha_(path) {
  try { return _ghApi_(`contents/${path}`, 'get', null).sha || null; }
  catch (e) { return null; }
}

function _ghPutContent_(path, json) {
  const { branch } = _ghProps_();
  const sha = _ghGetSha_(path);
  const content = Utilities.base64Encode(JSON.stringify(json, null, 2));
  return _ghApi_(`contents/${path}`, 'put', {
    message: `chore: publish ${path} from Sheets`,
    content,
    branch,
    sha
  });
}

function publishToGithub() {
  const parties = getPartiesJson_();
  const results = getResultsJson_();
  _ghPutContent_('parties.json', parties);
  _ghPutContent_('bihar_election_results_consolidated.json', results);
}
```

Trigger: add a time-driven trigger (e.g., every 5 minutes or on a schedule) for `publishToGithub`, or bind it to a custom menu.

Your site then reads static JSON from:

- `https://suhastpml.github.io/Bihar_constituency_page/parties.json`
- `https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json`

You can add a version query `?v=<ISO timestamp>` when you publish to bust caches.

---

## Viewer/Map wiring notes

- The viewer already supports toggling between sandbox and GH Pages JSON; map loads from this repo’s GH Pages with local fallback.
- Map supports 2025 on/off via `enable2025` URL param; viewer now passes it based on the “Results announced” toggle.
- If you later point the viewer to the Apps Script Web App endpoints, ensure CORS/no-cors issues are addressed (Apps Script JSON endpoints typically work with cross-origin GETs).

### Quick wiring in this repo

- Viewer (`index.html`) expects JSON at:
  - Parties: `https://suhastpml.github.io/Bihar_constituency_page/parties.json`
  - Results: `https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json`
  (or local equivalents when the “Use GitHub Pages data” toggle is on.)

- Map (`map.html`) expects the same endpoints and reads `enable2025=1/0` in the iframe URL to default to 2025 or 2020 modes.

To embed the viewer with 2025 enabled by default:

```
https://suhastpml.github.io/Bihar_constituency_page/index.html?source=gh
```

Then check “Results announced” (the viewer propagates `enable2025=1` to the map). You can also directly use:

```
https://suhastpml.github.io/Bihar_constituency_page/map.html?ac=021&enable2025=1
```

---

## Trade-offs

- Apps Script Web App: easiest live JSON; expect higher, more variable latency and quota limits.
- Static publish to GH Pages: near-instant loads with CDN caching; requires a simple publish job on sheet updates.

---

## Troubleshooting

- Missing party color/alliance: ensure `parties` tab has `code, name, color` and alliance columns for 2010/2015/2020/2025.
- Seat not coloring in 2025 Party: check `y2025_winner_party` in results row.
- Cached JSON: add `?v=<Date.now()>` while testing; set fetch to `{ cache: 'no-store' }`.
- API errors when publishing: verify PAT scope, repo path (owner/name), and that the branch exists.
