import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    # Use utf-8-sig to handle potential BOM
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def index_year_results(results_obj):
    """Build { seat_no:int -> rec } from normalized results JSON structure."""
    by_no = {}
    if not isinstance(results_obj, dict):
        return by_no
    for _district, rows in results_obj.items():
        if not isinstance(rows, list):
            continue
        for rec in rows:
            try:
                no = int(str(rec.get("#", "")).strip())
            except ValueError:
                continue
            by_no[no] = rec
    return by_no


def index_current_mla(mla_obj):
    """Build { seat_no:int -> {Name, Party, Alliance, Remarks} }"""
    by_no = {}
    if not isinstance(mla_obj, dict):
        return by_no
    for _district, rows in mla_obj.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            try:
                no = int(str(row.get("No.", "")).strip())
            except ValueError:
                continue
            by_no[no] = {
                "Name": row.get("Name") or "",
                "Party": row.get("Party") or "",
                "Alliance": row.get("Alliance") or "",
                "Remarks": row.get("Remarks") or "",
            }
    return by_no


def pick_party(p):
    if not isinstance(p, dict):
        return {"Candidate": "", "Party": "", "Votes": ""}
    return {
        "Candidate": p.get("Candidate") or "",
        "Party": p.get("Party") or "",
        "Votes": str(p.get("Votes") or ""),
    }


def build_record(no: int, base: dict, r2010: dict | None, r2015: dict | None, r2020: dict | None, mla: dict | None):
    def year_fields(rec: dict | None, year: int):
        y = str(year)
        out = {}
        if rec:
            w = pick_party(rec.get("Winner") or {})
            ru = pick_party(rec.get("Runner up") or {})
            margin = str(rec.get("Margin") or "")
            out[f"y{y}_winner_name"] = w["Candidate"]
            out[f"y{y}_winner_party"] = w["Party"]
            out[f"y{y}_winner_votes"] = w["Votes"]
            out[f"y{y}_runner_name"] = ru["Candidate"]
            out[f"y{y}_runner_party"] = ru["Party"]
            out[f"y{y}_runner_votes"] = ru["Votes"]
            out[f"y{y}_margin"] = margin
        else:
            # keep keys present but empty
            out[f"y{y}_winner_name"] = ""
            out[f"y{y}_winner_party"] = ""
            out[f"y{y}_winner_votes"] = ""
            out[f"y{y}_runner_name"] = ""
            out[f"y{y}_runner_party"] = ""
            out[f"y{y}_runner_votes"] = ""
            out[f"y{y}_margin"] = ""
        return out

    # Base constituency fields
    rec = {
        "no": str(no),
        "constituency_name": base.get("name") or "",
        "slug": base.get("slug") or "",
        "district": base.get("district") or "",
        "reserved": (base.get("reserved") or "") or "",
        "lok_sabha_no": str(base.get("lok_sabha_no") or ""),
        "lok_sabha": base.get("lok_sabha") or "",
    }

    # Year fields
    rec.update(year_fields(r2010, 2010))
    rec.update(year_fields(r2015, 2015))
    rec.update(year_fields(r2020, 2020))

    # Current MLA
    mla = mla or {}
    rec["current_mla_name"] = mla.get("Name") or ""
    rec["current_mla_party"] = mla.get("Party") or ""
    rec["current_mla_alliance"] = mla.get("Alliance") or ""
    rec["current_remarks"] = mla.get("Remarks") or ""

    # Diffs vs 2020
    rec["diff_party_vs_2020"] = (
        "True" if rec.get("current_mla_party") and rec.get("y2020_winner_party") and rec["current_mla_party"] != rec["y2020_winner_party"] else "False"
    )
    rec["diff_name_vs_2020"] = (
        "True" if rec.get("current_mla_name") and rec.get("y2020_winner_name") and rec["current_mla_name"] != rec["y2020_winner_name"] else "False"
    )

    return rec


def main():
    # Inputs
    constituencies = load_json(ROOT / "bihar_constituencies.json")
    parties = load_json(ROOT / "parties.json")  # not embedded, but kept for potential validation
    r2010 = index_year_results(load_json(ROOT / "2010_results.normalized.json"))
    r2015 = index_year_results(load_json(ROOT / "2015_results.normalized.json"))
    r2020 = index_year_results(load_json(ROOT / "2020_results.normalized.json"))
    mla_idx = index_current_mla(load_json(ROOT / "current_mla.json"))

    # Build consolidated rows
    rows = []
    for no_str, base in constituencies.items():
        try:
            no = int(str(no_str))
        except ValueError:
            continue
        row = build_record(
            no=no,
            base=base or {},
            r2010=r2010.get(no),
            r2015=r2015.get(no),
            r2020=r2020.get(no),
            mla=mla_idx.get(no),
        )
        rows.append(row)

    # Sort by seat number as string for stable output
    rows.sort(key=lambda r: int(r.get("no", 0)))

    out_path = ROOT / "bihar_election_results_consolidated.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
