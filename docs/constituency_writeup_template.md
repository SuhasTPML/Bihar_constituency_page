# Bihar Assembly Constituency Pages - Writeup Template (Formulaic)

## Overview

This template provides a **purely factual, data-driven structure** for writing constituency pages using only information that can be directly extracted from the JSON without interpretation. All statements are formulaically generated from available fields. No subjective analysis or contextual interpretation is included.

---

## Template Structure (Factual Only)

### 1. **Opening Paragraph - Constituency Introduction**

**Template:**
```
The [Constituency Name] assembly constituency (No. [No]) is located in the [District] district of Bihar. It is a [General/SC/ST - if reserved empty use "General"] seat under the [Lok Sabha] Lok Sabha constituency. [Current MLA Name] of the [Current MLA Party] currently represents this constituency.
```

**Example (Using Patna Sahib - Seat #184):**
```
The Patna Sahib assembly constituency (No. 184) is located in the Patna district of Bihar. It is a General seat under the Patna Sahib Lok Sabha constituency. Nand Kishore Yadav of the BJP currently represents this constituency.
```

**Formulaic Logic:**
- If `reserved` == "" → use "General"
- If `reserved` == "SC" → use "SC"
- If `reserved` == "ST" → use "ST"

---

### 2. **2020 Election Results**

**Template:**
```
In the 2020 Bihar Assembly elections, [Y2020 Winner Name] ([Y2020 Winner Party]) won the seat with [Y2020 Winner Votes] votes. [Y2020 Runner Name] ([Y2020 Runner Party]) was the runner-up with [Y2020 Runner Votes] votes. The victory margin was [Y2020 Margin] votes.
```

**Example (Using Patna Sahib):**
```
In the 2020 Bihar Assembly elections, Nand Kishore Yadav (BJP) won the seat with 76,402 votes. Sandeep Kumar Saurav (INC) was the runner-up with 60,038 votes. The victory margin was 16,364 votes.
```

---

### 3. **2015 Election Results**

**Template:**
```
In the 2015 Bihar Assembly elections, [Y2015 Winner Name] ([Y2015 Winner Party]) won with [Y2015 Winner Votes] votes. [Y2015 Runner Name] ([Y2015 Runner Party]) secured [Y2015 Runner Votes] votes. The margin was [Y2015 Margin] votes.
```

**Example (Using Patna Sahib):**
```
In the 2015 Bihar Assembly elections, Nand Kishore Yadav (BJP) won with 65,517 votes. Anup Kumar Sinha (JD(U)) secured 56,647 votes. The margin was 8,870 votes.
```

---

### 4. **2010 Election Results**

**Template:**
```
In the 2010 Bihar Assembly elections, [Y2010 Winner Name] ([Y2010 Winner Party]) won with [Y2010 Winner Votes] votes. [Y2010 Runner Name] ([Y2010 Runner Party]) secured [Y2010 Runner Votes] votes. The margin was [Y2010 Margin] votes.
```

**Example (Using Patna Sahib):**
```
In the 2010 Bihar Assembly elections, Nand Kishore Yadav (BJP) won with 47,820 votes. Anirudh Prasad Alias Sadhu Yadav (RJD) secured 34,541 votes. The margin was 13,279 votes.
```

---

### 5. **Electoral Pattern Summary (Formulaic)**

**Template (Based on conditional logic):**

**If same party won all 3 elections:**
```
The [Party Name] has won this constituency in all three elections between 2010 and 2020.
```

**If same candidate won all 3 elections:**
```
[Candidate Name] has won this constituency in all three elections between 2010 and 2020, representing [Party1 in 2010], [Party2 in 2015], and [Party3 in 2020].
```

**If different parties won:**
```
The constituency has seen victories by [Y2010 Winner Party] in 2010, [Y2015 Winner Party] in 2015, and [Y2020 Winner Party] in 2020.
```

**Victory margin comparison:**
```
The victory margins were [Y2010 Margin] votes in 2010, [Y2015 Margin] votes in 2015, and [Y2020 Margin] votes in 2020.
```

**Vote count comparison:**
```
The winning candidate's vote count was [Y2010 Winner Votes] in 2010, [Y2015 Winner Votes] in 2015, and [Y2020 Winner Votes] in 2020.
```

**Example (Using Patna Sahib):**
```
Nand Kishore Yadav has won this constituency in all three elections between 2010 and 2020, representing BJP in each election. The victory margins were 13,279 votes in 2010, 8,870 votes in 2015, and 16,364 votes in 2020. The winning candidate's vote count was 47,820 in 2010, 65,517 in 2015, and 76,402 in 2020.
```

---

## Complete Example: Patna Sahib Constituency (Factual Only)

```markdown
# Patna Sahib Assembly Constituency

The Patna Sahib assembly constituency (No. 184) is located in the Patna district of Bihar. It is a General seat under the Patna Sahib Lok Sabha constituency. Nand Kishore Yadav of the BJP currently represents this constituency.

In the 2020 Bihar Assembly elections, Nand Kishore Yadav (BJP) won the seat with 76,402 votes. Sandeep Kumar Saurav (INC) was the runner-up with 60,038 votes. The victory margin was 16,364 votes.

In the 2015 Bihar Assembly elections, Nand Kishore Yadav (BJP) won with 65,517 votes. Anup Kumar Sinha (JD(U)) secured 56,647 votes. The margin was 8,870 votes.

In the 2010 Bihar Assembly elections, Nand Kishore Yadav (BJP) won with 47,820 votes. Anirudh Prasad Alias Sadhu Yadav (RJD) secured 34,541 votes. The margin was 13,279 votes.

Nand Kishore Yadav has won this constituency in all three elections between 2010 and 2020, representing BJP in each election. The victory margins were 13,279 votes in 2010, 8,870 votes in 2015, and 16,364 votes in 2020. The winning candidate's vote count was 47,820 in 2010, 65,517 in 2015, and 76,402 in 2020.
```

---

## Formulaic Logic Rules

### Candidate Continuity
```python
if (y2010_winner_name == y2015_winner_name == y2020_winner_name):
    return f"{name} has won this constituency in all three elections between 2010 and 2020"
else:
    return f"The constituency has seen victories by {y2010_winner_name} in 2010, {y2015_winner_name} in 2015, and {y2020_winner_name} in 2020"
```

### Party Continuity
```python
if (y2010_winner_party == y2015_winner_party == y2020_winner_party):
    return f"{party} has won this constituency in all three elections"
elif (y2010_winner_party == y2015_winner_party):
    return f"{party1} won in 2010 and 2015, while {party2} won in 2020"
elif (y2015_winner_party == y2020_winner_party):
    return f"{party1} won in 2010, while {party2} won in 2015 and 2020"
else:
    return f"Different parties won each election: {party1} (2010), {party2} (2015), {party3} (2020)"
```

### Margin Trends
```python
margins = [y2010_margin, y2015_margin, y2020_margin]
return f"The victory margins were {margins[0]} votes in 2010, {margins[1]} votes in 2015, and {margins[2]} votes in 2020"
```

### Vote Count Progression
```python
votes = [y2010_winner_votes, y2015_winner_votes, y2020_winner_votes]
return f"The winning candidate's vote count was {votes[0]} in 2010, {votes[1]} in 2015, and {votes[2]} in 2020"
```

### Runner-up Party Pattern
```python
runners = [y2010_runner_party, y2015_runner_party, y2020_runner_party]
if (runners[0] == runners[1] == runners[2]):
    return f"{party} has been the runner-up in all three elections"
else:
    return f"The runner-up parties were {runners[0]} in 2010, {runners[1]} in 2015, and {runners[2]} in 2020"
```

---

## Data Fields Used

**All fields directly from JSON:**

**Basic Information:**
- `no` - Constituency number
- `constituency_name` - Name
- `district` - District
- `reserved` - Seat type ("", "SC", or "ST")
- `lok_sabha` - Lok Sabha constituency name
- `current_mla_name` - Current MLA
- `current_mla_party` - Current MLA's party

**2020 Election:**
- `y2020_winner_name`
- `y2020_winner_party`
- `y2020_winner_votes`
- `y2020_runner_name`
- `y2020_runner_party`
- `y2020_runner_votes`
- `y2020_margin`

**2015 Election:**
- `y2015_winner_name`
- `y2015_winner_party`
- `y2015_winner_votes`
- `y2015_runner_name`
- `y2015_runner_party`
- `y2015_runner_votes`
- `y2015_margin`

**2010 Election:**
- `y2010_winner_name`
- `y2010_winner_party`
- `y2010_winner_votes`
- `y2010_runner_name`
- `y2010_runner_party`
- `y2010_runner_votes`
- `y2010_margin`

---

## Automation Implementation

This template is **100% automatable** with simple Python logic:

```python
def generate_writeup(constituency_data):
    # Section 1: Opening
    opening = f"The {constituency_data['constituency_name']} assembly constituency (No. {constituency_data['no']}) is located in the {constituency_data['district']} district of Bihar. It is a {get_seat_type(constituency_data['reserved'])} seat under the {constituency_data['lok_sabha']} Lok Sabha constituency. {constituency_data['current_mla_name']} of the {constituency_data['current_mla_party']} currently represents this constituency."

    # Section 2-4: Election results (2020, 2015, 2010)
    results_2020 = generate_election_result(constituency_data, 2020)
    results_2015 = generate_election_result(constituency_data, 2015)
    results_2010 = generate_election_result(constituency_data, 2010)

    # Section 5: Pattern summary
    pattern = generate_pattern_summary(constituency_data)

    return f"{opening}\n\n{results_2020}\n\n{results_2015}\n\n{results_2010}\n\n{pattern}"

def get_seat_type(reserved):
    return "General" if reserved == "" else reserved

def generate_election_result(data, year):
    y = str(year)
    return f"In the {year} Bihar Assembly elections, {data[f'y{y}_winner_name']} ({data[f'y{y}_winner_party']}) won the seat with {data[f'y{y}_winner_votes']:,} votes. {data[f'y{y}_runner_name']} ({data[f'y{y}_runner_party']}) was the runner-up with {data[f'y{y}_runner_votes']:,} votes. The victory margin was {data[f'y{y}_margin']:,} votes."

def generate_pattern_summary(data):
    # Candidate continuity
    same_candidate = (data['y2010_winner_name'] == data['y2015_winner_name'] == data['y2020_winner_name'])
    same_party = (data['y2010_winner_party'] == data['y2015_winner_party'] == data['y2020_winner_party'])

    if same_candidate:
        pattern = f"{data['y2020_winner_name']} has won this constituency in all three elections between 2010 and 2020"
        if same_party:
            pattern += f", representing {data['y2020_winner_party']} in each election"
        else:
            pattern += f", representing {data['y2010_winner_party']} in 2010, {data['y2015_winner_party']} in 2015, and {data['y2020_winner_party']} in 2020"
    else:
        pattern = f"The constituency has seen victories by {data['y2010_winner_name']} in 2010, {data['y2015_winner_name']} in 2015, and {data['y2020_winner_name']} in 2020"

    # Margins
    margins = f". The victory margins were {data['y2010_margin']:,} votes in 2010, {data['y2015_margin']:,} votes in 2015, and {data['y2020_margin']:,} votes in 2020"

    # Vote counts
    votes = f". The winning candidate's vote count was {data['y2010_winner_votes']:,} in 2010, {data['y2015_winner_votes']:,} in 2015, and {data['y2020_winner_votes']:,} in 2020"

    return pattern + margins + votes + "."
```

---

## Output Characteristics

**Length:** ~200-250 words per constituency
**Tone:** Purely factual, no interpretation
**Structure:** 5 short paragraphs
**Automation:** 100% programmatic generation
**Maintenance:** Auto-updates when JSON changes
**Scalability:** Generate all 243 constituencies in seconds

This approach ensures complete consistency and eliminates any subjective language that cannot be directly derived from the data.
