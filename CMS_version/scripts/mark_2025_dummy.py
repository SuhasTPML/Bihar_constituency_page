import json
from pathlib import Path

def main():
    path = Path('bihar_election_results_consolidated.json')
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    changed = 0
    for row in data:
        for key in ("y2025_winner_name", "y2025_runner_name"):
            val = row.get(key)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                row[key] = "Dummy"
                changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"updated_2025_name_fields: {changed}")

if __name__ == "__main__":
    main()

