#!/usr/bin/env python3
"""Convert CSV files to JSON with schema-aware tweaks.

Usage: python csv_to_json.py parties.csv bihar_election_results_consolidated.csv
Outputs sit alongside inputs with .json extension.

Schema notes:
- parties.csv -> parties.json
  - If CSV contains per-year alliance columns (alliance_2010, alliance_2015,
    alliance_2020, alliance_2025), output a nested map `alliances` with those
    years as keys. Missing years fall back to `alliance_2020` or `alliance`.
  - If CSV only has a single `alliance` (legacy), create `alliances` using
    that value for 2020 and copy to other years as needed.
- bihar_election_results_consolidated.csv -> JSON keeps all fields, including
  runner fields for 2010/2015/2020. Output objects are written with a
  canonical key order for readability.
- Other CSV files are converted as-is (row-per-object) without field renaming.
"""

import csv
import json
import pathlib
import sys
from typing import Any, List, Dict


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
            # 2025 placeholders
            "y2025_winner_name","y2025_winner_party","y2025_winner_votes",
            "y2025_runner_name","y2025_runner_party","y2025_runner_votes",
            "y2025_margin",
            # current
            "current_mla_name","current_mla_party","current_mla_alliance","current_remarks",
            "diff_party_vs_2020","diff_name_vs_2020",
        ]
    if name.startswith("parties"):
        # Do not enforce order for parties; schema writes nested "alliances"
        return None
    return None


def csv_to_records(csv_path: pathlib.Path) -> List[Dict[str, Any]]:
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def write_json(records: List[Dict[str, Any]], json_path: pathlib.Path) -> None:
    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_file(csv_path: pathlib.Path) -> None:
    records = csv_to_records(csv_path)

    stem = csv_path.stem.lower()

    # Schema-aware transformation for parties.csv -> new parties.json (alliances per year)
    if stem.startswith("parties") and records:
        transformed: List[Dict[str, Any]] = []
        for row in records:
            # Extract alliances for years with sensible fallbacks
            def a(yr: int) -> str:
                return (
                    (row.get(f"alliance_{yr}") or row.get("alliance_2020") or row.get("alliance") or "").strip()
                )
            alliances = {
                "2010": a(2010),
                "2015": a(2015),
                "2020": a(2020),
                "2025": a(2025),
            }
            transformed.append(
                {
                    "code": (row.get("code", "").strip()),
                    "name": (row.get("name", "").strip()),
                    "color": (row.get("color", "").strip()),
                    "alliances": alliances,
                }
            )
        records = transformed

    # Canonical key order for consolidated results
    preferred = _preferred_order_for(stem)
    if preferred and records:
        projected: List[Dict[str, Any]] = []
        for r in records:
            # Build in canonical order first
            ordered: Dict[str, Any] = {k: r.get(k, "") for k in preferred}
            # Append any extra keys at the end to avoid data loss
            for k, v in r.items():
                if k not in ordered:
                    ordered[k] = v
            projected.append(ordered)
        records = projected

    json_path = csv_path.with_suffix(".json")
    write_json(records, json_path)
    print(f"Converted {csv_path.name} -> {json_path.name} ({len(records)} records)")


def main(args: List[str]) -> None:
    if not args:
        print("Usage: python csv_to_json.py <file1.csv> [file2.csv ...]")
        sys.exit(1)

    for arg in args:
        path = pathlib.Path(arg)
        if not path.exists():
            print(f"Skipping {arg}: file not found")
            continue
        convert_file(path)


if __name__ == "__main__":
    main(sys.argv[1:])
