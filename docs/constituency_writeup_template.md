# Bihar Assembly Constituency Pages - Writeup Template

## Overview

This template provides a standardized structure for writing constituency pages using data fields that are **consistently available across all 243 Bihar constituencies**. The template excludes 2025 election data and focuses on historical context, current representation, and past election trends.

---

## Template Structure

### 1. **Opening Paragraph - Constituency Introduction**

**Template:**
```
The [Constituency Name] assembly constituency is located in the [District] district of Bihar. This is a [General/SC/ST] seat represented under the [Lok Sabha] Lok Sabha constituency. The seat is currently held by [Current MLA Name] of the [Current MLA Party].
```

**Example (Using Patna Sahib - Seat #184):**
```
The Patna Sahib assembly constituency is located in the Patna district of Bihar. This is a General seat represented under the Patna Sahib Lok Sabha constituency. The seat is currently held by Nand Kishore Yadav of the BJP.
```

**Available Fields:**
- `constituency_name` - Full constituency name
- `district` - District name
- `reserved` - Seat reservation status (empty = "General", "SC", or "ST")
- `lok_sabha` - Parent Lok Sabha constituency name
- `current_mla_name` - Current sitting MLA
- `current_mla_party` - Current MLA's party affiliation

---

### 2. **Current Representation**

**Template:**
```
## Current Representation

[Current MLA Name] represents the [Constituency Name] constituency in the Bihar Legislative Assembly. [He/She] is a member of the [Current MLA Party], which is part of the [Current MLA Alliance] alliance. [Current MLA Name] won the seat in the 2020 Bihar Assembly elections with [Y2020 Winner Votes] votes, defeating [Y2020 Runner Name] of [Y2020 Runner Party] by a margin of [Y2020 Margin] votes.
```

**Example (Using Patna Sahib):**
```
## Current Representation

Nand Kishore Yadav represents the Patna Sahib constituency in the Bihar Legislative Assembly. He is a member of the BJP, which is part of the NDA alliance. Nand Kishore Yadav won the seat in the 2020 Bihar Assembly elections with 76,402 votes, defeating Sandeep Kumar Saurav of the INC by a margin of 16,364 votes.
```

**Available Fields:**
- `current_mla_name`
- `current_mla_party`
- `current_mla_alliance` (NDA, MGB, OTH, etc.)
- `y2020_winner_votes`
- `y2020_runner_name`
- `y2020_runner_party`
- `y2020_margin`

---

### 3. **Electoral History Overview**

**Template:**
```
## Electoral History

The [Constituency Name] constituency has witnessed competitive elections over the past decade. Here's a brief overview of the last three assembly elections:
```

**Available Data Points:**
- 2020 Election Results
- 2015 Election Results
- 2010 Election Results

Each election year has: winner name, winner party, winner votes, runner-up name, runner-up party, runner-up votes, and victory margin.

---

### 4. **2020 Election Results (Detailed)**

**Template:**
```
### 2020 Bihar Assembly Election

In the 2020 assembly election, [Y2020 Winner Name] of [Y2020 Winner Party] emerged victorious with [Y2020 Winner Votes] votes. The main challenger was [Y2020 Runner Name] from [Y2020 Runner Party], who secured [Y2020 Runner Votes] votes. The victory margin was [Y2020 Margin] votes.

**2020 Results at a Glance:**
- **Winner:** [Y2020 Winner Name] ([Y2020 Winner Party]) - [Y2020 Winner Votes] votes
- **Runner-up:** [Y2020 Runner Name] ([Y2020 Runner Party]) - [Y2020 Runner Votes] votes
- **Victory Margin:** [Y2020 Margin] votes
```

**Example (Using Patna Sahib):**
```
### 2020 Bihar Assembly Election

In the 2020 assembly election, Nand Kishore Yadav of BJP emerged victorious with 76,402 votes. The main challenger was Sandeep Kumar Saurav from INC, who secured 60,038 votes. The victory margin was 16,364 votes.

**2020 Results at a Glance:**
- **Winner:** Nand Kishore Yadav (BJP) - 76,402 votes
- **Runner-up:** Sandeep Kumar Saurav (INC) - 60,038 votes
- **Victory Margin:** 16,364 votes
```

**Available Fields:**
- `y2020_winner_name`
- `y2020_winner_party`
- `y2020_winner_votes`
- `y2020_runner_name`
- `y2020_runner_party`
- `y2020_runner_votes`
- `y2020_margin`

---

### 5. **2015 Election Results**

**Template:**
```
### 2015 Bihar Assembly Election

The 2015 election saw [Y2015 Winner Name] of [Y2015 Winner Party] winning the seat with [Y2015 Winner Votes] votes. [Y2015 Runner Name] from [Y2015 Runner Party] came in second with [Y2015 Runner Votes] votes. The margin of victory was [Y2015 Margin] votes.

**2015 Results Summary:**
- **Winner:** [Y2015 Winner Name] ([Y2015 Winner Party]) - [Y2015 Winner Votes] votes
- **Runner-up:** [Y2015 Runner Name] ([Y2015 Runner Party]) - [Y2015 Runner Votes] votes
- **Victory Margin:** [Y2015 Margin] votes
```

**Available Fields:**
- `y2015_winner_name`
- `y2015_winner_party`
- `y2015_winner_votes`
- `y2015_runner_name`
- `y2015_runner_party`
- `y2015_runner_votes`
- `y2015_margin`

---

### 6. **2010 Election Results**

**Template:**
```
### 2010 Bihar Assembly Election

Going back to 2010, [Y2010 Winner Name] of [Y2010 Winner Party] won the constituency with [Y2010 Winner Votes] votes. [Y2010 Runner Name] from [Y2010 Runner Party] was the runner-up with [Y2010 Runner Votes] votes. The winning margin stood at [Y2010 Margin] votes.

**2010 Results Summary:**
- **Winner:** [Y2010 Winner Name] ([Y2010 Winner Party]) - [Y2010 Winner Votes] votes
- **Runner-up:** [Y2010 Runner Name] ([Y2010 Runner Party]) - [Y2010 Runner Votes] votes
- **Victory Margin:** [Y2010 Margin] votes
```

**Available Fields:**
- `y2010_winner_name`
- `y2010_winner_party`
- `y2010_winner_votes`
- `y2010_runner_name`
- `y2010_runner_party`
- `y2010_runner_votes`
- `y2010_margin`

---

### 7. **Electoral Trends Analysis**

**Template Options:**

#### Option A: Party Continuity
```
## Electoral Trends

The [Constituency Name] constituency has shown [party continuity/political volatility] over the past three elections. [Party Name] has [held the seat consistently / won X out of 3 elections / shown growing strength / faced declining support] in this region.
```

#### Option B: Margin Analysis
```
## Electoral Trends

Victory margins in [Constituency Name] have [increased/decreased/fluctuated] over the years:
- 2010: [Y2010 Margin] votes
- 2015: [Y2015 Margin] votes
- 2020: [Y2020 Margin] votes

[This indicates/suggests...] [stronger mandate/competitive races/consolidating support].
```

#### Option C: Candidate Patterns
```
## Electoral Trends

[Constituency Name] has seen [repeat candidates/new faces/same party different candidates] across elections. Notable patterns include:
- [Observation about winning parties]
- [Observation about vote share changes]
- [Observation about challenger parties]
```

**Analysis Points You Can Derive:**
- Party dominance (which party won in which years)
- Incumbent performance (did the sitting MLA retain the seat?)
- Margin trends (increasing/decreasing margins = strengthening/weakening mandate)
- Vote share patterns (growing/declining vote counts)
- Party switches (did winners change parties between elections?)

---

### 8. **Constituency Profile**

**Template:**
```
## Constituency Profile

- **Constituency Number:** [No]
- **Constituency Name:** [Constituency Name]
- **District:** [District]
- **Seat Type:** [Reserved status - General/SC/ST]
- **Lok Sabha Constituency:** [Lok Sabha] (LS #[Lok Sabha No])
- **Current MLA:** [Current MLA Name] ([Current MLA Party])
- **Alliance:** [Current MLA Alliance]
```

**Example (Using Patna Sahib):**
```
## Constituency Profile

- **Constituency Number:** 184
- **Constituency Name:** Patna Sahib
- **District:** Patna
- **Seat Type:** General
- **Lok Sabha Constituency:** Patna Sahib (LS #29)
- **Current MLA:** Nand Kishore Yadav (BJP)
- **Alliance:** NDA
```

**Available Fields:**
- `no` - Constituency number (1-243)
- `constituency_name`
- `district`
- `reserved`
- `lok_sabha`
- `lok_sabha_no`
- `current_mla_name`
- `current_mla_party`
- `current_mla_alliance`

---

### 9. **Key Takeaways / Summary Points**

**Template:**
```
## Key Highlights

- [Constituency Name] is a [General/SC/ST] constituency in [District] district
- Currently represented by [Current MLA Name] from [Current MLA Party]
- Part of the [Current MLA Alliance] alliance in the state assembly
- Witnessed [competitive/one-sided] contests in recent elections
- [Additional notable trend from data]
```

---

## Complete Example: Patna Sahib Constituency

```markdown
# Patna Sahib Assembly Constituency - Bihar Assembly Elections

## Introduction

The Patna Sahib assembly constituency is located in the Patna district of Bihar. This is a General seat represented under the Patna Sahib Lok Sabha constituency. The seat is currently held by Nand Kishore Yadav of the BJP.

## Current Representation

Nand Kishore Yadav represents the Patna Sahib constituency in the Bihar Legislative Assembly. He is a member of the BJP, which is part of the NDA alliance. Nand Kishore Yadav won the seat in the 2020 Bihar Assembly elections with 76,402 votes, defeating Sandeep Kumar Saurav of the INC by a margin of 16,364 votes.

## Electoral History

The Patna Sahib constituency has witnessed competitive elections over the past decade. Here's a detailed look at the last three assembly elections:

### 2020 Bihar Assembly Election

In the 2020 assembly election, Nand Kishore Yadav of BJP emerged victorious with 76,402 votes. The main challenger was Sandeep Kumar Saurav from INC, who secured 60,038 votes. The victory margin was 16,364 votes.

**2020 Results at a Glance:**
- **Winner:** Nand Kishore Yadav (BJP) - 76,402 votes
- **Runner-up:** Sandeep Kumar Saurav (INC) - 60,038 votes
- **Victory Margin:** 16,364 votes

### 2015 Bihar Assembly Election

The 2015 election saw Nand Kishore Yadav of BJP winning the seat with 65,517 votes. Anup Kumar Sinha from JD(U) came in second with 56,647 votes. The margin of victory was 8,870 votes.

**2015 Results Summary:**
- **Winner:** Nand Kishore Yadav (BJP) - 65,517 votes
- **Runner-up:** Anup Kumar Sinha (JD(U)) - 56,647 votes
- **Victory Margin:** 8,870 votes

### 2010 Bihar Assembly Election

Going back to 2010, Nand Kishore Yadav of BJP won the constituency with 47,820 votes. Anirudh Prasad Alias Sadhu Yadav from RJD was the runner-up with 34,541 votes. The winning margin stood at 13,279 votes.

**2010 Results Summary:**
- **Winner:** Nand Kishore Yadav (BJP) - 47,820 votes
- **Runner-up:** Anirudh Prasad Alias Sadhu Yadav (RJD) - 34,541 votes
- **Victory Margin:** 13,279 votes

## Electoral Trends

The Patna Sahib constituency has shown remarkable party continuity over the past three elections. BJP's Nand Kishore Yadav has held the seat consistently since 2010, demonstrating strong voter loyalty in this urban constituency.

Victory margins have fluctuated but remained substantial:
- 2010: 13,279 votes
- 2015: 8,870 votes
- 2020: 16,364 votes

The 2020 election saw an increased margin compared to 2015, indicating a strengthening mandate. Nand Kishore Yadav's vote share has also grown consistently across all three elections, from 47,820 votes in 2010 to 76,402 votes in 2020.

## Constituency Profile

- **Constituency Number:** 184
- **Constituency Name:** Patna Sahib
- **District:** Patna
- **Seat Type:** General
- **Lok Sabha Constituency:** Patna Sahib (LS #29)
- **Current MLA:** Nand Kishore Yadav (BJP)
- **Alliance:** NDA

## Key Highlights

- Patna Sahib is a General constituency in Patna district
- Currently represented by Nand Kishore Yadav from BJP
- Part of the NDA alliance in the state assembly
- Witnessed consistent BJP victories with the same candidate winning three consecutive terms
- Urban constituency showing growing vote counts and strengthening margins for the incumbent
```

---

## Data Fields Reference

### Always Available (All 243 Constituencies):

**Basic Information:**
- `no` - Constituency number (1-243)
- `constituency_name` - Full name
- `slug` - URL-friendly slug
- `district` - District name
- `reserved` - "" (General), "SC", or "ST"
- `lok_sabha_no` - Parent Lok Sabha constituency number
- `lok_sabha` - Parent Lok Sabha constituency name

**Current MLA:**
- `current_mla_name`
- `current_mla_party`
- `current_mla_alliance`
- `current_remarks` (usually empty)

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

### Excluded from Template (2025 Data - Not Yet Declared):
- `y2025_winner_name`
- `y2025_winner_party`
- `y2025_winner_votes`
- `y2025_runner_name`
- `y2025_runner_party`
- `y2025_runner_votes`
- `y2025_margin`

---

## Usage Notes

1. **Pronoun Usage:** Use gender-neutral language or check candidate names to determine appropriate pronouns (He/She/They).

2. **Reserved Seats:** If `reserved` field is empty, use "General" in writeup. Otherwise, use "SC" or "ST" as applicable.

3. **Margin Formatting:** Format large numbers with commas for readability (e.g., 16,364 not 16364).

4. **Party Names:** Use party codes as-is from data (BJP, INC, JD(U), RJD, etc.). Consider expanding full names in first mention.

5. **Trend Analysis:** This requires manual analysis based on the numerical data. Look for:
   - Same party winning multiple times = party stronghold
   - Different parties winning = swing constituency
   - Increasing margins = strengthening base
   - Decreasing margins = competitive seat

6. **Bulk Generation:** This template can be programmatically populated using the JSON data for all 243 constituencies.

---

## Automation Potential

This template structure can be easily automated using:
- Python script to read JSON and populate template
- Jinja2 template engine for bulk generation
- Simple find-replace for field substitution
- Logic for trend analysis based on patterns

Would enable quick generation of 243 constituency pages with consistent structure and formatting.
