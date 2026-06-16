# Password Security Analyzer — Study Guide

## Project Structure

```
├── main.py            # Entry point — CLI handler, orchestrates all modules
├── analysis.py        # Module 1: Analyzes password composition & patterns
├── attacks.py         # Module 2: Simulates 3 attack types
├── scoring.py         # Module 3: Calculates score + generates feedback
├── visualization.py   # Module 4: Renders terminal output + saves chart
├── utils.py           # Shared helpers (no project logic)
├── wordlists/         # RockYou subset wordlists (Tier 1-3)
├── output/            # Generated charts & reports
├── requirements.txt   # Dependencies: rich, matplotlib
├── docs/              # Documentation
└── README.md
```

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Module-by-Module Guide

---

### Module 1: Analysis Engine (`analysis.py`)

**What it does:** Examines the password's raw properties before any attack runs.

**Cybersecurity concept:** *Password entropy* — a mathematical measure of unpredictability based on Claude Shannon's information theory. Higher entropy = harder to crack.

**Key functions:**

| Function | What it measures | Why it matters |
|---|---|---|
| `get_length()` | Character count | Longer passwords have exponentially more combinations |
| `detect_charset()` | Which character types are used | More types = larger search space for brute-force |
| `calculate_entropy()` | Bits of unpredictability | Gold-standard measure of password strength |
| `detect_patterns()` | Keyboard walks, repeats, sequences | Humans are predictable — attackers exploit this |

**Sample supervisor Q&A:**

> **Q:** Why do you calculate entropy using `log2`?
> **A:** Entropy is measured in bits. Each bit represents a binary choice (0 or 1). `log2` converts character set size into the number of bits needed to represent each character. This is standard information theory — every bit doubles the number of possible passwords an attacker must try.

> **Q:** Why does pattern detection matter if you already calculate entropy?
> **A:** Entropy treats all characters as equally random, but humans don't create random passwords. "qwerty123" has 10 characters with symbols and digits — its entropy looks decent. But pattern detection catches that it's a keyboard walk + sequential numbers, which attackers check first.

> **Q:** Could this module be extended?
> **A:** Yes — we could add date detection (e.g., "1992"), common name checking, or personal info patterns. The architecture supports adding new pattern checks without changing other modules.

---

### Module 2: Attack Simulation (`attacks.py`)

**What it does:** Simulates three techniques real attackers use to crack passwords.

**Cybersecurity concept:** *Offensive security* — understanding attack methods is essential for building defenses. "Know thy enemy."

**The three attacks:**

| Attack | Method | Real-world equivalence |
|---|---|---|
| Dictionary | Checks password against 500K known passwords | RockYou breach (14M passwords) — most common passwords |
| Rule-based | Applies 22 mutation rules to dictionary words | Hashcat rule engine — what real crackers use |
| Brute-force | Calculates time to try ALL possible combinations | GPU cluster (10 billion guesses/sec) |

**Key formula:** `Keyspace = charset_size ^ password_length`; `Crack time = Keyspace / guesses_per_second`

**Sample supervisor Q&A:**

> **Q:** Why simulate three attacks instead of just rating the password?
> **A:** Each attack reveals different weaknesses. A password can survive dictionary lookup (it's unique) but still be weak against brute-force because it's short. Another password might be long but contain a dictionary word with l33t substitutions, which rule-based cracking will find. Three attacks give a complete picture.

> **Q:** Why assume 10 billion guesses per second?
> **A:** This represents a modern multi-GPU setup (e.g., 8× RTX 4090) cracking NTLM hashes. It's realistic for a determined attacker with moderate resources. Government agencies would have much faster hardware, but 10 billion/sec is a defensible baseline for academic work.

> **Q:** Does the rule-based attack test ALL possible mutations?
> **A:** No — we test 22 common rules from Hashcat's rule engine. A real attacker would use thousands of rules. We chose the most common ones (capitalization, number appending, l33tspeak) that cover ~80% of user mutation patterns. This balances accuracy with performance.

---

### Module 3: Scoring Engine (`scoring.py`)

**What it does:** Combines analysis + attack results into a 0–100 score with specific feedback.

**Scoring pillars:** Attack Resistance (45 pts — the core thesis), Composition (20 pts), Unpredictability (20 pts), Red Flags (15 pts).

**Classification:** 0–25 Very Weak → 26–50 Weak → 51–75 Moderate → 76–90 Strong → 91–100 Very Strong

**Sample supervisor Q&A:**

> **Q:** Why does attack resistance carry the most weight (45%)?
> **A:** Because the only true test of a password is whether it survives an actual attack. A password can look mathematically strong (high entropy, good composition) but still exist in a breach database — making it trivially crackable. Attack resistance is the real-world validation.

> **Q:** How do you ensure the scoring is not arbitrary?
> **A:** Each pillar maps to a measurable cybersecurity principle. Composition = NIST password guidelines (length + complexity). Unpredictability = Shannon entropy (information theory). Attack resistance = empirical crackability (real attack simulation). Red flags = common pattern penalties from password cracking literature.

> **Q:** Could two different weak passwords get the same score?
> **A:** Yes — but they'll have different weakness lists and suggestions. Two passwords scoring 40/100 might fail for different reasons (one is dictionary-found, the other has low entropy). The score is the summary; the feedback is the actionable part.

---

### Module 4: Visualization (`visualization.py`)

**What it does:** Presents results visually in the terminal and saves a crack-time chart.

**Outputs:** Strength meter (progress bar), pillar breakdown, attack simulation log, summary report, crack-time bar chart (PNG).

**Sample supervisor Q&A:**

> **Q:** Why use a log scale on the crack time chart?
> **A:** Crack times range from milliseconds (for a dictionary match) to millions of years (for a strong password). A linear scale would make the fast bars invisible and the slow ones off the chart. Log scale lets you compare all values proportionally.

> **Q:** Could the visualization be web-based instead of CLI?
> **A:** Yes — the modular architecture makes this easy. Replace `visualization.py` with a Flask/Django view that receives the same data dictionaries. The data format wouldn't change — only the rendering layer.

---

## How Each Module Connects

```
User Input (password)
        ↓
    main.py          ← orchestrates the pipeline
        ↓
  analysis.py        ← pure observation (no attacks needed)
  Returns: {length, charset, entropy, patterns}
        ↓
   attacks.py        ← receives password + charset_size
  Returns: {dictionary, rule_based, brute_force}
        ↓
   scoring.py        ← receives analysis + attack results
  Returns: {pillar_scores, total, classification, weaknesses, suggestions}
        ↓
 visualization.py    ← receives everything, renders output
  Returns: terminal display + output/report.png
```

## Running Tests in Isolation

Each module can be tested independently:

```python
# Test analysis alone
python3 -c "
from analysis import analyze
result = analyze('MyPassword123')
print(result)
"

# Test attacks alone
python3 -c "
from attacks import simulate_attacks
result = simulate_attacks('password123', 36)
print(result['dictionary'])
print(result['brute_force']['crack_time_readable'])
"
```

## Dependencies

| Library | Purpose |
|---|---|
| `rich` | Terminal coloring, progress bars, tables, panels |
| `matplotlib` | Crack-time bar chart saved as PNG |

Everything else is Python standard library (math, os, getpass, etc.).

## Wordlist Source

Wordlists are extracted from the RockYou breach dataset (14.3 million real passwords), stored at `/usr/share/wordlists/rockyou.txt.gz` on Kali Linux. The project uses three tiered subsets:

| Tier | Size | Use |
|---|---|---|
| Tier 1 | 1,000 entries | Fast initial check |
| Tier 2 | 100,000 entries | Broad dictionary coverage |
| Tier 3 | 500,000 entries | Deep extended check |
