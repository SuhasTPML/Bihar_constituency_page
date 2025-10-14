import json

# Load the 2015 results data
with open('2015_results.json', 'r', encoding='utf-8') as f:
    data_2015 = json.load(f)

# Load the current MLA data
with open('current_mla.json', 'r', encoding='utf-8') as f:
    data_current = json.load(f)

# Flatten the 2015 data
flat_2015 = []
for district, constituencies in data_2015.items():
    for constituency in constituencies:
        flat_2015.append({
            'constituency': constituency['Name'],
            'winner': constituency['Winner']['Candidate'],
            'party': constituency['Winner']['Party'],
            'votes': constituency['Winner']['Votes'],
            'margin': constituency['Margin']
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

# Find constituencies where the party changed
changes = []
for entry_2015 in flat_2015:
    for entry_current in flat_current:
        if entry_2015['constituency'] == entry_current['constituency']:
            if entry_2015['party'] != entry_current['party']:
                changes.append({
                    'constituency': entry_2015['constituency'],
                    '2015_winner': entry_2015['winner'],
                    '2015_party': entry_2015['party'],
                    'current_winner': entry_current['winner'],
                    'current_party': entry_current['party'],
                    'alliance': entry_current['alliance']
                })
            break

# Group changes by party movements
party_movements = {}
for change in changes:
    key = f"{change['2015_party']} -> {change['current_party']}"
    if key in party_movements:
        party_movements[key].append(change)
    else:
        party_movements[key] = [change]

print("=== MAJOR CONSTITUENCY-LEVEL CHANGES ===")
print(f"Total constituencies with party changes: {len(changes)} out of 243 ({len(changes)/243*100:.1f}%)\n")

print("=== PARTY MOVEMENTS ===")
for movement, constituencies in sorted(party_movements.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n{movement}: {len(constituencies)} constituencies")
    if len(constituencies) <= 5:
        for con in constituencies:
            print(f"  - {con['constituency']}: {con['2015_winner']} -> {con['current_winner']}")
    else:
        for con in constituencies[:3]:
            print(f"  - {con['constituency']}: {con['2015_winner']} -> {con['current_winner']}")
        print(f"  ... and {len(constituencies)-3} more")

# Find the most competitive constituencies in 2015 (smallest margins)
flat_2015_sorted = sorted(flat_2015, key=lambda x: int(x['margin'].replace(',', '')))
print("\n=== CLOSEST CONTESTS IN 2015 ===")
print("Top 10 constituencies with smallest winning margins:")
for i, con in enumerate(flat_2015_sorted[:10]):
    margin = int(con['margin'].replace(',', ''))
    print(f"  {i+1}. {con['constituency']}: {con['winner']} ({con['party']}) won by {margin:,} votes")

# Find constituencies that switched alliances
alliance_changes = []
for entry_2015 in flat_2015:
    for entry_current in flat_current:
        if entry_2015['constituency'] == entry_current['constituency']:
            # Determine 2015 alliance based on party
            if entry_2015['party'] in ['BJP', 'JD(U)']:
                alliance_2015 = 'NDA'
            elif entry_2015['party'] in ['RJD', 'INC']:
                alliance_2015 = 'MGB'
            else:
                alliance_2015 = 'Others'
                
            if entry_current['alliance'] != alliance_2015:
                alliance_changes.append({
                    'constituency': entry_2015['constituency'],
                    '2015_winner': entry_2015['winner'],
                    '2015_party': entry_2015['party'],
                    '2015_alliance': alliance_2015,
                    'current_winner': entry_current['winner'],
                    'current_party': entry_current['party'],
                    'current_alliance': entry_current['alliance']
                })
            break

print(f"\n=== ALLIANCE SWITCHES ===")
print(f"Total constituencies that switched alliances: {len(alliance_changes)}")
for change in alliance_changes[:10]:
    print(f"  {change['constituency']}: {change['2015_alliance']} -> {change['current_alliance']}")
    print(f"    2015: {change['2015_winner']} ({change['2015_party']})")
    print(f"    Current: {change['current_winner']} ({change['current_party']})")