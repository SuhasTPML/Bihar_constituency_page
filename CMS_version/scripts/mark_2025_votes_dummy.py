import json
from pathlib import Path

def main():
    path = Path('bihar_election_results_consolidated.json')
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    changed = 0
    for row in data:
        wv = row.get('y2025_winner_votes')
        rv = row.get('y2025_runner_votes')
        if wv is None or (isinstance(wv, str) and wv.strip() == ""):
            row['y2025_winner_votes'] = "1"
            changed += 1
        if rv is None or (isinstance(rv, str) and rv.strip() == ""):
            row['y2025_runner_votes'] = "0"
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"updated_2025_vote_fields: {changed}")

if __name__ == "__main__":
    main()

