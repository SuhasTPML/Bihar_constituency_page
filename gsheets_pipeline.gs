/**
 * Bihar Elections: Sheets <-> JSON pipeline (mirrors Python tools)
 * - Export parties/results sheets to JSON with a copy-to-clipboard dialog (no Drive writes).
 * - Import parties/results by pasting JSON into a dialog to create new sheets (no Drive reads).
 */

const CONFIG = {
  // If null, uses the active spreadsheet
  SPREADSHEET_ID: null,

  // Sheet names for CSV-uploaded data
  PARTIES_SHEET_NAME: 'parties',
  RESULTS_SHEET_NAME: 'bihar_election_results_consolidated',
  // Default sheet names for pasted JSON imports
  PARTIES_IMPORT_SHEET_NAME: 'Parties (from JSON)',
  RESULTS_IMPORT_SHEET_NAME: 'Results (from JSON)',
};

// Canonical results key order (as per Python scripts)
const RESULTS_PREFERRED_KEYS = [
  'no','constituency_name','slug','district','reserved',
  'lok_sabha_no','lok_sabha',
  // 2010
  'y2010_winner_name','y2010_winner_party','y2010_winner_votes',
  'y2010_runner_name','y2010_runner_party','y2010_runner_votes',
  'y2010_margin',
  // 2015
  'y2015_winner_name','y2015_winner_party','y2015_winner_votes',
  'y2015_runner_name','y2015_runner_party','y2015_runner_votes',
  'y2015_margin',
  // 2020
  'y2020_winner_name','y2020_winner_party','y2020_winner_votes',
  'y2020_runner_name','y2020_runner_party','y2020_runner_votes',
  'y2020_margin',
  // 2025 placeholders
  'y2025_winner_name','y2025_winner_party','y2025_winner_votes',
  'y2025_runner_name','y2025_runner_party','y2025_runner_votes',
  'y2025_margin',
  // current
  'current_mla_name','current_mla_party','current_mla_alliance','current_remarks',
  'diff_party_vs_2020','diff_name_vs_2020',
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Bihar Data')
    .addSubMenu(
      SpreadsheetApp.getUi().createMenu('Export (Copy JSON)')
        .addItem('Parties → JSON (copy)', 'exportPartiesJsonCopy')
        .addItem('Results → JSON (copy)', 'exportResultsJsonCopy')
    )
    .addSubMenu(
      SpreadsheetApp.getUi().createMenu('Import (Paste JSON)')
        .addItem('Paste Parties JSON → Sheet', 'importPartiesJsonPaste')
        .addItem('Paste Results JSON → Sheet', 'importResultsJsonPaste')
    )
    .addToUi();
}

/* ========== Core utilities ========== */

function _getSpreadsheet() {
  return CONFIG.SPREADSHEET_ID
    ? SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID)
    : SpreadsheetApp.getActive();
}

function _getSheetOrThrow(name) {
  const ss = _getSpreadsheet();
  const sh = ss.getSheetByName(name);
  if (!sh) throw new Error('Sheet not found: ' + name);
  return sh;
}

function _sheetToObjects(sheet) {
  const values = sheet.getDataRange().getValues();
  if (!values.length) return [];
  const headers = values[0].map(h => String(h || '').trim());
  const rows = values.slice(1);
  const records = [];
  for (const row of rows) {
    const obj = {};
    let nonEmpty = false;
    for (let i = 0; i < headers.length; i++) {
      const key = headers[i] || '';
      if (!key) continue;
      const val = row[i];
      if (val !== '' && val !== null && val !== undefined) nonEmpty = true;
      obj[key] = val;
    }
    if (nonEmpty) records.push(obj);
  }
  return records;
}

function _showJsonCopyDialog(title, jsonString) {
  const html = HtmlService.createHtmlOutput(
    `<!doctype html>
    <html><head><meta charset="utf-8">
    <style>
      body{font:14px system-ui,Segoe UI,Arial,sans-serif;margin:16px;}
      textarea{width:100%;height:360px;font:12px ui-monospace,Consolas,monospace;}
      .row{display:flex;gap:8px;margin-top:8px}
      button{padding:6px 10px}
    </style></head>
    <body>
      <h3>${title}</h3>
      <textarea id="txt" readonly></textarea>
      <div class="row">
        <button id="copy">Copy to clipboard</button>
        <button id="close">Close</button>
      </div>
      <script>
        const t = document.getElementById('txt');
        t.value = ${JSON.stringify(jsonString)};
        document.getElementById('copy').onclick = async ()=>{
          try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
              await navigator.clipboard.writeText(t.value);
            } else {
              t.select(); document.execCommand('copy');
            }
            alert('Copied to clipboard');
          } catch(e){ alert('Copy failed: ' + e); }
        };
        document.getElementById('close').onclick = ()=> google.script.host.close();
      </script>
    </body></html>`
  ).setWidth(640).setHeight(500);
  SpreadsheetApp.getUi().showModalDialog(html, title);
}

function _showPasteJsonDialog(kind, suggestedSheetName) {
  const title = kind === 'parties' ? 'Paste Parties JSON → Sheet' : 'Paste Results JSON → Sheet';
  const serverFn = kind === 'parties' ? 'importPartiesJsonFromText' : 'importResultsJsonFromText';
  const html = HtmlService.createHtmlOutput(
    `<!doctype html>
    <html><head><meta charset="utf-8">
    <style>
      body{font:14px system-ui,Segoe UI,Arial,sans-serif;margin:16px;}
      label{display:block;margin:6px 0}
      input,textarea{width:100%;box-sizing:border-box}
      textarea{height:320px;font:12px ui-monospace,Consolas,monospace}
      .row{display:flex;gap:8px;margin-top:8px}
      button{padding:6px 10px}
    </style></head>
    <body>
      <h3>${title}</h3>
      <label>Target sheet name <input id="sheet" value="${suggestedSheetName}"></label>
      <label>Paste JSON array below</label>
      <textarea id="txt" placeholder="[ { ... }, { ... } ]"></textarea>
      <div class="row">
        <button id="go">Convert to Sheet</button>
        <button id="cancel">Cancel</button>
      </div>
      <script>
        const go = document.getElementById('go');
        go.onclick = ()=>{
          go.disabled = true; go.textContent = 'Converting...';
          const payload = { text: document.getElementById('txt').value, sheet: document.getElementById('sheet').value };
          google.script.run.withSuccessHandler((msg)=>{ alert(msg||'Done'); google.script.host.close(); })
            .withFailureHandler((e)=>{ alert('Error: ' + e.message); go.disabled=false; go.textContent='Convert to Sheet'; })
            ['${serverFn}'](payload.text, payload.sheet);
        };
        document.getElementById('cancel').onclick = ()=> google.script.host.close();
      </script>
    </body></html>`
  ).setWidth(640).setHeight(520);
  SpreadsheetApp.getUi().showModalDialog(html, title);
}

function _reorderRecord(record, preferredOrder) {
  const out = {};
  preferredOrder.forEach(k => { if (Object.prototype.hasOwnProperty.call(record, k)) out[k] = record[k]; });
  Object.keys(record).forEach(k => { if (!Object.prototype.hasOwnProperty.call(out, k)) out[k] = record[k]; });
  return out;
}

function _ensureSheet(name) {
  const ss = _getSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  else sh.clearContents();
  return sh;
}

function _writeTableToSheet(sheet, header, rows) {
  if (!header || !header.length) return;
  const data = [header, ...rows];
  sheet.getRange(1, 1, data.length, header.length).setValues(
    data.map(r => header.map((_, i) => r[i] == null ? '' : r[i]))
  );
}

/* ========== Export: Sheets → JSON (copy dialog) ========== */

function exportPartiesJsonCopy() {
  const sheet = _getSheetOrThrow(CONFIG.PARTIES_SHEET_NAME);
  const rows = _sheetToObjects(sheet);

  // Map rows to schema with per-year alliances
  const out = rows.map(r => {
    const a = (yr) => String(
      r['alliance_' + yr] || r['alliance_2020'] || r['alliance'] || ''
    ).trim();
    return {
      code: String(r.code || '').trim(),
      name: String(r.name || '').trim(),
      color: String(r.color || '').trim(),
      alliances: {
        '2010': a(2010),
        '2015': a(2015),
        '2020': a(2020),
        '2025': a(2025),
      },
    };
  });

  const json = JSON.stringify(out, null, 2);
  _showJsonCopyDialog('Parties JSON', json);
}

function exportResultsJsonCopy() {
  const sheet = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
  const rows = _sheetToObjects(sheet);

  // Keep all fields; reorder to canonical order for readability
  const out = rows.map(r => _reorderRecord(r, RESULTS_PREFERRED_KEYS));

  const json = JSON.stringify(out, null, 2);
  _showJsonCopyDialog('Results JSON', json);
}

/* ========== Import: JSON (paste) → Sheet ========== */

function importPartiesJsonPaste() {
  _showPasteJsonDialog('parties', CONFIG.PARTIES_IMPORT_SHEET_NAME);
}

function importResultsJsonPaste() {
  _showPasteJsonDialog('results', CONFIG.RESULTS_IMPORT_SHEET_NAME);
}

function importPartiesJsonFromText(jsonText, newSheetName) {
  let data;
  try {
    data = JSON.parse(String(jsonText || ''));
  } catch (e) {
    throw new Error('Invalid JSON: ' + e);
  }
  if (!Array.isArray(data)) throw new Error('Expected a JSON array at top level');

  // Detect per-year alliances map
  const hasPerYear = data.some(r => r && typeof r.alliances === 'object');

  let header, rows;
  if (hasPerYear) {
    header = ['code','name','color','alliance_2010','alliance_2015','alliance_2020','alliance_2025'];
    rows = data.map(r => {
      const alliances = r.alliances || {};
      const val = (yr) =>
        alliances[String(yr)] || alliances[yr] || r['alliance_' + yr] || r['alliance'] || '';
      return [
        r.code || '', r.name || '', r.color || '',
        val(2010), val(2015), val(2020), val(2025),
      ];
    });
  } else {
    header = ['code','name','color','alliance'];
    rows = data.map(r => [r.code || '', r.name || '', r.color || '', r.alliance || r.alliance_2020 || '']);
  }

  const sh = _ensureSheet(newSheetName || CONFIG.PARTIES_IMPORT_SHEET_NAME);
  _writeTableToSheet(sh, header, rows);
  return 'Imported Parties JSON into sheet: ' + (newSheetName || CONFIG.PARTIES_IMPORT_SHEET_NAME);
}

function importResultsJsonFromText(jsonText, newSheetName) {
  let data;
  try {
    data = JSON.parse(String(jsonText || ''));
  } catch (e) {
    throw new Error('Invalid JSON: ' + e);
  }
  if (!Array.isArray(data)) throw new Error('Expected a JSON array at top level');
  const sh = _ensureSheet(newSheetName || CONFIG.RESULTS_IMPORT_SHEET_NAME);
  if (!data.length) {
    _writeTableToSheet(sh, [], []);
    return 'No records found; created empty sheet';
  }

  // Build header: start with preferred keys, then add any extras seen
  const seen = {};
  const header = [];
  RESULTS_PREFERRED_KEYS.forEach(k => { seen[k] = true; header.push(k); });
  data.forEach(r => {
    Object.keys(r || {}).forEach(k => {
      if (!seen[k]) { seen[k] = true; header.push(k); }
    });
  });

  const rows = data.map(r => header.map(k => (r && r[k] != null) ? r[k] : ''));
  _writeTableToSheet(sh, header, rows);
  return 'Imported Results JSON into sheet: ' + (newSheetName || CONFIG.RESULTS_IMPORT_SHEET_NAME);
}

// Note: Web endpoint removed to keep interactions clipboard/paste-only.
