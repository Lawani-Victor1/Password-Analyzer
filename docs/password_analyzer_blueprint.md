# Password Security Analyzer — Complete Technical Blueprint

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [main.py — Entry Point](#2-mainpy--entry-point)
3. [analysis.py — Analysis Engine](#3-analysispy--analysis-engine)
4. [attacks.py — Attack Simulation](#4-attackspy--attack-simulation)
5. [scoring.py — Scoring Engine](#5-scoringpy--scoring-engine)
6. [visualization.py — Visualization Module](#6-visualizationpy--visualization-module)
7. [utils.py — Shared Helpers](#7-utilspy--shared-helpers)
8. [Scoring System — Full Breakdown](#8-scoring-system--full-breakdown)
9. [requirements.txt](#9-requirementstxt)
10. [README — Study Guide Structure](#10-readme--study-guide-structure)
11. [Data Flow — Full Picture](#11-data-flow--full-picture)

---

## 1. Project Structure

```
password_analyzer/
│
├── main.py                 # Entry point, CLI handler
├── analysis.py             # Module 1 - Analysis Engine
├── attacks.py              # Module 2 - Attack Simulation
├── scoring.py              # Module 3 - Scoring Engine
├── visualization.py        # Module 4 - Visualization
├── utils.py                # Shared helper functions
│
├── wordlists/
│   ├── tier1_top1000.txt
│   ├── tier2_rockyou_100k.txt
│   └── tier3_extended.txt
│
├── output/
│   └── report.png          # Saved matplotlib chart
│
├── requirements.txt        # All dependencies
└── README.md               # Study guide + setup
```

---

## 2. main.py — Entry Point

**Purpose:** The face of the application. Handles user interaction, calls each module in order, and passes data between them.

### Flow

```
Start
  ↓
Display welcome banner
  ↓
Prompt user for password input
  ↓
Call Analysis Engine → get analysis_result
  ↓
Call Attack Simulation → get attack_result
  ↓
Call Scoring Engine → get final_score
  ↓
Call Visualization → display everything
  ↓
Ask user if they want to test another password
  ↓
End
```

### CLI Interaction — What the User Sees

```
========================================
   Password Security Analyzer v1.0
========================================

Enter password to analyze: ********

[1/4] Running analysis...
[2/4] Simulating attacks...
[3/4] Calculating score...
[4/4] Generating report...

Done. Results below.
```

### Session Data Object

One dictionary travels through every module:

```
session = {
  "password": raw input,
  "analysis": analysis_result,
  "attacks": attack_result,
  "score": final_score
}
```

Everything travels in one dictionary. Clean, simple, explainable.

---

## 3. analysis.py — Analysis Engine

**Purpose:** Dissect the password. Understand what it is made of before any attack runs.

**Inputs:** Raw password string

**Outputs:**

```
analysis_result = {
  "length": int,
  "charset": {
    "lowercase": bool,
    "uppercase": bool,
    "digits": bool,
    "symbols": bool,
    "charset_size": int
  },
  "entropy": float,
  "patterns": {
    "keyboard_walk": bool,
    "repeated_chars": bool,
    "leet_speak": bool,
    "sequential": bool,
    "common_word_embedded": bool,
    "predictable_structure": bool
  }
}
```

---

### Function 1 — get_length(password)

**Logic:**
- Count characters in the password
- Return integer

---

### Function 2 — detect_charset(password)

**Logic:**
1. Check if any character is a lowercase letter → set lowercase = True
2. Check if any character is an uppercase letter → set uppercase = True
3. Check if any character is a digit → set digits = True
4. Check if any character is a symbol (not letter, not digit) → set symbols = True
5. Calculate charset_size:
   - Start at 0
   - lowercase present → add 26
   - uppercase present → add 26
   - digits present → add 10
   - symbols present → add 33
6. Return charset dictionary

---

### Function 3 — calculate_entropy(password, charset_size)

**Logic:**
1. Get password length
2. Get charset_size from detect_charset
3. Formula: `entropy = length × log2(charset_size)`
4. Return float rounded to 2 decimal places

> **Why log2?** Entropy is measured in bits. Each bit represents a binary choice. This is standard information theory — defensible in any presentation.

---

### Function 4 — detect_patterns(password)

**Logic — check each pattern independently:**

#### Keyboard Walk
- Define known walks: `qwerty`, `asdf`, `zxcv`, `qwer`, `1234`, `2345` etc.
- Check if any walk substring appears in the lowercased password
- If yes → `keyboard_walk = True`

#### Repeated Characters
- Scan through password
- If any character appears 3 or more times consecutively → `repeated_chars = True`
- Example: `aaa`, `111`

#### L33tspeak
- Define substitution map: `a→@`, `e→3`, `i→1`, `o→0`, `s→$`, `t→7`
- Replace all l33t chars in password with their letter equivalents
- Check if result appears in wordlist
- If yes → `leet_speak = True`

#### Sequential
- Check for ascending sequences: `abc`, `bcd`, `123`, `234` etc.
- Check for descending sequences: `cba`, `321` etc.
- If found → `sequential = True`

#### Common Word Embedded
- Load Tier 1 wordlist
- Check if any word from it appears as a substring of the password
- If yes → `common_word_embedded = True`

#### Predictable Structure
- Check if password matches pattern: Capital letter + lowercase word + numbers at end
- Example: `Password123`, `Michael2024`
- If yes → `predictable_structure = True`

---

## 4. attacks.py — Attack Simulation

**Purpose:** Simulate three real attack types against the password.

**Inputs:** Password string, wordlist paths

**Outputs:**

```
attack_result = {
  "dictionary": {
    "found": bool,
    "tier": int or None,
    "matched_word": str or None
  },
  "rule_based": {
    "found": bool,
    "base_word": str or None,
    "rule_applied": str or None,
    "mutated_form": str or None
  },
  "brute_force": {
    "charset_size": int,
    "keyspace": int,
    "crack_time_seconds": float,
    "crack_time_readable": str
  }
}
```

### Execution Order

```
Dictionary Attack → Rule-based Mutation → Brute-force Estimator
```

If the dictionary attack finds a match, flag it immediately but still run the others for a complete report.

---

### Function 1 — dictionary_attack(password)

**Concept:** Real attackers don't guess randomly — they try known passwords first. Rockyou alone has 14 million entries. Most users are in there.

**Wordlist — Tiered Loading Strategy:**

| Tier | Wordlist | Size | Purpose |
|---|---|---|---|
| Tier 1 | Top 1000 common passwords | ~1k entries | Fastest check |
| Tier 2 | Rockyou subset | ~100k entries | Broad coverage |
| Tier 3 | Full extended list | Variable | Deep check |

**Logic:**
1. Normalize password → lowercase, strip whitespace
2. Load Tier 1 wordlist
3. Compare normalized password against every entry
4. If match → return `found=True`, `tier=1`, `matched_word`
5. If no match → load Tier 2, repeat
6. If no match → load Tier 3, repeat
7. If no match anywhere → return `found=False`, `tier=None`, `matched_word=None`

**What it reports:**
- Found / Not Found
- Which tier it was found in
- Exact matched word

---

### Function 2 — rule_based_attack(password)

**Concept:** Attackers apply transformations to wordlists. Tools like Hashcat do this automatically. We simulate it manually.

**Mutation Rules — Applied to Every Word in Tier 1 + Tier 2:**

| Rule ID | Rule Name | Example Transformation |
|---|---|---|
| R1 | Capitalize first letter | `password → Password` |
| R2 | All caps | `password → PASSWORD` |
| R3 | Append numbers | `password → password1, password12, password123, password1234` |
| R4 | Prepend numbers | `password → 1password, 12password, 123password` |
| R5 | L33tspeak substitution | `password → p@ssw0rd` |
| R6 | Append symbols | `password → password!, password@, password#` |
| R7 | Reverse the word | `password → drowssap` |
| R8 | Double the word | `pass → passpass` |
| R9 | Year append | `password → password2020, password2021, password2022, password2023, password2024` |

**Logic:**
1. Load Tier 1 + Tier 2 wordlists
2. For each word in the wordlist, apply every rule and generate variants
3. Compare each variant against the input password
4. If any variant matches → return `found=True`, `base_word`, `rule_applied`, `mutated_form`
5. If nothing matches → return `found=False`, all fields `None`

**What it reports:**
- Found / Not Found
- Which base word was used
- Which rule exposed it
- Example: *"password → Password matched via R1: Capitalize first letter"*

---

### Function 3 — brute_force_estimator(password, charset_size)

**Concept:** Does not actually try combinations — calculates how long it would take based on mathematics.

**The Formula:**
```
Keyspace         = charset_size ^ password_length
Crack time (sec) = Keyspace / guesses_per_second
```

**Charset Size Reference:**

| Characters Used | Charset Size |
|---|---|
| Lowercase only | 26 |
| + Uppercase | 52 |
| + Digits | 62 |
| + Symbols | 95 |

**Assumed Hardware Speed:** 10,000,000,000 guesses/second (10 billion) — represents a modern GPU cracking offline hashes. Realistic and defensible.

**Logic:**
1. Detect which character types are present in the password
2. Determine charset size from the table above
3. Calculate keyspace = charset_size ^ length
4. Divide by 10 billion to get seconds
5. Convert seconds into human-readable time:
   - Under 60 → "X seconds"
   - Under 3,600 → "X minutes"
   - Under 86,400 → "X hours"
   - Under 2,592,000 → "X days"
   - Under 31,536,000 → "X months"
   - Above → "X years"
6. Return full brute_force result dictionary

**What it reports:**
- Character set detected
- Keyspace size
- Estimated crack time in plain language
- Example: *"Using uppercase + lowercase + digits, a 9-character password would take approximately 3 hours to brute-force at 10 billion guesses/second"*

---

## 5. scoring.py — Scoring Engine

**Purpose:** Take all results, calculate the final score, classify it, and generate human-readable feedback.

**Inputs:** `analysis_result`, `attack_result`

**Outputs:**

```
final_score = {
  "pillar_scores": {
    "composition": int,
    "unpredictability": int,
    "attack_resistance": int,
    "red_flags": int
  },
  "total": int,
  "classification": str,
  "weaknesses": [list of strings],
  "suggestions": [list of strings]
}
```

---

### Scoring Pillars — Overview

| Pillar | Max Points | Purpose |
|---|---|---|
| Composition | 20 | Raw material of the password |
| Unpredictability | 20 | How structurally random it is |
| Attack Resistance | 45 | Real-world survival against attacks |
| Red Flags | 15 | Penalty layer for predictable patterns |
| **Total** | **100** | |

> **Why Attack Resistance carries the most weight?**
> Because a password's true strength is measured by whether an attacker can actually crack it — not just how it looks on paper.

---

### Function 1 — score_composition(analysis_result)

**Length — 12 points:**

| Length | Points |
|---|---|
| 1–5 characters | 0 |
| 6–7 characters | 3 |
| 8–9 characters | 6 |
| 10–11 characters | 9 |
| 12–15 characters | 11 |
| 16+ characters | 12 |

**Character Variety — 8 points:**

| Character Type Present | Points |
|---|---|
| Lowercase letters | 2 |
| Uppercase letters | 2 |
| Digits | 2 |
| Symbols | 2 |

2 points per type used. Maximum 8 points.

**Maximum total: 20 points**

---

### Function 2 — score_unpredictability(analysis_result)

**Entropy — 12 points:**

| Entropy (bits) | Points |
|---|---|
| Below 28 | 0 |
| 28–35 | 3 |
| 36–49 | 6 |
| 50–59 | 9 |
| 60+ | 12 |

**Pattern Absence — 8 points:**

Start at 8. Deduct per detected pattern:

| Pattern Detected | Deduction |
|---|---|
| Keyboard walk | -3 |
| Repeated characters | -2 |
| L33tspeak substitution | -2 |
| Sequential characters | -1 |

Minimum 0. No negative scores.

**Maximum total: 20 points**

---

### Function 3 — score_attack_resistance(attack_result)

| Attack | Found | Points |
|---|---|---|
| Dictionary Attack | Not found | 15 |
| Dictionary Attack | Found | 0 |
| Rule-based Attack | Not found | 15 |
| Rule-based Attack | Found | 0 |

> Found means cracked. No partial credit.

**Brute-force — 15 points:**

| Estimated Crack Time | Points |
|---|---|
| Under 1 minute | 0 |
| 1 minute – 1 hour | 3 |
| 1 hour – 1 day | 6 |
| 1 day – 1 month | 9 |
| 1 month – 1 year | 12 |
| Over 1 year | 15 |

**Maximum total: 45 points**

---

### Function 4 — score_red_flags(analysis_result)

Start at 15. Deduct per flag:

| Red Flag | Deduction |
|---|---|
| Contains common dictionary word embedded | -5 |
| Follows Word + numbers structure | -4 |
| Only first letter capitalized | -3 |
| Ends with common suffix (!, 123, @1) | -3 |

Minimum 0.

**Maximum total: 15 points**

---

### Function 5 — classify(total_score)

| Score Range | Classification |
|---|---|
| 0–25 | Very Weak |
| 26–50 | Weak |
| 51–75 | Moderate |
| 76–90 | Strong |
| 91–100 | Very Strong |

---

### Function 6 — generate_feedback(analysis_result, attack_result, pillar_scores)

For every weakness detected, add a plain-English message and a corresponding suggestion:

| Weakness | Message | Suggestion |
|---|---|---|
| Dictionary found | "This password exists in known breach databases — cracked instantly" | "Avoid real words entirely. Use a random passphrase or generated password" |
| Rule-based found | "A simple transformation of a common word — still crackable" | "Don't rely on substitutions like @ for a or 0 for o — attackers know these" |
| Short length | "Password is too short — low keyspace" | "Use at least 12 characters" |
| No symbols | "Missing symbols reduces keyspace significantly" | "Add symbols like !@#$ anywhere in the password" |
| Keyboard walk | "Contains keyboard pattern — first thing attackers try" | "Avoid sequences like qwerty or 12345" |
| Predictable structure | "Word + numbers structure is extremely common" | "Don't just capitalize the first letter and add numbers at the end" |
| Low entropy | "Password is too predictable mathematically" | "Increase length and use all character types" |

---

## 6. visualization.py — Visualization Module

**Purpose:** Present everything visually in the terminal and save a chart to file.

**Inputs:** `final_score`, `attack_result`

---

### Visual 1 — Strength Meter (Terminal)

ASCII progress bar showing total score out of 100, color coded via `rich`:

```
Strength  [████████░░░░░░░░░░░░]  42/100  WEAK
```

| Score Range | Color |
|---|---|
| 0–25 | Red |
| 26–50 | Orange |
| 51–75 | Yellow |
| 76–90 | Green |
| 91–100 | Bright Green |

---

### Visual 2 — Pillar Breakdown (Terminal)

Four bars showing each pillar score:

```
Composition       [████████████░░░░░░░░]  14/20
Unpredictability  [████░░░░░░░░░░░░░░░░]   8/20
Attack Resistance [██░░░░░░░░░░░░░░░░░░]  15/45
Red Flags         [████████████████░░░░]  12/15
```

---

### Visual 3 — Attack Simulation Log (Terminal)

Step-by-step display of what each attack attempted:

```
ATTACK SIMULATION LOG
─────────────────────────────────────────────────
[Dictionary Attack]
  ✗ Not found in Tier 1 (top 1000)
  ✗ Not found in Tier 2 (rockyou 100k)
  ✓ FOUND in Tier 3 — matched: "password"

[Rule-based Attack]
  Base word   : "password"
  Rule applied: L33tspeak (R5)
  Mutated form: "p@ssw0rd"
  ✓ MATCH FOUND

[Brute-force Estimate]
  Charset detected : lowercase + digits (36 chars)
  Keyspace         : 36^9 = 101,559,956,668,416
  Estimated time   : 2 hours 49 minutes
─────────────────────────────────────────────────
```

---

### Visual 4 — Crack Time Bar Chart (matplotlib → PNG)

Horizontal bar chart comparing estimated crack time across all three attacks.

- **X axis:** Time (log scale — ranges are too large for linear)
- **Y axis:** Attack type
- **Bars:** Color coded by severity
- **Saved to:** `output/report.png`
- Displayed inline if terminal supports it

---

### Visual 5 — Summary Report (Terminal)

Final printable block:

```
══════════════════════════════════════════════
           PASSWORD ANALYSIS REPORT
══════════════════════════════════════════════
Password Length    : 9 characters
Character Types    : lowercase, digits
Entropy            : 46.3 bits
Overall Score      : 42 / 100
Classification     : WEAK

WEAKNESSES DETECTED:
  • Found in breach database
  • L33tspeak substitution detected
  • Predictable structure (word + numbers)

SUGGESTIONS:
  • Use at least 12 characters
  • Avoid common word substitutions
  • Add uppercase letters and symbols
══════════════════════════════════════════════
```

---

## 7. utils.py — Shared Helpers

Functions used across multiple modules. Everything shared lives here so no module imports from another module.

| Function | Purpose |
|---|---|
| `normalize(password)` | Lowercase + strip whitespace |
| `load_wordlist(path)` | Read file, return list of strings |
| `seconds_to_readable(seconds)` | Convert float to human time string |
| `apply_leet(word)` | Apply l33tspeak substitution map to a string |

---

## 8. Scoring System — Full Breakdown

### Why This Weight Distribution?

| Pillar | Weight | Reasoning |
|---|---|---|
| Composition | 20% | Foundation — but a long, complex password can still be cracked |
| Unpredictability | 20% | Structural randomness matters, but overlaps with composition |
| Attack Resistance | 45% | The core thesis of the project — real-world survival |
| Red Flags | 15% | Penalty layer for human-predictable patterns |

### Score → Classification Table

| Score | Classification | Meaning |
|---|---|---|
| 0–25 | Very Weak | Cracked in seconds by any method |
| 26–50 | Weak | Cracked quickly by at least one method |
| 51–75 | Moderate | Survives simple attacks but vulnerable to advanced ones |
| 76–90 | Strong | Resists most attacks; brute-force would take significant time |
| 91–100 | Very Strong | Resists all simulated attacks; brute-force infeasible |

---

## 9. requirements.txt

```
rich
matplotlib
```

Two dependencies only. Everything else is Python standard library.

- **rich** — Terminal visuals, colors, progress bars, formatted panels
- **matplotlib** — Crack time bar chart saved as PNG

---

## 10. README — Study Guide Structure

Each section of the README maps to one module and includes:

1. What the module does in plain English
2. The cybersecurity concept behind it
3. Three sample supervisor questions with model answers
4. How to run that part in isolation for testing

### Sample Q&A Per Module

**Analysis Engine**
> Q: Why do you calculate entropy?
> A: Entropy measures unpredictability. Higher entropy means more possible combinations, making the password harder to crack by any method.

**Attack Simulation**
> Q: Why simulate attacks instead of just rating the password?
> A: A password can look strong but still exist in a breach database. Simulating real attack techniques exposes vulnerabilities that a simple rating system would miss.

**Scoring Engine**
> Q: Why does attack resistance carry the most weight in the score?
> A: Because the purpose of a password is to resist being cracked. A password that fails under a real attack is weak regardless of how complex it appears.

**Visualization**
> Q: Why use a log scale on the crack time chart?
> A: Crack time ranges from milliseconds to millions of years depending on password strength. A linear scale would make most bars invisible. Log scale makes all values comparable.

---

## 11. Data Flow — Full Picture

```
User Input (password)
        ↓
    main.py
        ↓
  analysis.py
        ↓
  analysis_result
  {length, charset, entropy, patterns}
        ↓
    main.py
        ↓
   attacks.py ←── receives password + analysis_result
        ↓
  attack_result
  {dictionary, rule_based, brute_force}
        ↓
    main.py
        ↓
   scoring.py ←── receives analysis_result + attack_result
        ↓
   final_score
   {pillar_scores, total, classification, weaknesses, suggestions}
        ↓
    main.py
        ↓
 visualization.py ←── receives final_score + attack_result
        ↓
  Terminal output + output/report.png
```

---

*Blueprint version 1.0 — Password Security Analyzer with Attack Simulation*
