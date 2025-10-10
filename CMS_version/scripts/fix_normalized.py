import json
from pathlib import Path


def fix_file(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for district, seats in data.items():
        if not isinstance(seats, list):
            continue
        for seat in seats:
            for key in ("Winner", "Runner up"):
                obj = seat.get(key)
                if isinstance(obj, dict) and obj.get("Party") == "CPI(ML)L":
                    obj["Party"] = "CPI(M)"
                    count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return count


def main():
    root = Path(__file__).resolve().parent.parent
    total = 0
    for name in ("2010_results.normalized.json", "2015_results.normalized.json", "2020_results.normalized.json"):
        p = root / name
        if p.exists():
            fixed = fix_file(p)
            print(f"{name}: fixed {fixed}")
            total += fixed
        else:
            print(f"{name}: missing")
    print(f"Total fixed: {total}")


if __name__ == "__main__":
    main()

