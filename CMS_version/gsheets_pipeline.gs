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
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Bihar Data')
    .addSubMenu(
      ui.createMenu('Export (Copy JSON)')
        .addItem('Parties → JSON (copy)', 'exportPartiesJsonCopy')
        .addItem('Results → JSON (copy)', 'exportResultsJsonCopy')
    )
    .addSubMenu(
      ui.createMenu('Import (Paste JSON)')
        .addItem('Paste Parties JSON → Sheet', 'importPartiesJsonPaste')
        .addItem('Paste Results JSON → Sheet', 'importResultsJsonPaste')
    )
    .addSubMenu(
      ui.createMenu('2025 Placeholders')
        .addItem('Seed 2025 from 2020 winners', 'seed2025From2020')
        .addItem('Clear 2025 placeholders (results)', 'clear2025Placeholders')
        .addSeparator()
        .addItem('Ensure alliance_2025 (Parties)', 'ensureAlliance2025Column')
        .addItem('Add validations for 2025 party fields', 'add2025Validations')
        .addSeparator()
        .addItem('Set 2025 fields (bulk input)…', 'openSet2025BulkDialog')
    )
    .addToUi();
}

/* ========== 2025 placeholder utilities (CMS copy) ========== */

function _getHeader_(sheet) {
  const values = sheet.getDataRange().getValues();
  return (values && values.length) ? values[0].map(h => String(h || '').trim()) : [];
}

function _getLastRow_(sheet, col) {
  const range = sheet.getRange(2, col, Math.max(1, sheet.getMaxRows() - 1), 1);
  const vals = range.getValues();
  for (let i = vals.length - 1; i >= 0; i--) {
    if (String(vals[i][0] || '').trim() !== '') return i + 2;
  }
  return 2;
}

function seed2025From2020() {
  const sh = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
  const values = sh.getDataRange().getValues();
  if (!values.length) return 'No data';
  const header = values[0].map(h => String(h || '').trim());
  const rows = values.slice(1);
  const c = (n) => header.indexOf(n);

  const i20n = c('y2020_winner_name');
  const i20p = c('y2020_winner_party');
  const i25n = c('y2025_winner_name');
  const i25p = c('y2025_winner_party');
  const i25wv = c('y2025_winner_votes');
  const i25rn = c('y2025_runner_name');
  const i25rp = c('y2025_runner_party');
  const i25rv = c('y2025_runner_votes');
  const i25m  = c('y2025_margin');
  const required = [i20n,i20p,i25n,i25p,i25wv,i25rn,i25rp,i25rv,i25m].every(i => i >= 0);
  if (!required) throw new Error('Required 2020/2025 columns not found.');

  let changed = 0;
  for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    const name2020 = row[i20n];
    const party2020 = row[i20p];
    if (String(row[i25n]||'').trim() === '' && String(row[i25p]||'').trim() === '') {
      row[i25n] = name2020 || '';
      row[i25p] = party2020 || '';
      changed++;
    }
    row[i25wv] = '';
    row[i25rn] = '';
    row[i25rp] = '';
    row[i25rv] = '';
    row[i25m]  = '';
  }
  sh.getRange(2, 1, rows.length, header.length).setValues(rows);
  SpreadsheetApp.getUi().alert(`Seeded ${changed} rows with 2025 placeholders from 2020 winners.`);
}

function clear2025Placeholders() {
  const sh = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
  const values = sh.getDataRange().getValues();
  if (!values.length) return 'No data';
  const header = values[0].map(h => String(h || '').trim());
  const rows = values.slice(1);
  const cols = [
    'y2025_winner_name','y2025_winner_party','y2025_winner_votes',
    'y2025_runner_name','y2025_runner_party','y2025_runner_votes','y2025_margin'
  ].map(n => header.indexOf(n));
  if (cols.some(i => i < 0)) throw new Error('Missing 2025 result columns.');
  for (let r = 0; r < rows.length; r++) {
    for (const i of cols) rows[r][i] = '';
  }
  sh.getRange(2, 1, rows.length, header.length).setValues(rows);
  SpreadsheetApp.getUi().alert('Cleared 2025 placeholder fields.');
}

function ensureAlliance2025Column() {
  const sh = _getSheetOrThrow(CONFIG.PARTIES_SHEET_NAME);
  const values = sh.getDataRange().getValues();
  if (!values.length) return 'No data';
  let header = values[0].map(h => String(h || '').trim());
  const colA20 = header.indexOf('alliance_2020');
  let colA25 = header.indexOf('alliance_2025');

  if (colA25 < 0) {
    sh.insertColumnAfter(header.length);
    colA25 = header.length;
    sh.getRange(1, colA25 + 1).setValue('alliance_2025');
    header = _getHeader_(sh);
  }
  const lastRow = _getLastRow_(sh, 1);
  const a20Range = (colA20 >= 0) ? sh.getRange(2, colA20 + 1, Math.max(0, lastRow - 1), 1) : null;
  const a25Range = sh.getRange(2, colA25 + 1, Math.max(0, lastRow - 1), 1);
  const a20 = a20Range ? a20Range.getValues() : [];
  const a25 = a25Range.getValues();
  for (let i = 0; i < a25.length; i++) {
    if (String(a25[i][0]||'').trim() === '') {
      a25[i][0] = (a20[i] && a20[i][0]) ? a20[i][0] : '';
    }
  }
  a25Range.setValues(a25);
  SpreadsheetApp.getUi().alert('Ensured alliance_2025 exists and backfilled from alliance_2020 (where empty).');
}

function add2025Validations() {
  const parties = _getSheetOrThrow(CONFIG.PARTIES_SHEET_NAME);
  const results = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);

  const pHeader = _getHeader_(parties);
  const codeIdx = pHeader.indexOf('code');
  if (codeIdx < 0) throw new Error('Parties sheet is missing a "code" column.');
  const pLast = _getLastRow_(parties, codeIdx + 1);
  const codesRange = parties.getRange(2, codeIdx + 1, Math.max(0, pLast - 1), 1);

  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInRange(codesRange, true)
    .setAllowInvalid(false)
    .build();

  const rHeader = _getHeader_(results);
  const cols = ['y2025_winner_party','y2025_runner_party'].map(n => rHeader.indexOf(n));
  if (cols.some(i => i < 0)) throw new Error('Missing results columns for 2025 party fields.');
  const rLast = _getLastRow_(results, 1);
  cols.forEach((idx) => {
    const rng = results.getRange(2, idx + 1, Math.max(0, rLast - 1), 1);
    rng.setDataValidation(rule);
  });

  const cfBuilder = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('')
    .setBackground('#fde68a')
    .setRanges(cols.map(idx => results.getRange(2, idx + 1, Math.max(0, rLast - 1), 1)));
  const existing = results.getConditionalFormatRules();
  existing.push(cfBuilder.build());
  results.setConditionalFormatRules(existing);

  SpreadsheetApp.getUi().alert('Added data validation for 2025 party fields and conditional formatting for blanks.');
}

function openSet2025BulkDialog(){
  const html = HtmlService.createHtmlOutput(
    `<!doctype html>
    <html><head><meta charset="utf-8">
    <style>
      body{font:14px system-ui,Segoe UI,Arial,sans-serif;margin:16px;}
      fieldset{border:1px solid #ddd;border-radius:8px;padding:12px;margin:0 0 12px}
      label{display:block;margin:6px 0}
      input[type=text],input[type=number]{width:100%;padding:8px;border:1px solid #ddd;border-radius:6px}
      .row{display:flex;gap:10px}
      .col{flex:1}
      .actions{display:flex;gap:8px;margin-top:12px}
      button{padding:8px 12px}
      small{color:#666}
    </style></head>
    <body>
      <h3>Set 2025 Fields (Bulk)</h3>
      <p>Enter values to apply to all rows. Leave any field blank to skip updating that column. Choose whether to overwrite or only fill blanks.</p>

      <fieldset>
        <legend>Results – 2025</legend>
        <div class="row">
          <div class="col"><label>Winner name <input id="y2025_winner_name" type="text"></label></div>
          <div class="col"><label>Winner party <input id="y2025_winner_party" type="text" placeholder="e.g., JD(U)"></label></div>
          <div class="col"><label>Winner votes <input id="y2025_winner_votes" type="number" min="0" step="1"></label></div>
        </div>
        <div class="row">
          <div class="col"><label>Runner name <input id="y2025_runner_name" type="text"></label></div>
          <div class="col"><label>Runner party <input id="y2025_runner_party" type="text"></label></div>
          <div class="col"><label>Runner votes <input id="y2025_runner_votes" type="number" min="0" step="1"></label></div>
        </div>
        <label>Margin <input id="y2025_margin" type="number" min="0" step="1"></label>
        <label><input id="overwrite_results" type="checkbox"> Overwrite existing values (unchecked = fill blanks only)</label>
      </fieldset>

      <fieldset>
        <legend>Parties – alliance_2025</legend>
        <label>Alliance 2025 (set for all parties) <input id="alliance_2025" type="text" placeholder="e.g., NDA / MGB / OTH"></label>
        <label><input id="overwrite_alliance" type="checkbox"> Overwrite existing values (unchecked = fill blanks only)</label>
        <small>Leave blank to skip updating Parties sheet.</small>
      </fieldset>

      <div class="actions">
        <button id="apply">Apply</button>
        <button id="close">Close</button>
      </div>

      <script>
        document.getElementById('close').onclick = () => google.script.host.close();
        document.getElementById('apply').onclick = () => {
          const payload = {
            results: {
              y2025_winner_name: document.getElementById('y2025_winner_name').value.trim(),
              y2025_winner_party: document.getElementById('y2025_winner_party').value.trim(),
              y2025_winner_votes: document.getElementById('y2025_winner_votes').value.trim(),
              y2025_runner_name: document.getElementById('y2025_runner_name').value.trim(),
              y2025_runner_party: document.getElementById('y2025_runner_party').value.trim(),
              y2025_runner_votes: document.getElementById('y2025_runner_votes').value.trim(),
              y2025_margin: document.getElementById('y2025_margin').value.trim(),
              overwrite: document.getElementById('overwrite_results').checked
            },
            parties: {
              alliance_2025: document.getElementById('alliance_2025').value.trim(),
              overwrite: document.getElementById('overwrite_alliance').checked
            }
          };
          google.script.run.withSuccessHandler((msg)=>{ alert(msg||'Done'); google.script.host.close(); })
            .withFailureHandler((e)=>{ alert('Error: ' + (e.message||e)); })
            .set2025FieldsBulk(payload);
        };
      </script>
    </body></html>`
  ).setWidth(760).setHeight(640);
  SpreadsheetApp.getUi().showModalDialog(html, 'Set 2025 Fields (Bulk)');
}

function set2025FieldsBulk(payload){
  if (!payload || !payload.results) throw new Error('Invalid payload');
  const rSh = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
  const rVals = rSh.getDataRange().getValues();
  if (rVals.length) {
    const header = rVals[0].map(h => String(h||'').trim());
    const rows = rVals.slice(1);
    const fields = ['y2025_winner_name','y2025_winner_party','y2025_winner_votes','y2025_runner_name','y2025_runner_party','y2025_runner_votes','y2025_margin'];
    const idx = Object.fromEntries(fields.map(f => [f, header.indexOf(f)]));
    if (Object.values(idx).some(i => i < 0)) throw new Error('Missing one or more 2025 result columns');
    const overwrite = !!payload.results.overwrite;
    rows.forEach((row) => {
      fields.forEach((f) => {
        const v = (payload.results[f] ?? '').toString();
        if (v === '') return;
        const i = idx[f];
        if (i < 0) return;
        const cur = String(row[i] || '').trim();
        if (overwrite || cur === '') {
          if (f.endsWith('_votes') || f === 'y2025_margin') {
            const n = Number(v.replace(/[,\s]/g, ''));
            row[i] = Number.isFinite(n) ? n : v;
          } else {
            row[i] = v;
          }
        }
      });
    });
    rSh.getRange(2, 1, rows.length, header.length).setValues(rows);
  }

  if (payload.parties && typeof payload.parties.alliance_2025 === 'string' && payload.parties.alliance_2025.trim() !== '') {
    const pSh = _getSheetOrThrow(CONFIG.PARTIES_SHEET_NAME);
    const pVals = pSh.getDataRange().getValues();
    if (pVals.length) {
      let header = pVals[0].map(h => String(h||'').trim());
      let a25 = header.indexOf('alliance_2025');
      if (a25 < 0) {
        pSh.insertColumnAfter(header.length);
        a25 = header.length;
        pSh.getRange(1, a25 + 1).setValue('alliance_2025');
        header = _getHeader_(pSh);
      }
      const overwriteA = !!(payload.parties.overwrite);
      const rows = pVals.slice(1);
      rows.forEach((row) => {
        const cur = String(row[a25] || '').trim();
        if (overwriteA || cur === '') row[a25] = payload.parties.alliance_2025;
      });
      pSh.getRange(2, 1, rows.length, header.length).setValues(rows);
    }
  }
  return 'Applied bulk updates to 2025 fields.';
}

/* ========== Core utilities ========== */

function _sanitizeText(value) {
  if (value == null) return '';
  let s = String(value);
  try { s = s.normalize('NFC'); } catch (e) {}
  // Common UTF-8 -> ISO-8859-1 mojibake sequences mapped back
  const replacements = [
    ['Ã¢â‚¬â€œ', '–'], // en dash
    ['Ã¢â‚¬â€�', '—'], // em dash
    ['Ã¢â‚¬Ëœ', '‘'],
    ['Ã¢â‚¬â„¢', '’'],
    ['Ã¢â‚¬Å“', '“'],
    ['Ã¢â‚¬Â�', '”'],
    ['Ã¢â‚¬Â¦', '…'],
    ['Ã‚Â', ''],     // stray non-breaking space marker
  ];
  for (const [bad, good] of replacements) {
    if (s.indexOf(bad) !== -1) s = s.split(bad).join(good);
  }
  // Optional: collapse other non-printable chars
  s = s.replace(/[\u0000-\u001F\u007F]/g, '');
  return s;
}

function _sanitizeRecordStrings(rec) {
  const out = {};
  Object.keys(rec || {}).forEach(k => {
    const v = rec[k];
    out[k] = (typeof v === 'string') ? _sanitizeText(v) : v;
  });
  return out;
}

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
      code: _sanitizeText(String(r.code || '').trim()),
      name: _sanitizeText(String(r.name || '').trim()),
      color: _sanitizeText(String(r.color || '').trim()),
      alliances: {
        '2010': _sanitizeText(a(2010)),
        '2015': _sanitizeText(a(2015)),
        '2020': _sanitizeText(a(2020)),
        '2025': _sanitizeText(a(2025)),
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
  const out = rows
    .map(r => _sanitizeRecordStrings(r))
    .map(r => _reorderRecord(r, RESULTS_PREFERRED_KEYS));

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
        _sanitizeText(alliances[String(yr)] || alliances[yr] || r['alliance_' + yr] || r['alliance'] || '');
      return [
        _sanitizeText(r.code || ''), _sanitizeText(r.name || ''), _sanitizeText(r.color || ''),
        val(2010), val(2015), val(2020), val(2025),
      ];
    });
  } else {
    header = ['code','name','color','alliance'];
    rows = data.map(r => [
      _sanitizeText(r.code || ''), _sanitizeText(r.name || ''), _sanitizeText(r.color || ''),
      _sanitizeText(r.alliance || r.alliance_2020 || '')
    ]);
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

  const rows = data.map(r => header.map(k => {
    const v = (r && r[k] != null) ? r[k] : '';
    return (typeof v === 'string') ? _sanitizeText(v) : v;
  }));
  _writeTableToSheet(sh, header, rows);
  return 'Imported Results JSON into sheet: ' + (newSheetName || CONFIG.RESULTS_IMPORT_SHEET_NAME);
}

// Note: Web endpoint removed to keep interactions clipboard/paste-only.
