import json

# Load the 2020 results data
with open('2020_results.json', 'r', encoding='utf-8') as f:
    data_2020 = json.load(f)

# Load the current MLA data
with open('current_mla.json', 'r', encoding='utf-8') as f:
    data_current = json.load(f)

# Flatten the 2020 data
flat_2020 = []
for district, constituencies in data_2020.items():
    for constituency in constituencies:
        flat_2020.append({
            'constituency': constituency['Name'],
            'winner': constituency['Winner']['Candidate'],
            'party': constituency['Winner']['Party'],
        })

# Flatten the current data
flat_current = []
for district, constituencies in data_current.items():
    for constituency in constituencies:
        flat_current.append({
            'constituency': constituency['Constituency'],
            'winner': constituency['Name'],
            'party': constituency['Party'],
            'alliance': constituency['Alliance']
        })

# Compare the data
matches = 0
mismatches = 0
total = len(flat_2020)

print("=== COMPARISON: 2020 WINNERS vs CURRENT MLAs ===\n")

mismatches_list = []

for entry_2020 in flat_2020:
    match_found = False
    for entry_current in flat_current:
        # Normalize constituency names by removing "(SC)" or "(ST)" suffixes for comparison
        const_2020 = entry_2020['constituency'].replace(" (SC)", "").replace(" (ST)", "")
        const_current = entry_current['constituency'].replace(" (SC)", "").replace(" (ST)", "")
        
        if const_2020 == const_current:
            if entry_2020['winner'] == entry_current['winner']:
                matches += 1
                match_found = True
                break
            else:
                mismatches += 1
                mismatches_list.append({
                    'constituency': entry_2020['constituency'],
                    '2020_winner': entry_2020['winner'],
                    '2020_party': entry_2020['party'],
                    'current_winner': entry_current['winner'],
                    'current_party': entry_current['party']
                })
                match_found = True
                break
    
    if not match_found:
        print(f"Could not find matching constituency for: {entry_2020['constituency']}")

print(f"Total constituencies: {total}")
print(f"Matches (same winner): {matches}")
print(f"Mismatches (different winner): {mismatches}")
print(f"Match rate: {matches/total*100:.2f}%\n")

if mismatches_list:
    print("=== MISMATCHES DETECTED ===")
    print("Constituencies where the current MLA is different from the 2020 winner:\n")
    
    # Group by party changes
    party_changes = {}
    for mismatch in mismatches_list:
        key = f"{mismatch['2020_party']} -> {mismatch['current_party']}"
        if key in party_changes:
            party_changes[key].append(mismatch)
        else:
            party_changes[key] = [mismatch]
    
    for change, constituencies in party_changes.items():
        print(f"\n{change}: {len(constituencies)} constituencies")
        for con in constituencies:
            print(f"  - {con['constituency']}: {con['2020_winner']} -> {con['current_winner']}")

# Check for major party changes
print("\n=== MAJOR OBSERVATIONS ===")
bjp_2020 = sum(1 for entry in flat_2020 if entry['party'] == 'BJP')
bjp_current = sum(1 for entry in flat_current if entry['party'] == 'BJP')
print(f"BJP MLAs: {bjp_2020} (2020) -> {bjp_current} (current)")

rjd_2020 = sum(1 for entry in flat_2020 if entry['party'] == 'RJD')
rjd_current = sum(1 for entry in flat_current if entry['party'] == 'RJD')
print(f"RJD MLAs: {rjd_2020} (2020) -> {rjd_current} (current)")

jdu_2020 = sum(1 for entry in flat_2020 if entry['party'] == 'JDU')
jdu_current = sum(1 for entry in flat_current if entry['party'] == 'JD(U)')
print(f"JD(U) MLAs: {jdu_2020} (2020) -> {jdu_current} (current)")

print("\nNote: The current MLA data appears to be more recent than the 2020 election results,")
print("which is expected as there may have been by-elections, disqualifications,")
print("or other changes since the 2020 general elections.")