#!/usr/bin/env python3
"""Convert JSON array files back to CSV with schema-aware handling.

Usage: python json_to_csv.py parties.json bihar_election_results_consolidated.json
Outputs use .csv extension in same directory.

Schema notes:
- parties.json
  - If objects have `alliances` (per‑year map), write columns:
    code,name,color,alliance_2010,alliance_2015,alliance_2020,alliance_2025
  - Else (legacy schema), write columns: code,name,color,alliance
- bihar_election_results_consolidated.json is written as-is using a
  canonical column order if recognized; otherwise falls back to the keys
  of the first record.
"""

import csv
import json
import pathlib
import sys
from typing import Any, List, Dict, Iterable


def json_to_records(json_path: pathlib.Path) -> List[Dict[str, Any]]:
    data = json.loads(json_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError(f"Expected list at top level in {json_path.name}")
    return data


def _preferred_order_for(filename: str) -> List[str] | None:
    name = filename.lower()
    if name.startswith("bihar_election_results_consolidated"):
        return [
            "no","constituency_name","slug","district","reserved",
            "lok_sabha_no","lok_sabha",
            # 2010
            "y2010_winner_name","y2010_winner_party","y2010_winner_votes",
            "y2010_runner_name","y2010_runner_party","y2010_runner_votes",
            "y2010_margin",
            # 2015
            "y2015_winner_name","y2015_winner_party","y2015_winner_votes",
            "y2015_runner_name","y2015_runner_party","y2015_runner_votes",
            "y2015_margin",
            # 2020
            "y2020_winner_name","y2020_winner_party","y2020_winner_votes",
            "y2020_runner_name","y2020_runner_party","y2020_runner_votes",
            "y2020_margin",
            # 2025 (placeholders until results available)
            "y2025_winner_name","y2025_winner_party","y2025_winner_votes",
            "y2025_runner_name","y2025_runner_party","y2025_runner_votes",
            "y2025_margin",
            "current_mla_name","current_mla_party","current_mla_alliance","current_remarks",
            "diff_party_vs_2020","diff_name_vs_2020",
        ]
    if name.startswith("parties"):
        # Caller will decide exact parties columns based on detected schema
        return None
    return None


def _collect_fieldnames(records: Iterable[Dict[str, Any]]) -> List[str]:
    seen: Dict[str, None] = {}
    for row in records:
        for k in row.keys():
            if k not in seen:
                seen[k] = None
    return list(seen.keys())


def write_csv(records: List[Dict[str, Any]], csv_path: pathlib.Path) -> None:
    if not records:
        csv_path.write_text("", encoding="utf-8")
        return

    preferred = _preferred_order_for(csv_path.stem)

    # Schema-aware projection for parties.json: enforce columns and order
    if csv_path.stem.lower().startswith("parties"):
        # Detect per-year alliances
        has_per_year = any(isinstance(r.get("alliances"), dict) for r in records)
        if has_per_year:
            def val(r, yr):
                alliances = r.get("alliances") or {}
                return (alliances.get(str(yr))
                        or alliances.get(yr)
                        or r.get(f"alliance_{yr}")
                        or r.get("alliance")
                        or "")
            projected = [
                {
                    "code": r.get("code", ""),
                    "name": r.get("name", ""),
                    "color": r.get("color", ""),
                    "alliance_2010": val(r, 2010),
                    "alliance_2015": val(r, 2015),
                    "alliance_2020": val(r, 2020),
                    "alliance_2025": val(r, 2025),
                }
                for r in records
            ]
            fieldnames = [
                "code","name","color",
                "alliance_2010","alliance_2015","alliance_2020","alliance_2025",
            ]
            records_to_write = projected
        else:
            projected = [
                {
                    "code": r.get("code", ""),
                    "name": r.get("name", ""),
                    "color": r.get("color", ""),
                    "alliance": r.get("alliance") or r.get("alliance_2020") or "",
                }
                for r in records
            ]
            fieldnames = ["code","name","color","alliance"]
            records_to_write = projected
    else:
        fieldnames = preferred or list(records[0].keys())
        records_to_write = records

    # If preferred includes keys that may be missing, include them; and add any extra keys at end
    if not preferred:
        # Extend with any unseen keys across all rows to avoid data loss
        union = _collect_fieldnames(records_to_write)
        for k in union:
            if k not in fieldnames:
                fieldnames.append(k)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in records_to_write:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def convert_file(json_path: pathlib.Path) -> None:
    records = json_to_records(json_path)
    csv_path = json_path.with_suffix(".csv")
    try:
        write_csv(records, csv_path)
        print(f"Converted {json_path.name} -> {csv_path.name} ({len(records)} records)")
    except PermissionError:
        # Fallback: write to a side file if the target is locked (common on Windows if open in another app)
        alt_path = csv_path.with_name(csv_path.stem + ".new.csv")
        write_csv(records, alt_path)
        print(
            f"Warning: Could not write {csv_path.name} (in use). Wrote to {alt_path.name} instead."
        )


def main(args: List[str]) -> None:
    if not args:
        print("Usage: python json_to_csv.py <file1.json> [file2.json ...]")
        sys.exit(1)

    for arg in args:
        path = pathlib.Path(arg)
        if not path.exists():
            print(f"Skipping {arg}: file not found")
            continue
        convert_file(path)


if __name__ == "__main__":
    main(sys.argv[1:])
