/**
 * Bihar Elections: Sheets <-> JSON pipeline (mirrors Python tools)
 * - Export parties/results sheets to JSON on Drive (schema-aware).
 * - Import parties/results JSON files to new sheets (schema-aware).
 */

const CONFIG = {
  // If null, uses the active spreadsheet
  SPREADSHEET_ID: null,

  // Optional target folder for exported JSON files (null -> My Drive root)
  OUTPUT_FOLDER_ID: null,

  // Sheet names for CSV-uploaded data
  PARTIES_SHEET_NAME: 'parties',
  RESULTS_SHEET_NAME: 'bihar_election_results_consolidated',

  // Exported filenames
  PARTIES_JSON_NAME: 'parties.json',
  RESULTS_JSON_NAME: 'bihar_election_results_consolidated.json',
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
      SpreadsheetApp.getUi().createMenu('Export (Sheets → JSON)')
        .addItem('Export Parties JSON', 'exportPartiesJson')
        .addItem('Export Results JSON', 'exportResultsJson')
    )
    .addSubMenu(
      SpreadsheetApp.getUi().createMenu('Import (JSON → Sheet)')
        .addItem('Import Parties JSON to Sheet', 'importPartiesJsonToSheetPrompt')
        .addItem('Import Results JSON to Sheet', 'importResultsJsonToSheetPrompt')
    )
    .addToUi();
}

/* ========== Core utilities ========== */

function _getSpreadsheet() {
  return CONFIG.SPREADSHEET_ID
    ? SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID)
    : SpreadsheetApp.getActive();
}

function _getOutputFolder() {
  if (!CONFIG.OUTPUT_FOLDER_ID) return null;
  try {
    return DriveApp.getFolderById(CONFIG.OUTPUT_FOLDER_ID);
  } catch (e) {
    throw new Error('Invalid OUTPUT_FOLDER_ID: ' + e);
  }
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

function _writeJsonToDrive(records, filename) {
  const json = JSON.stringify(records, null, 2);
  const blob = Utilities.newBlob(json, 'application/json', filename);
  const folder = _getOutputFolder();
  const file = folder ? folder.createFile(blob) : DriveApp.createFile(blob);
  return file.getUrl();
}

function _readJsonFromDriveFileId(fileId) {
  const file = DriveApp.getFileById(fileId);
  const text = file.getBlob().getDataAsString('utf-8');
  const data = JSON.parse(text);
  if (!Array.isArray(data)) {
    throw new Error('Expected top-level array in JSON file: ' + file.getName());
  }
  return data;
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

/* ========== Export: Sheets → JSON ========== */

function exportPartiesJson() {
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

  const url = _writeJsonToDrive(out, CONFIG.PARTIES_JSON_NAME);
  SpreadsheetApp.getUi().alert('Exported parties.json\n' + url);
  return url;
}

function exportResultsJson() {
  const sheet = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
  const rows = _sheetToObjects(sheet);

  // Keep all fields; reorder to canonical order for readability
  const out = rows.map(r => _reorderRecord(r, RESULTS_PREFERRED_KEYS));

  const url = _writeJsonToDrive(out, CONFIG.RESULTS_JSON_NAME);
  SpreadsheetApp.getUi().alert('Exported results JSON\n' + url);
  return url;
}

/* ========== Import: JSON → Sheet ========== */

function importPartiesJsonToSheetPrompt() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.prompt('Import Parties JSON', 'Enter Drive File ID of parties.json:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  const fileId = resp.getResponseText().trim();
  importPartiesJsonToSheet(fileId, 'Parties (from JSON)');
}

function importResultsJsonToSheetPrompt() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.prompt('Import Results JSON', 'Enter Drive File ID of bihar_election_results_consolidated.json:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  const fileId = resp.getResponseText().trim();
  importResultsJsonToSheet(fileId, 'Results (from JSON)');
}

function importPartiesJsonToSheet(fileId, newSheetName) {
  const data = _readJsonFromDriveFileId(fileId);

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

  const sh = _ensureSheet(newSheetName);
  _writeTableToSheet(sh, header, rows);
  SpreadsheetApp.getUi().alert('Imported Parties JSON into sheet: ' + newSheetName);
}

function importResultsJsonToSheet(fileId, newSheetName) {
  const data = _readJsonFromDriveFileId(fileId);
  const sh = _ensureSheet(newSheetName);
  if (!data.length) {
    _writeTableToSheet(sh, [], []);
    return;
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
  SpreadsheetApp.getUi().alert('Imported Results JSON into sheet: ' + newSheetName);
}

/* ========== Optional web endpoints (serve JSON from this sheet) ========== */
/* Publish as web app to serve JSON: doGet?file=parties|results */
function doGet(e) {
  const p = (e && e.parameter && e.parameter.file || '').toLowerCase();
  let data = [];
  if (p === 'parties') {
    const sheet = _getSheetOrThrow(CONFIG.PARTIES_SHEET_NAME);
    const rows = _sheetToObjects(sheet);
    data = rows.map(r => ({
      code: String(r.code || '').trim(),
      name: String(r.name || '').trim(),
      color: String(r.color || '').trim(),
      alliances: {
        '2010': String(r.alliance_2010 || r.alliance_2020 || r.alliance || '').trim(),
        '2015': String(r.alliance_2015 || r.alliance_2020 || r.alliance || '').trim(),
        '2020': String(r.alliance_2020 || r.alliance || '').trim(),
        '2025': String(r.alliance_2025 || r.alliance_2020 || r.alliance || '').trim(),
      },
    }));
  } else if (p === 'results') {
    const sheet = _getSheetOrThrow(CONFIG.RESULTS_SHEET_NAME);
    const rows = _sheetToObjects(sheet);
    data = rows.map(r => _reorderRecord(r, RESULTS_PREFERRED_KEYS));
  } else {
    return ContentService.createTextOutput('Specify ?file=parties or ?file=results')
      .setMimeType(ContentService.MimeType.TEXT);
  }
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

