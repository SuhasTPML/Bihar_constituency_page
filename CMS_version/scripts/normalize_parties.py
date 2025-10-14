import json
from pathlib import Path


# Canonical normalization map
NORMALIZE = {
    # JD(U)
    "JDU": "JD(U)",
    # Independent
    "Ind": "IND",
    # CPI(M)
    "CPM": "CPI(M)",
    # CPI(ML) → normalize to CPI(M) per request
    "CPI(ML)": "CPI(M)",
    "CPI (ML)": "CPI(M)",
    "CPI(ML)L": "CPI(M)",
    # HAM(S)
    "HAM": "HAM(S)",
}


def normalize_party(label: str) -> str:
    if label is None:
        return label
    return NORMALIZE.get(label, label)


def normalize_file(path: Path) -> Path:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Iterate districts -> list of seats
    for district, seats in data.items():
        if not isinstance(seats, list):
            continue
        for seat in seats:
            w = seat.get("Winner", {})
            r = seat.get("Runner up", {})
            if isinstance(w, dict) and "Party" in w:
                w["Party"] = normalize_party(w["Party"])
            if isinstance(r, dict) and "Party" in r:
                r["Party"] = normalize_party(r["Party"])

    out_path = path.with_name(path.stem + ".normalized.json")
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def collect_parties(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    s = set()
    for district, seats in data.items():
        if not isinstance(seats, list):
            continue
        for seat in seats:
            w = seat.get("Winner", {})
            r = seat.get("Runner up", {})
            if isinstance(w, dict):
                p = w.get("Party")
                if p:
                    s.add(p)
            if isinstance(r, dict):
                p = r.get("Party")
                if p:
                    s.add(p)
    return sorted(s)


def load_known_codes(parties_json: Path):
    try:
        arr = json.loads(parties_json.read_text(encoding="utf-8"))
        return {item.get("code") for item in arr if isinstance(item, dict)}
    except Exception:
        return set()


def main():
    root = Path(__file__).resolve().parent.parent
    result_files = [root / f for f in ("2010_results.json", "2015_results.json", "2020_results.json")]
    known_codes = load_known_codes(root / "parties.json")

    for f in result_files:
        before = collect_parties(f)
        out = normalize_file(f)
        after = collect_parties(out)
        unknown_after = sorted(set(after) - set(known_codes)) if known_codes else []
        print(f"=== {f.name} ===")
        print("Before:", ", ".join(before))
        print("After: ", ", ".join(after))
        if known_codes:
            print("Not in parties.json:", ", ".join(unknown_after) if unknown_after else "(all mapped)")
        print()


if __name__ == "__main__":
    main()
