#!/usr/bin/env python3
import sys
import json
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_indexed_by_no(path: Path):
    idx = {}
    if not path.exists():
        return idx
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                no = int(row.get("no", "").strip())
            except Exception:
                continue
            idx[no] = row
    return idx


def sanitize_int(val):
    if val is None:
        return None
    s = str(val).strip().replace(",", "")
    if s == "" or s == "None":
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except Exception:
            return None


def sanitize_float(val):
    if val is None:
        return None
    s = str(val).strip().replace("%", "")
    if s == "" or s == "None":
        return None
    try:
        return float(s)
    except Exception:
        return None


def normalize_party(code: str) -> str:
    if not code:
        return code
    mapping = {
        "JDU": "JD(U)",
        "JD(U)": "JD(U)",
        "CPM": "CPI(M)",
        "HAM": "HAM(S)",
        "Ind": "IND",
        "IND": "IND",
        "JD(U) ": "JD(U)",
    }
    return mapping.get(code, code)


def find_result_for_no(results_by_district: dict, seat_no: int):
    # results_by_district is a dict of district -> [records]
    key = str(seat_no)
    for district, arr in results_by_district.items():
        for rec in arr:
            if str(rec.get("#")) == key:
                return rec
    return None


def main(argv):
    if len(argv) >= 2:
        try:
            seat_no = int(argv[1])
        except ValueError:
            print("Usage: python scripts/constituency_info.py <constituency_no>")
            return 2
    else:
        try:
            seat_no = int(input("Enter constituency number (1-243): ").strip())
        except Exception:
            print("Invalid number")
            return 2

    # Load base data
    const_path = ROOT / "bihar_constituencies.json"
    parties_path = ROOT / "parties.json"
    mla_json = ROOT / "current_mla.json"
    electors_csv = ROOT / "electors_2024.csv"
    r2020_path = ROOT / "2020_results.json"
    r2015_path = ROOT / "2015_results.json"
    r2010_path = ROOT / "2010_results.json"

    constituencies = load_json(const_path) if const_path.exists() else {}
    parties = load_json(parties_path) if parties_path.exists() else []
    parties_idx = {p.get("code"): p for p in parties}

    # Build MLA index from district-keyed JSON { District: [{"No.", "Name", "Party", "Alliance", "Remarks"}, ...] }
    mla_idx = {}
    if mla_json.exists():
        mla_data = load_json(mla_json)
        if isinstance(mla_data, dict):
            for district, rows in mla_data.items():
                if not isinstance(rows, list):
                    continue
                for row in rows:
                    try:
                        no = int(str(row.get("No.", "").strip()))
                    except Exception:
                        continue
                    mla_idx[no] = {
                        "mla": row.get("Name"),
                        "party": row.get("Party"),
                        "alliance": row.get("Alliance"),
                        "note": (row.get("Remarks") or None),
                    }
    elect_idx = load_csv_indexed_by_no(electors_csv)

    # Results files keyed by district
    results_2020 = load_json(r2020_path) if r2020_path.exists() else {}
    results_2015 = load_json(r2015_path) if r2015_path.exists() else {}
    results_2010 = load_json(r2010_path) if r2010_path.exists() else {}

    base = constituencies.get(str(seat_no)) or {}

    def enrich_party_meta(code):
        code_norm = normalize_party(code) if code else None
        meta = parties_idx.get(code_norm) or parties_idx.get(code)
        return code_norm, (meta or None)

    # Current MLA
    mla_row = mla_idx.get(seat_no) or {}
    mla_name = mla_row.get("mla") or None
    mla_party_raw = (mla_row.get("party") or "").strip() or None
    mla_party, mla_party_meta = enrich_party_meta(mla_party_raw)
    mla_alliance = (mla_row.get("alliance") or "").strip() or None
    mla_note = mla_row.get("note") or None

    # Electors
    e_row = elect_idx.get(seat_no) or {}
    electors = sanitize_int(e_row.get("electors_2024"))
    shifted = sanitize_int(e_row.get("shifted_2024"))

    # Results 2020
    r2020 = find_result_for_no(results_2020, seat_no) if results_2020 else None
    winner_2020 = runner_2020 = None
    margin_2020 = None
    if r2020:
        w = r2020.get("Winner", {})
        ru = r2020.get("Runner up", {})
        w_party_norm, w_meta = enrich_party_meta(w.get("Party"))
        ru_party_norm, ru_meta = enrich_party_meta(ru.get("Party"))
        winner_2020 = {
            "name": w.get("Candidate"),
            "party": w_party_norm,
            "party_name": (w_meta or {}).get("name") if w_meta else None,
            "votes": sanitize_int(w.get("Votes")),
        }
        runner_2020 = {
            "name": ru.get("Candidate"),
            "party": ru_party_norm,
            "party_name": (ru_meta or {}).get("name") if ru_meta else None,
            "votes": sanitize_int(ru.get("Votes")),
        }
        margin_2020 = sanitize_int(r2020.get("Margin"))
    # Results 2015
    r2015 = find_result_for_no(results_2015, seat_no) if results_2015 else None
    winner_2015 = runner_2015 = None
    margin_2015 = None
    if r2015:
        w = r2015.get("Winner", {})
        ru = r2015.get("Runner up", {})
        w_party_norm, w_meta = enrich_party_meta(w.get("Party"))
        ru_party_norm, ru_meta = enrich_party_meta(ru.get("Party"))
        winner_2015 = {
            "name": w.get("Candidate"),
            "party": w_party_norm,
            "party_name": (w_meta or {}).get("name") if w_meta else None,
            "votes": sanitize_int(w.get("Votes")),
        }
        runner_2015 = {
            "name": ru.get("Candidate"),
            "party": ru_party_norm,
            "party_name": (ru_meta or {}).get("name") if ru_meta else None,
            "votes": sanitize_int(ru.get("Votes")),
        }
        margin_2015 = sanitize_int(r2015.get("Margin"))
    # Results 2010
    r2010 = find_result_for_no(results_2010, seat_no) if results_2010 else None
    winner_2010 = runner_2010 = None
    margin_2010 = None
    if r2010:
        w = r2010.get("Winner", {})
        ru = r2010.get("Runner up", {})
        w_party_norm, w_meta = enrich_party_meta(w.get("Party"))
        ru_party_norm, ru_meta = enrich_party_meta(ru.get("Party"))
        winner_2010 = {
            "name": w.get("Candidate"),
            "party": w_party_norm,
            "party_name": (w_meta or {}).get("name") if w_meta else None,
            "votes": sanitize_int(w.get("Votes")),
        }
        runner_2010 = {
            "name": ru.get("Candidate"),
            "party": ru_party_norm,
            "party_name": (ru_meta or {}).get("name") if ru_meta else None,
            "votes": sanitize_int(ru.get("Votes")),
        }
        margin_2010 = sanitize_int(r2010.get("Margin"))

    out = {
        "no": seat_no,
        "name": base.get("name"),
        "slug": base.get("slug"),
        "district": base.get("district"),
        "reserved": base.get("reserved"),
        "mla_current": {
            "name": mla_name,
            "party": mla_party,
            "party_name": (mla_party_meta or {}).get("name") if mla_party_meta else None,
            "alliance": mla_alliance,
            "note": mla_note,
        },
        "results_2020": {
            "winner": winner_2020,
            "runner_up": runner_2020,
            "margin_votes": margin_2020,
        } if r2020 else None,
        "results_2015": {
            "winner": winner_2015,
            "runner_up": runner_2015,
            "margin_votes": margin_2015,
        } if r2015 else None,
        "results_2010": {
            "winner": winner_2010,
            "runner_up": runner_2010,
            "margin_votes": margin_2010,
        } if r2010 else None,
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
