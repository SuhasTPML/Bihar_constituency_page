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
            'votes': constituency['Winner']['Votes']
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

# Party-wise comparison
party_2015 = {}
for entry in flat_2015:
    party = entry['party']
    if party in party_2015:
        party_2015[party] += 1
    else:
        party_2015[party] = 1

party_current = {}
for entry in flat_current:
    party = entry['party']
    if party in party_current:
        party_current[party] += 1
    else:
        party_current[party] = 1

print("=== PARTY-WISE COMPARISON ===")
print("2015 Parties:")
for party, count in sorted(party_2015.items(), key=lambda x: x[1], reverse=True):
    print(f"  {party}: {count}")

print("\nCurrent Parties:")
for party, count in sorted(party_current.items(), key=lambda x: x[1], reverse=True):
    print(f"  {party}: {count}")

# Alliance-wise comparison
alliance_current = {}
for entry in flat_current:
    alliance = entry['alliance']
    if alliance in alliance_current:
        alliance_current[alliance] += 1
    else:
        alliance_current[alliance] = 1

print("\n=== ALLIANCE-WISE DISTRIBUTION (CURRENT) ===")
for alliance, count in sorted(alliance_current.items(), key=lambda x: x[1], reverse=True):
    print(f"  {alliance}: {count}")

# Find major changes
print("\n=== NOTABLE CHANGES ===")

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
                    'current_party': entry_current['party']
                })
            break

print(f"Total constituencies with party changes: {len(changes)}")

# Show some examples of changes
print("\nExamples of party changes:")
for i, change in enumerate(changes[:10]):
    print(f"  {change['constituency']}: {change['2015_party']} ({change['2015_winner']}) -> {change['current_party']} ({change['current_winner']})")

# Check specific parties
bjp_2015 = party_2015.get('BJP', 0)
bjp_current = party_current.get('BJP', 0)
rjd_2015 = party_2015.get('RJD', 0)
rjd_current = party_current.get('RJD', 0)
jdu_2015 = party_2015.get('JD(U)', 0)
jdu_current = party_current.get('JD(U)', 0)

print(f"\nBJP: {bjp_2015} (2015) -> {bjp_current} (Current)")
print(f"RJD: {rjd_2015} (2015) -> {rjd_current} (Current)")
print(f"JD(U): {jdu_2015} (2015) -> {jdu_current} (Current)")