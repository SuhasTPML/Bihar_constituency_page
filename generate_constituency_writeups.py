"""
Generate constituency writeups for all 243 Bihar constituencies.
Creates factual, data-driven text based on JSON data.
"""

import json
import os


def get_seat_type(reserved):
    """Convert reserved field to readable seat type."""
    return "General" if reserved == "" else reserved


def generate_election_result(data, year):
    """Generate election result paragraph for a specific year."""
    y = str(year)
    winner_name = data.get(f'y{y}_winner_name', '')
    winner_party = data.get(f'y{y}_winner_party', '')
    winner_votes = data.get(f'y{y}_winner_votes', 0)
    runner_name = data.get(f'y{y}_runner_name', '')
    runner_party = data.get(f'y{y}_runner_party', '')
    runner_votes = data.get(f'y{y}_runner_votes', 0)
    margin = data.get(f'y{y}_margin', 0)

    # Format numbers with commas
    winner_votes_fmt = f"{winner_votes:,}" if winner_votes else "0"
    runner_votes_fmt = f"{runner_votes:,}" if runner_votes else "0"
    margin_fmt = f"{margin:,}" if margin else "0"

    return f"In the {year} Bihar Assembly elections, {winner_name} ({winner_party}) won the seat with {winner_votes_fmt} votes. {runner_name} ({runner_party}) was the runner-up with {runner_votes_fmt} votes. The victory margin was {margin_fmt} votes."


def generate_pattern_summary(data):
    """Generate electoral pattern summary paragraph."""
    # Candidate continuity check
    w2010 = data.get('y2010_winner_name', '')
    w2015 = data.get('y2015_winner_name', '')
    w2020 = data.get('y2020_winner_name', '')

    p2010 = data.get('y2010_winner_party', '')
    p2015 = data.get('y2015_winner_party', '')
    p2020 = data.get('y2020_winner_party', '')

    same_candidate = (w2010 == w2015 == w2020) and w2020 != ''
    same_party = (p2010 == p2015 == p2020) and p2020 != ''

    # Build pattern statement
    if same_candidate:
        pattern = f"{w2020} has won this constituency in all three elections between 2010 and 2020"
        if same_party:
            pattern += f", representing {p2020} in each election"
        else:
            pattern += f", representing {p2010} in 2010, {p2015} in 2015, and {p2020} in 2020"
    else:
        pattern = f"The constituency has seen victories by {w2010} in 2010, {w2015} in 2015, and {w2020} in 2020"

    # Margins
    m2010 = data.get('y2010_margin', 0)
    m2015 = data.get('y2015_margin', 0)
    m2020 = data.get('y2020_margin', 0)

    m2010_fmt = f"{m2010:,}" if m2010 else "0"
    m2015_fmt = f"{m2015:,}" if m2015 else "0"
    m2020_fmt = f"{m2020:,}" if m2020 else "0"

    margins = f". The victory margins were {m2010_fmt} votes in 2010, {m2015_fmt} votes in 2015, and {m2020_fmt} votes in 2020"

    # Vote counts
    v2010 = data.get('y2010_winner_votes', 0)
    v2015 = data.get('y2015_winner_votes', 0)
    v2020 = data.get('y2020_winner_votes', 0)

    v2010_fmt = f"{v2010:,}" if v2010 else "0"
    v2015_fmt = f"{v2015:,}" if v2015 else "0"
    v2020_fmt = f"{v2020:,}" if v2020 else "0"

    votes = f". The winning candidate's vote count was {v2010_fmt} in 2010, {v2015_fmt} in 2015, and {v2020_fmt} in 2020"

    return pattern + margins + votes + "."


def generate_writeup(constituency_data):
    """Generate complete writeup for a constituency."""
    # Section 1: Opening
    name = constituency_data.get('constituency_name', '')
    no = constituency_data.get('no', '')
    district = constituency_data.get('district', '')
    reserved = constituency_data.get('reserved', '')
    lok_sabha = constituency_data.get('lok_sabha', '')
    current_mla = constituency_data.get('current_mla_name', '')
    current_party = constituency_data.get('current_mla_party', '')

    seat_type = get_seat_type(reserved)

    opening = f"The {name} assembly constituency (No. {no}) is located in the {district} district of Bihar. It is a {seat_type} seat under the {lok_sabha} Lok Sabha constituency. {current_mla} of the {current_party} currently represents this constituency."

    # Section 2-4: Election results
    results_2020 = generate_election_result(constituency_data, 2020)
    results_2015 = generate_election_result(constituency_data, 2015)
    results_2010 = generate_election_result(constituency_data, 2010)

    # Section 5: Pattern summary
    pattern = generate_pattern_summary(constituency_data)

    # Combine all sections
    writeup = f"{opening}\n\n{results_2020}\n\n{results_2015}\n\n{results_2010}\n\n{pattern}"

    return writeup


def main():
    """Main function to generate writeups for all constituencies."""
    # Load consolidated data
    json_file = 'bihar_election_results_consolidated.json'

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        constituencies = json.load(f)

    print(f"Loaded {len(constituencies)} constituencies")

    # Create output directory
    output_dir = 'constituency_writeups'
    os.makedirs(output_dir, exist_ok=True)

    # Generate writeup for each constituency
    for constituency in constituencies:
        no = constituency.get('no', 0)
        name = constituency.get('constituency_name', 'Unknown')
        slug = constituency.get('slug', f'constituency-{no}')

        # Generate writeup
        writeup = generate_writeup(constituency)

        # Create markdown file
        filename = f"{str(no).zfill(3)}-{slug}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {name} Assembly Constituency\n\n")
            f.write(writeup)
            f.write("\n")

        print(f"Generated: {filename}")

    print(f"\nSuccessfully generated {len(constituencies)} writeups in '{output_dir}' directory")

    # Show sample output (first constituency)
    if constituencies:
        print("\n" + "="*80)
        print("SAMPLE OUTPUT (First Constituency):")
        print("="*80)
        sample = generate_writeup(constituencies[0])
        print(f"\n# {constituencies[0]['constituency_name']} Assembly Constituency\n")
        print(sample)
        print("\n" + "="*80)


if __name__ == "__main__":
    main()
