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
print(f"{'Party':<15} {'2015':<10} {'Current':<10} {'Change':<10}")
print("-" * 45)
all_parties = set(list(party_2015.keys()) + list(party_current.keys()))
for party in sorted(all_parties, key=lambda x: (party_current.get(x, 0), party_2015.get(x, 0)), reverse=True):
    count_2015 = party_2015.get(party, 0)
    count_current = party_current.get(party, 0)
    change = count_current - count_2015
    sign = "+" if change > 0 else "" if change == 0 else ""
    print(f"{party:<15} {count_2015:<10} {count_current:<10} {sign}{change:<10}")

# Alliance-wise comparison
alliance_current = {}
for entry in flat_current:
    alliance = entry['alliance']
    if alliance in alliance_current:
        alliance_current[alliance] += 1
    else:
        alliance_current[alliance] = 1

print("\n=== ALLIANCE-WISE DISTRIBUTION (CURRENT) ===")
print(f"{'Alliance':<15} {'Seats':<10}")
print("-" * 25)
for alliance, count in sorted(alliance_current.items(), key=lambda x: x[1], reverse=True):
    print(f"{alliance:<15} {count:<10}")

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

print(f"Total constituencies with party changes: {len(changes)} out of 243")

# Find the biggest gainers and losers
print("\n=== BIGGEST PARTY GAINS ===")
gains = []
for party in all_parties:
    count_2015 = party_2015.get(party, 0)
    count_current = party_current.get(party, 0)
    change = count_current - count_2015
    if change > 0:
        gains.append((party, change))

gains.sort(key=lambda x: x[1], reverse=True)
for party, gain in gains[:5]:
    print(f"  {party}: +{gain} seats")

print("\n=== BIGGEST PARTY LOSSES ===")
losses = []
for party in all_parties:
    count_2015 = party_2015.get(party, 0)
    count_current = party_current.get(party, 0)
    change = count_current - count_2015
    if change < 0:
        losses.append((party, abs(change)))

losses.sort(key=lambda x: x[1], reverse=True)
for party, loss in losses[:5]:
    print(f"  {party}: -{loss} seats")

# Notable individual changes
print("\n=== NOTABLE INDIVIDUAL WINNERS/LOSERS ===")

# Find BJP's biggest gains
bjp_gains = []
for entry_2015 in flat_2015:
    for entry_current in flat_current:
        if entry_2015['constituency'] == entry_current['constituency']:
            if entry_2015['party'] != 'BJP' and entry_current['party'] == 'BJP':
                bjp_gains.append({
                    'constituency': entry_2015['constituency'],
                    '2015_winner': entry_2015['winner'],
                    '2015_party': entry_2015['party'],
                    'current_winner': entry_current['winner']
                })
            break

print(f"BJP gained {len(bjp_gains)} seats from other parties:")
for gain in bjp_gains[:5]:
    print(f"  {gain['constituency']}: {gain['2015_party']} ({gain['2015_winner']}) -> BJP ({gain['current_winner']})")

# Find RJD's losses
rjd_losses = []
for entry_2015 in flat_2015:
    for entry_current in flat_current:
        if entry_2015['constituency'] == entry_current['constituency']:
            if entry_2015['party'] == 'RJD' and entry_current['party'] != 'RJD':
                rjd_losses.append({
                    'constituency': entry_2015['constituency'],
                    '2015_winner': entry_2015['winner'],
                    'current_winner': entry_current['winner'],
                    'current_party': entry_current['party']
                })
            break

print(f"\nRJD lost {len(rjd_losses)} seats to other parties:")
for loss in rjd_losses[:5]:
    print(f"  {loss['constituency']}: RJD ({loss['2015_winner']}) -> {loss['current_party']} ({loss['current_winner']})")

# Find JD(U)'s losses
jdu_losses = []
for entry_2015 in flat_2015:
    for entry_current in flat_current:
        if entry_2015['constituency'] == entry_current['constituency']:
            if entry_2015['party'] == 'JD(U)' and entry_current['party'] != 'JD(U)':
                jdu_losses.append({
                    'constituency': entry_2015['constituency'],
                    '2015_winner': entry_2015['winner'],
                    'current_winner': entry_current['winner'],
                    'current_party': entry_current['party']
                })
            break

print(f"\nJD(U) lost {len(jdu_losses)} seats to other parties:")
for loss in jdu_losses[:5]:
    print(f"  {loss['constituency']}: JD(U) ({loss['2015_winner']}) -> {loss['current_party']} ({loss['current_winner']})")

# Find new parties that emerged
new_parties = set(party_current.keys()) - set(party_2015.keys())
if new_parties:
    print(f"\nNew parties that emerged since 2015: {', '.join(new_parties)}")

# Find parties that disappeared
disappeared_parties = set(party_2015.keys()) - set(party_current.keys())
if disappeared_parties:
    print(f"Parties that disappeared since 2015: {', '.join(disappeared_parties)}")

print("\n=== SUMMARY ===")
total_seats = len(flat_current)
nda_seats = alliance_current.get('NDA', 0)
mgb_seats = alliance_current.get('MGB', 0)
other_seats = total_seats - nda_seats - mgb_seats

print(f"Total seats: {total_seats}")
print(f"NDA seats: {nda_seats} ({nda_seats/total_seats*100:.1f}%)")
print(f"MGB seats: {mgb_seats} ({mgb_seats/total_seats*100:.1f}%)")
print(f"Others seats: {other_seats} ({other_seats/total_seats*100:.1f}%)")
print(f"Seats that changed party: {len(changes)} ({len(changes)/total_seats*100:.1f}%)")