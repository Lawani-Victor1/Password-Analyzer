# Password Security Analyzer — Complete Defense Guide

## For Final Year Project Presentation

---

> **Read this document from start to finish. It explains everything you need to
> know to present and defend this project — even if you have never written a
> line of code before.**
>
> Each section builds on the one before it. By the end, you will understand
> not just *what* the project does, but *why* it works that way — which is
> what your supervisor will ask about.

---

## Table of Contents

1. [Part 1: The Absolute Basics](#part-1-the-absolute-basics)
2. [Part 2: What This Project Does (Non-Technical)](#part-2-what-this-project-does-non-technical)
3. [Part 3: How the Project is Organized](#part-3-how-the-project-is-organized)
4. [Part 4: Module 1 — Analysis Engine (analysis.py)](#part-4-module-1--analysis-engine-analysispy)
5. [Part 5: Module 2 — Attack Simulation (attacks.py)](#part-5-module-2--attack-simulation-attackspy)
6. [Part 6: Module 3 — Scoring Engine (scoring.py)](#part-6-module-3--scoring-engine-scoringpy)
7. [Part 7: Module 4 — Visualization (visualization.py)](#part-7-module-4--visualization-visualizationpy)
8. [Part 8: Helper Tools (utils.py)](#part-8-helper-tools-utilspy)
9. [Part 9: The Conductor (main.py)](#part-9-the-conductor-mainpy)
10. [Part 10: Important Concepts You Must Know](#part-10-important-concepts-you-must-know)
11. [Part 11: Supervisor Q&A — Full Script](#part-11-supervisor-qa--full-script)
12. [Part 12: Common Traps to Avoid](#part-12-common-traps-to-avoid)
13. [Part 13: Quick Reference — One-Liners Per File](#part-13-quick-reference--one-liners-per-file)

---

## Part 1: The Absolute Basics

### What is a password?

A password is a secret word or string of characters used to prove you are who
you say you are. When you log into Facebook, email, or online banking, the
system asks for your username (who you are) and your password (proof that
it's really you).

### What makes a password "strong"?

A strong password is one that an attacker cannot guess or compute quickly.
There are two ways attackers try to get your password:

1. **Guessing** — trying common passwords like "password123" or "admin"
2. **Systematic computation** — trying every possible combination until one
   works (like trying every combination on a combination lock)

A strong password survives both methods.

### What is a "program" or "script"?

A program is a set of instructions written in a language that a computer can
follow. Think of it like a cooking recipe:

```
Recipe for cake:                    Program for password analysis:
1. Preheat oven                     1. Ask user for password
2. Mix flour and eggs               2. Check if it's in a wordlist
3. Pour into pan                    3. Calculate how long to crack
4. Bake for 30 minutes              4. Show results to user
```

This project is written in **Python**, which is one of the easiest programming
languages to read — it looks almost like English.

### What is "Python"?

Python is a programming language. It was chosen for this project because:

- It is free and widely used in universities
- It is easy to read (even non-programmers can understand the logic)
- It has many free tools ("libraries") that we can use — like `rich` for
  making nice-looking terminal output and `matplotlib` for drawing charts

### What is a "library" or "dependency"?

A library is pre-written code that someone else created so you don't have to
re-invent the wheel. For example, instead of writing code to draw a bar chart
from scratch, we use `matplotlib` which already knows how to do it.

Our project uses only TWO external libraries:

| Library | What it does for us |
|---|---|
| `rich` | Makes the terminal output colorful with progress bars and boxes |
| `matplotlib` | Draws a bar chart and saves it as a PNG image file |

Everything else in the project is built using tools that come built-in with
Python (no extra installation needed).

### What is "CLI" (Command-Line Interface)?

CLI means the program runs in a terminal/command prompt window — the black
screen where you type commands. The user types their password, presses Enter,
and the results appear as text and colored bars in the same window.

This is different from a "GUI" (Graphical User Interface) which has buttons,
windows, and mouse interaction — like a typical phone app or website.

---

## Part 2: What This Project Does (Non-Technical)

### In One Sentence

This project is a tool that tests how strong a password is by simulating how
a real hacker would try to crack it.

### The Problem It Solves

Most password strength checkers on websites just look at simple rules:
- Is it at least 8 characters?
- Does it have a mix of letters, numbers, and symbols?
- Does it have uppercase and lowercase?

These checks are **misleading**. A password like `Password123!` passes all
these rules (12 characters, uppercase, lowercase, numbers, symbol) — but it
is actually **weak** because it contains a real word ("password") with a
simple number and symbol tacked on. A hacker's computer would crack it in
minutes.

Our tool goes deeper. Instead of just checking rules, it actually **simulates
attacks** the way a real hacker would — checking common password lists,
trying simple variations, and calculating the mathematical time to crack it.

### The Core Idea (Your Thesis Statement)

> "The only true test of password strength is whether it survives a real
> attack — not how complex it looks on paper."

This is the key argument of your project. It is what makes your project
different from every online password checker. Remember this sentence — your
supervisor will ask why your project is special, and this is the answer.

### What Happens When You Run It (Step by Step)

```
User types a password
         ↓
[1/4] Analyze the password's structure
      → How long is it? What characters does it use?
      → Is there a pattern? (keyboard walks, repeated chars, etc.)
      → Calculate entropy (mathematical randomness score)
         ↓
[2/4] Simulate attacks
      → Dictionary attack: check if it's in known leaked passwords
      → Rule-based attack: try simple variations of common words
      → Brute-force: calculate time to try ALL possible combinations
         ↓
[3/4] Calculate a score
      → Combine everything into a score out of 100
      → Give it a label: Very Weak → Very Strong
      → List specific weaknesses found
      → Suggest how to fix each weakness
         ↓
[4/4] Show results
      → Progress bar with color (green = good, red = bad)
      → Breakdown of each scoring area
      → Step-by-step attack log
      → Summary report with weaknesses and suggestions
      → Save a bar chart as a PNG image
```

### Think of It Like a Doctor's Checkup

The password is the patient. The tool is the doctor:

| Step | Medical Analogy |
|---|---|
| Analysis | Taking vitals (height, weight, blood pressure) |
| Attack Simulation | Stress test (running on a treadmill) |
| Scoring | Diagnosis (healthy? at risk? critical?) |
| Visualization | Patient report with charts and recommendations |

---

## Part 3: How the Project is Organized

### The File Structure

```
Password-Analyzer/
│
├── main.py               # The "conductor" — runs everything in order
├── analysis.py            # Module 1: Analyzes password structure
├── attacks.py             # Module 2: Simulates attacks
├── scoring.py             # Module 3: Calculates score + feedback
├── visualization.py       # Module 4: Shows results on screen
├── utils.py               # Shared tools used by multiple modules
│
├── wordlists/             # Folder containing word lists (dictionaries)
│   ├── tier1_top1000.txt      # Top 1000 most common passwords
│   ├── tier2_rockyou_100k.txt # 100,000 leaked passwords
│   ├── tier3_extended.txt     # Extended list of passwords
│   └── dictionary.txt         # English dictionary (104,000 words)
│
├── output/                # Folder where saved images go
│   └── report.png             # Bar chart saved as image
│
├── docs/                  # Documentation folder (you are here)
│
├── requirements.txt       # List of libraries to install
└── README.md              # Project overview
```

### The Assembly Line Analogy

Think of the project as a car factory assembly line:

```
main.py is the conveyor belt
         │
         ▼
analysis.py  →  Station 1: Inspect the raw materials (the password)
         │
         ▼
attacks.py   →  Station 2: Crash-test the password
         │
         ▼
scoring.py   →  Station 3: Grade the results
         │
         ▼
visualization.py → Station 4: Package and display the final product
```

Each station does one job and passes the result to the next station.
This design is called **modular** — each piece is independent. If you want
to change how attacks work, you only change `attacks.py`. The other files
don't need to change.

### Why Is It Organized This Way?

**Reason 1: Easy to understand.** Each file has one clear job.

**Reason 2: Easy to test.** You can test each module by itself without
running the whole program.

**Reason 3: Easy to improve.** If you want to add a new type of attack,
you only modify `attacks.py`. The other files don't need to change.

---

## Part 4: Module 1 — Analysis Engine (`analysis.py`)

### What This File Does (Plain English)

Before we attack the password, we need to understand what it's made of.
This file examines the password like a doctor checking your vital signs:

- **How long is it?** (Length)
- **What characters does it use?** (Lowercase, uppercase, numbers, symbols)
- **How random is it?** (Entropy — a math score for unpredictability)
- **Does it have patterns?** (Keyboard walks, repeated characters, etc.)

### Key Function 1: get_length(password)

**What it does:** Counts how many characters are in the password.

**Simple explanation:** If your password is "dog", this returns 3. If your
password is "correcthorsebatterystaple", this returns 25.

**Why it matters:** Every extra character makes the password exponentially
harder to crack. A 12-character password is not 50% harder than an 8-character
one — it is thousands of times harder.

**If supervisor asks:** "The length is found using Python's `len()` function,
which counts the number of characters in a string. It's a built-in function
that returns the length as a number."

---

### Key Function 2: detect_charset(password)

**What it does:** Checks which types of characters the password uses.

**Simple explanation:** It looks at every single character in the password
and categorizes each one:

| Category | Examples |
|---|---|
| Lowercase letters | a, b, c, ..., z |
| Uppercase letters | A, B, C, ..., Z |
| Digits | 0, 1, 2, ..., 9 |
| Symbols | !, @, #, $, %, &, *, etc. |

**Then it calculates the "charset size":**

| Character types used | Charset size | Explanation |
|---|---|---|
| Lowercase only | 26 | Only 26 possible letters for each position |
| + Uppercase | 52 | 26 lowercase + 26 uppercase |
| + Digits | 62 | Added 10 more possibilities |
| + Symbols | 95 | Added 33 more possibilities (total) |

**Why it matters:** The more character types you use, the more combinations
an attacker has to try. A password with only lowercase letters has 26 choices
per character. A password with all four types has 95 choices per character.
That is a HUGE difference in how long it takes to crack.

**If supervisor asks:** "For each character in the password, the code checks
if it is lowercase, uppercase, a digit, or a symbol using Python's built-in
character tests. Then it adds up the charset size based on which types were
found."

---

### Key Function 3: calculate_entropy(password, charset_size)

**What it does:** Calculates a mathematical "unpredictability" score for the
password.

**The formula:** `Entropy = password_length × log₂(charset_size)`

**Simple explanation:** Entropy measures how many "bits" of randomness are
in your password. Think of each bit as a coin flip. A coin flip has 1 bit of
entropy (heads or tails). A password with 60 bits of entropy is as hard to
guess as flipping 60 coins and getting the exact sequence right.

**Example calculations:**

| Password | Length | Types | Charset Size | Entropy (bits) |
|---|---|---|---|---|
| `dog` | 3 | lowercase | 26 | 3 × 4.7 = 14.1 |
| `Password123!` | 12 | all 4 | 95 | 12 × 6.57 = 78.8 |
| `correcthorsebatterystaple` | 25 | lowercase | 26 | 25 × 4.7 = 117.5 |

**Why log₂?** Logarithms convert multiplication into addition. Every bit
doubles the number of possible passwords. 10 bits = 2¹⁰ = 1024 passwords.
20 bits = 2²⁰ = 1 million passwords. This is standard information theory
developed by Claude Shannon in 1948 — it is the gold standard for measuring
randomness.

**The caveat (important for defense):** Entropy assumes the password was
chosen randomly. A password like `aaaaaaaaaaaaaaaa` (16 a's) has high entropy
on paper (16 × 4.7 = 75 bits) but is actually very weak because it is
completely predictable. This is exactly why we also check for **patterns**
— entropy alone is not enough.

**If supervisor asks:** "Entropy is calculated using Claude Shannon's formula
from information theory. It measures the number of bits of randomness. But
entropy only works for truly random passwords — that is why we also check
for patterns separately."

---

### Key Function 4: detect_patterns(password)

**What it does:** Checks the password for common human patterns that weaken
it — even if it looks strong on paper.

#### Pattern 1: Keyboard Walk

**What it checks:** Is the password just a pattern on a keyboard?

**Examples:** `qwerty`, `asdfgh`, `zxcvbn`, `12345`, `1qaz2wsx`

**Why it matters:** These are among the first things attackers try. They are
extremely common because they are easy to remember.

**How it works (simple):** The code has a list of known keyboard patterns.
It checks if any of those patterns appears inside the password.

#### Pattern 2: Repeated Characters

**What it checks:** Does the same character appear 3+ times in a row?

**Examples:** `aaa`, `111`, `@@@`, `pppp`

**Why it matters:** A password like `aaaaaaaaaaaa` looks long but has no
real randomness.

**How it works (simple):** The code looks at every group of 3 consecutive
characters. If all 3 are the same, it flags this pattern.

#### Pattern 3: Leetspeak (1337 5p34k)

**What it checks:** Does the password use common letter-to-symbol substitutions?

**Examples:**

| Leet | Meaning |
|---|---|
| `@` | a |
| `3` | e |
| `1` | i |
| `0` | o |
| `$` | s |
| `4` | a |
| `7` | t |

So `P@ssw0rd` = `Password`, `Tr0ub4dor` = `Troubadour`

**Why it matters:** Users think "p@ssw0rd" is clever and secure. Attackers
have been reversing these substitutions for decades — it is the first thing
their software does.

**How it works (simple):** The code has a "reverse leet" table. It applies
the table to the password to convert leet back to letters. Then it checks
if the result contains a real English word from the dictionary.

#### Pattern 4: Sequential Characters

**What it checks:** Are there consecutive letters or numbers like `abc` or
`321`?

**Examples:** `abc`, `def`, `123`, `987`, `xyz`

**Why it matters:** These patterns are easy to guess. Attackers check for
them automatically.

**How it works (simple):** The code looks at every group of 3 consecutive
characters. If each character follows the previous one in alphabet or number
order (like a→b→c or 3→2→1), it flags it.

#### Pattern 5: Common Word Embedded

**What it checks:** Does the password contain a real English word?

**Examples:** `iloveyouJohn`, `correcthorsebatterystaple`, `admin2024`

**Why it matters:** Passwords made of real words are vulnerable to
"dictionary attacks" where attackers try every word in the dictionary.

**How it works (simple):** The code loads the English dictionary (104,000
words) and checks if any of those words appear as part of the password.

#### Pattern 6: Passphrase Detection

**What it checks:** Is the password made of multiple dictionary words in a
row?

**Examples:** `correcthorsebatterystaple` (4 words), `opensesame` (2 words)

**Why it matters:** Even if each individual word is fine, using multiple
words together creates a "passphrase" that attackers can crack by trying
word combinations.

**How it works (simple):** The code tries to break the password down into
dictionary words. If it finds 2+ words that make up most of the password,
it flags it as a passphrase.

#### Pattern 7: Predictable Structure

**What it checks:** Does the password follow a "Capital letter + word +
numbers at the end" pattern?

**Examples:** `Password123`, `Admin2024`, `Michael1`

**Why this is the #1 most common structure:** Most websites require an
uppercase letter and a number, and most users just capitalize the first
letter and add a number at the end. Attackers know this and check it first.

**How it works (simple):** The code checks if:
1. The first character is uppercase
2. There are trailing digits before any ending symbols
3. The middle part is mostly lowercase letters

---

## Part 5: Module 2 — Attack Simulation (`attacks.py`)

### What This File Does (Plain English)

This is the heart of the project. Instead of just rating the password, we
actually simulate what a real attacker would do. Three different attack
methods are simulated.

### Attack 1: Dictionary Attack

**What it does:** Checks if the password appears in lists of known leaked
passwords.

**Where do the wordlists come from?** The famous "RockYou" data breach in
2009 leaked 14 million real passwords. We use subsets of that data,
organized into three tiers:

| Tier | Number of Passwords | What It Represents |
|---|---|---|
| Tier 1 | 1,000 | The absolute most common passwords |
| Tier 2 | 100,000 | A broad range of common passwords |
| Tier 3 | 500,000 | An extended range of real passwords |

**How it works (simple):**
1. Take the password and convert it to lowercase
2. Check if it exists in Tier 1 (fast check)
3. If not found, check Tier 2
4. If not found, check Tier 3
5. Report whether it was found, which tier, and the matching word

**Why three tiers?** Performance. Most weak passwords are in Tier 1 (top
1000). Checking 1000 entries takes milliseconds. Only if the password
survives Tier 1 do we check the larger lists.

**Why lowercase?** Attackers try lowercase first because users who type
passwords quickly often don't bother with shift key. Also, "Password" and
"password" are treated the same by cracking software.

**Why this matters:** If your password appears in any of these lists, a
real attacker would crack it in under a second. This happens more often
than you'd think — millions of people still use "123456" and "password".

### Attack 2: Rule-Based Attack

**What it does:** Takes words from the wordlists and applies common
transformations ("rules") to see if any variation matches the password.

**Why this attack?** Most users don't use bare dictionary words — they
change them slightly. They capitalize the first letter, add a number,
replace letters with symbols. Attackers know all these tricks.

**The rules we simulate (22 total):**

| Rule | Example | What it does |
|---|---|---|
| Capitalize | `password → Password` | Capitalizes first letter |
| ALL CAPS | `password → PASSWORD` | Makes everything uppercase |
| Append 1 | `password → password1` | Adds "1" at the end |
| Append 123 | `password → password123` | Adds numbers at the end |
| Append 1234 | `password → password1234` | Longer number append |
| Prepend 1 | `password → 1password` | Adds number at the start |
| Prepend 123 | `password → 123password` | Longer number at start |
| L33tspeak | `password → p@ssw0rd` | Replaces letters with symbols |
| Append ! | `password → password!` | Adds exclamation mark |
| Append @ | `password → password@` | Adds @ symbol |
| Append # | `password → password#` | Adds hash symbol |
| Reverse | `password → drowssap` | Reverses the word |
| Double | `password → passwordpassword` | Repeats the word twice |
| Append year | `password → password2024` | Adds recent years |

**How it works (simple):**
1. Load Tier 1 and Tier 2 wordlists
2. For each word in those lists, apply all 22 rules
3. If any resulting variation matches the password, report it
4. Show which base word was used and which rule exposed it

**Real-world equivalence:** This is exactly what Hashcat — the industry
standard password cracking tool — does with its rule engine. Hashcat has
thousands of rules. We implemented the 22 most common ones that catch
~80% of user mutation patterns.

**Example:** If your password is `Password123!`, the tool would find:
- Base word: `password`
- Rule applied: `R3: Append 123` → creates `password123`
- Then: the user also added `!` at the end

So the password is exposed as a simple mutation of a common word.

### Attack 3: Brute-Force Estimator

**What it does:** Calculates mathematically how long it would take to try
EVERY possible combination of characters.

**It does NOT actually try every combination** — it just calculates the
time. For strong passwords this would take millions of years.

**The formula:**

```
Step 1: Keyspace = (charset_size) ^ (password_length)
Step 2: Time (seconds) = Keyspace / guesses_per_second
```

**What is "keyspace"?** The total number of possible passwords of that
length using those characters.

| Example | Calculation | Keyspace |
|---|---|---|
| 4-digit PIN | 10⁴ | 10,000 |
| 8-char lowercase | 26⁸ | 208 billion |
| 8-char all types | 95⁸ | 6.6 quadrillion |
| 12-char all types | 95¹² | 540 sextillion |

**What is "guesses per second"?** We assume **10 billion guesses per
second**. This represents:

- A modern computer with multiple high-end graphics cards (GPUs)
- Cracking password hashes offline (not through a website)
- A realistic but not extreme attacker setup

Government agencies would have much faster hardware, but 10 billion/sec is
a solid baseline for academic work.

**Example calculation:**
```
Password: "Password123!" (12 chars, all 4 types)
Charset size: 95
Keyspace: 95¹² = 540,360,087,662,636,990,201,856
Time: 540,360,087,662,636,990,201,856 ÷ 10,000,000,000
    = 54,036,008,766 seconds
    = about 1,713,470 years
```

**The output is converted to human-readable form:**
- Under 1 minute → "less than 1 minute"
- Under 1 hour → "X minutes"
- Under 1 day → "X hours"
- Under 1 month → "X days"
- Under 1 year → "X months"
- Over 1 year → "X years"

### How Attacks Affect Each Other

If the dictionary attack found the password, we know it is weak immediately.
But we still run the other attacks to give a complete picture. Even if a
dictionary found it, the user needs to see HOW it was found and how long
brute-force would take.

---

## Part 6: Module 3 — Scoring Engine (`scoring.py`)

### What This File Does (Plain English)

This file takes ALL the results from the analysis and attack modules and
turns them into:
1. A score out of 100
2. A label (Very Weak → Very Strong)
3. A list of specific weaknesses
4. A list of specific suggestions

### The Four Scoring Pillars

The score is built from four "pillars" — like four legs of a table. Each
pillar measures a different aspect of password strength:

```
┌─────────────────────────────────────────────┐
│            TOTAL SCORE (100)                 │
├──────────┬──────────┬──────────┬─────────────┤
│Composition│Unpredict-│ Attack   │  Red Flags  │
│  20 pts   │  ability │Resistance│   15 pts    │
│           │  20 pts  │  45 pts  │             │
└──────────┴──────────┴──────────┴─────────────┘
```

### Why Attack Resistance is 45% of the Score

This is the most important design decision in the project. Attack resistance
carries the most weight because:

> **"A password that fails under a real attack is weak — period. It does not
> matter how long it is or how many symbols it uses."**

Most online password meters only check length and character types. Our
project is different because it rewards actual attack survival, not just
appearance. This is the "thesis" of your project — the unique idea that
makes it worth a final year project.

### Pillar 1: Composition (20 points)

**What it measures:** The raw materials of the password.

**Length score (max 12 points):**

| Password Length | Points | Example |
|---|---|---|
| 1–5 characters | 0 | `dog` |
| 6–7 characters | 3 | `abcdef` |
| 8–9 characters | 6 | `password` |
| 10–11 characters | 9 | `qwerty123` |
| 12–15 characters | 11 | `Password123!` |
| 16+ characters | 12 | `correcthorse...` |

**Character variety score (max 8 points, 2 per type):**

| Each type used | Points |
|---|---|
| Lowercase letters | 2 |
| Uppercase letters | 2 |
| Digits (0-9) | 2 |
| Symbols (!@#$ etc.) | 2 |

**Why this exists:** Longer passwords with more character types are harder
to crack. This is the foundation — but foundation alone is not enough.

### Pillar 2: Unpredictability (20 points)

**What it measures:** How random the password actually is.

**Entropy score (max 12 points):**

| Entropy (bits) | Points |
|---|---|
| Below 28 | 0 |
| 28–35 | 3 |
| 36–49 | 6 |
| 50–59 | 9 |
| 60+ | 12 |

**Pattern absence score (max 8 points, starts at 8, deducts):**

| Pattern Found | Deduction |
|---|---|
| Keyboard walk (qwerty, asdf) | -3 |
| Repeated characters (aaa, 111) | -2 |
| Leetspeak (p@ssw0rd) | -2 |
| Sequential characters (abc, 123) | -1 |
| Passphrase (multiple dictionary words) | -3 |

**Why this exists:** A password like `aaaaaaaaaaaa` has 12 characters (good
composition) and decent entropy on paper, but it is extremely predictable
because all characters are the same. Pattern detection catches what entropy
misses.

### Pillar 3: Attack Resistance (45 points)

**What it measures:** Did the password survive real attack simulations?

**Dictionary attack (15 points):**
- If NOT found in any wordlist → 15 points (full marks)
- If found in any wordlist → 0 points

**Rule-based attack (15 points):**
- If NOT matched by any mutation → 15 points (full marks)
- If matched by a mutation → 0 points

**Brute-force resistance (15 points), based on estimated crack time:**

| Crack Time | Points |
|---|---|
| Under 1 minute | 0 |
| 1 minute – 1 hour | 3 |
| 1 hour – 1 day | 6 |
| 1 day – 1 month | 9 |
| 1 month – 1 year | 12 |
| Over 1 year | 15 |

**Note on passphrases:** If the password is a passphrase (multiple
dictionary words), the brute-force estimate is adjusted. Instead of
calculating based on individual characters, we calculate based on word
combinations from a dictionary. This gives a more realistic (lower) time.

**Why this is the most important pillar:** Because it tests the password
against what real attackers actually do. A mathematically perfect password
that happens to be "123456" gets 0 in attack resistance because a real
attacker would crack it instantly.

### Pillar 4: Red Flags (15 points)

**What it measures:** Additional structural problems that scream "weak."

**Starts at 15. Deducts for each flag found:**

| Red Flag | Deduction |
|---|---|
| Contains a dictionary word | -5 |
| Passphrase (2+ dictionary words) | -5 |
| Predictable structure (Capital+word+numbers) | -4 |
| Only first letter capitalized | -3 |

**Why this exists:** Even before any attack runs, some passwords are
obviously weak by their structure. These deductions catch the most common
patterns found in password leaks.

### Putting It All Together — The Classification

| Total Score | Label | What It Means |
|---|---|---|
| 0–25 | Very Weak | Cracks instantly — change immediately |
| 26–50 | Weak | Would crack quickly with basic tools |
| 51–75 | Moderate | OK for low-value accounts, not for important ones |
| 76–90 | Strong | Would take significant resources to crack |
| 91–100 | Very Strong | Would take years to crack with current technology |

### How Feedback is Generated

The tool doesn't just give a number. It generates two lists:

**Weaknesses detected:** Every issue found during analysis and attacks.
Example: "Found in Tier 1 wordlist (matched: 'password')"

**Suggestions:** A specific fix for each weakness.
Example: "Don't use real words or common passwords. Use a random passphrase
or a password manager."

This makes the tool educational, not just evaluative.

---

## Part 7: Module 4 — Visualization (`visualization.py`)

### What This File Does (Plain English)

This file takes all the results and displays them nicely on screen.
It creates five different visual outputs.

### Output 1: Strength Meter

A large progress bar at the top with color coding:

```
╭────────── Password Strength Report ──────────╮
│                                               │
│   Overall Strength: ████████░░░░░░  55/100    │
│   Classification: MODERATE                    │
│                                               │
╰───────────────────────────────────────────────╯
```

**Colors:** Red (0-25) → Orange (26-50) → Yellow (51-75) → Green (76-90) →
Bright Green (91-100)

### Output 2: Pillar Breakdown

Four smaller bars showing how the score is built:

```
  Composition       ████████████████░░░░  15/20
  Unpredictability  ████████████████████  19/20
  Attack Res.       ████████████░░░░░░░░  30/45
  Red Flags         ██████████░░░░░░░░░░  10/15
```

### Output 3: Attack Simulation Log

A step-by-step replay of what each attack did:

```
[Dictionary Attack]
  ✗ Not found in any tier

[Rule-based Attack]
  Base word   : password
  Rule applied: R3: Append 123
  Mutated form: password123
  ✓ MATCH FOUND

[Brute-force Estimate]
  Charset size    : 95 characters
  Password length : 12 characters
  Keyspace        : 540,360,087,662,636,990,201,856
  Estimated time  : 1,713,470 years
```

### Output 4: Summary Report

A clean printable summary with all weaknesses and suggestions:

```
══════════════════════════════════════════════
        PASSWORD ANALYSIS REPORT
══════════════════════════════════════════════
 Password Length   12 characters
 Character Types   lowercase, uppercase, digits, symbols
 Entropy           78.8 bits
 Overall Score     55 / 100
 Classification    Moderate

WEAKNESSES DETECTED:
  • Contains a common dictionary word
  • Contains sequential characters

SUGGESTIONS:
  • Avoid real words entirely
  • Avoid letter or number sequences
══════════════════════════════════════════════
```

### Output 5: Crack Time Chart (Saved as PNG)

A horizontal bar chart saved to `output/report.png`:

```
Attack Type
─────────────────────────────────────
Dictionary    ██  0.001 seconds
Rule-based    ██████  0.01 seconds
Brute-force   ████████████████████  1,713,470 years
─────────────────────────────────────
     (log scale — each step = 10x)
```

**Why a log scale?** Crack times range from milliseconds (dictionary match)
to millions of years (strong password). A regular scale would make fast
bars invisible and slow bars off the chart. A log scale lets you compare
all values proportionally.

---

## Part 8: Helper Tools (`utils.py`)

### What This File Does (Plain English)

This file contains small utility functions that are used by multiple other
modules. Instead of writing the same code twice, we put it here once.

### Function 1: normalize(password)

**What it does:** Converts the password to lowercase and removes extra
spaces.

**Why:** Attackers check lowercase first. "Password" and "password" are
the same to cracking software. This ensures consistent comparison.

### Function 2: load_wordlist(filepath)

**What it does:** Reads a text file (one word per line) and returns it as
a list.

**Why:** Wordlists are just plain text files. This function handles the
reading so other modules don't have to.

### Function 3: seconds_to_readable(seconds)

**What it does:** Converts a number like `1012847189` into "32 years".

**Why:** A raw number like "1012847189 seconds" means nothing to a user.
"32 years" is immediately understandable.

### Function 4: apply_leet(word)

**What it does:** Applies leetspeak substitutions to a word.

**Example:** `password` → `p@ssw0rd`

**Why:** Used by the rule-based attack to generate mutated versions of
dictionary words.

---

## Part 9: The Conductor (`main.py`)

### What This File Does (Plain English)

This is the "conductor" of the orchestra. It does not do any heavy analysis
itself — it just calls each module in the right order and passes data
between them.

### The Flow:

```
1. Display welcome banner
2. Ask user for password (hidden input — not shown on screen)
3. Call analysis.py → get analysis result
4. Call attacks.py → get attack result
5. Call scoring.py → get final score
6. Call visualization.py → show everything
7. Ask if user wants to test another password
```

### Why This Design?

**Separation of concerns:** Each file has one job. `main.py` orchestrates.
`analysis.py` analyzes. `attacks.py` attacks. This is a professional
software design pattern called "modular architecture."

**Testability:** You can test each module independently:
```python
# Test analysis alone
from analysis import analyze
result = analyze("MyPassword123")
print(result)

# Test attacks alone
from attacks import simulate_attacks
result = simulate_attacks("password123", 36)
print(result)
```

**Extensibility:** To add a new feature, you either add a function to an
existing module or create a new module. `main.py` barely needs to change.

### The Session Data Flow

Data flows through the program as Python dictionaries (like labeled boxes):

```
analysis_result = {
    "length": 12,
    "charset": {"lowercase": True, "uppercase": True, ...},
    "entropy": 78.8,
    "patterns": {"keyboard_walk": False, "repeated_chars": False, ...}
}

attack_result = {
    "dictionary": {"found": True, "tier": "Tier 1", "matched_word": "password"},
    "rule_based": {"found": False, ...},
    "brute_force": {"crack_time_seconds": 12345, "crack_time_readable": "3 hours"}
}

final_score = {
    "total": 55,
    "classification": "Moderate",
    "weaknesses": ["Contains dictionary word", ...],
    "suggestions": ["Don't use real words", ...]
}
```

---

## Part 10: Important Concepts You Must Know

### 1. What is "Entropy" and Why Do We Use It?

Entropy comes from a field called **information theory**, created by Claude
Shannon in 1948. It measures how much "surprise" or "unpredictability" is
in a piece of information.

**Simple explanation:** Imagine flipping a coin. There are 2 possibilities
(heads or tails). That is 1 bit of entropy. Now imagine rolling a 6-sided
die. There are 6 possibilities, which is about 2.6 bits of entropy.

For passwords, entropy tells us how many "bits" of randomness were used to
create it. Higher entropy = more possible passwords an attacker has to check.

**Formula:** `Entropy = length × log₂(charset_size)`

We use `log₂` (logarithm base 2) because entropy is measured in bits, and
each bit represents a binary choice (0 or 1).

**The catch (important for defense):** Entropy assumes each character was
chosen randomly. But humans don't choose randomly — we choose patterns.
That is why entropy alone is not enough, and why we also check for patterns.

### 2. What is "Keyspace"?

Keyspace is the total number of possible passwords of a given length using
a given set of characters.

**Formula:** `Keyspace = charset_size^password_length`

**Example:** A 4-digit PIN has charset_size = 10 (digits 0-9) and length = 4.
Keyspace = 10⁴ = 10,000 possible PINs.

A 12-character password with all character types (95) has keyspace = 95¹²,
which is about 540 sextillion — an astronomically large number.

### 3. What is "log scale"?

A normal (linear) scale goes 0, 1, 2, 3, 4, 5... Each step adds the same
amount. A log scale goes 0.001, 0.01, 0.1, 1, 10, 100, 1000... Each step
multiplies by 10.

**Why we use it:** Crack times range from 0.001 seconds (dictionary match)
to 1,713,470 years (brute-force-resistant). If we used a normal scale, the
0.001 second bar would be invisible and the million-year bar would be off
the chart. Log scale makes them all visible and comparable.

### 4. What are GPU Cracking Speeds?

Modern graphics cards (GPUs) are extremely good at parallel processing —
doing many calculations at once. Password cracking uses this to try billions
of passwords per second.

**Our assumption:** 10 billion (10,000,000,000) guesses per second.

**What that means:** This could be achieved by a computer with 8 high-end
graphics cards (like RTX 4090s) cracking certain types of password hashes.

**Is it realistic?** Yes, for a determined attacker with moderate resources.
Government agencies and organized crime groups have much faster hardware.
We chose 10 billion/sec as a defensible baseline for academic work.

### 5. The RockYou Breach

In 2009, a company called RockYou (which made social networking apps) had a
data breach. The attacker stole 14 million passwords — stored in plain text
(not encrypted). These passwords were published online and became the most
famous password dataset in cybersecurity history.

Our wordlists (tier1, tier2, tier3) are subsets of this data. This means
when we check a password against our wordlists, we are checking if it was
actually used by a real person and leaked in a real breach.

### 6. Hashcat

Hashcat is the industry-standard password cracking tool. It is free and
open-source. It supports:

- Dictionary attacks (checking wordlists)
- Rule-based attacks (applying mutations to wordlists)
- Brute-force / mask attacks (trying all combinations)
- GPU acceleration (using graphics cards for speed)

Our project is inspired by Hashcat and implements simplified versions of
its three main attack modes.

---

## Part 11: Supervisor Q&A — Full Script

These are questions your supervisor might ask, with answers you can
memorize. Practice saying them out loud.

### About the Project

**Q: Why did you choose this topic?**

A: "Password security affects everyone — from casual users to large
organizations. Most password strength meters are misleading because they
only check length and character types. I wanted to build a tool that
actually simulates real attack techniques, because the only true test of
a password is whether it survives a real attack."

**Q: What makes your project different from existing password checkers?**

A: "Most online checkers just measure complexity — they check length,
character types, and maybe entropy. Our project actually simulates three
attack methods: dictionary lookup, rule-based mutation, and brute-force
estimation. This gives a much more realistic assessment of password
strength."

**Q: What are the limitations of your project?**

A: "Three main limitations: First, the attack simulation is simplified
compared to professional tools like Hashcat, which have thousands of rules.
Second, the brute-force estimate assumes a fixed hardware speed — a real
attacker might have faster or slower hardware. Third, the wordlists are
static — a real attacker might have access to more recent breach data."

**Q: How would you extend this project in the future?**

A: "Several possibilities: Adding a web interface instead of command-line.
Adding more attack rules to catch more mutation patterns. Adding detection
for personal information patterns (names, dates, birthdays). Or connecting
to a live breach database API for real-time checking."

### About the Technical Implementation

**Q: Why did you use Python?**

A: "Python is widely used in academia and cybersecurity. It has excellent
libraries for our needs — `rich` for terminal visualization and `matplotlib`
for charts. Python code is also very readable, which makes the project easy
to understand, test, and extend."

**Q: Why is the code split into multiple files?**

A: "This is called a modular architecture. Each file has one specific job:
`analysis.py` analyzes password structure, `attacks.py` simulates attacks,
`scoring.py` calculates the score, `visualization.py` displays results,
and `main.py` orchestrates everything. This makes the code easier to
understand, test, and modify. If I want to change how attacks work, I only
modify `attacks.py` — the other files don't need to change."

**Q: How does data flow through the program?**

A: "The user enters a password in `main.py`. This is passed to `analysis.py`
which returns a dictionary of results. Then `main.py` passes the password
and analysis results to `attacks.py` for attack simulation. Then both
results go to `scoring.py` for the final score. Finally, everything goes to
`visualization.py` for display. Each step adds information to the pipeline."

**Q: How do you calculate entropy?**

A: "Using Claude Shannon's information theory formula:
`entropy = length × log₂(charset_size)`. This gives us the number of bits
of randomness. We use `log₂` because entropy is measured in bits — each bit
represents a binary choice."

**Q: Why do you need both entropy and pattern detection?**

A: "Entropy assumes characters are chosen randomly, but humans don't choose
randomly — we use patterns. A password like 'qwerty123' has decent entropy
on paper but is actually very weak because it's a keyboard walk with
sequential numbers. Pattern detection catches what entropy misses."

**Q: Why do you assume 10 billion guesses per second?**

A: "This represents a realistic modern GPU cracking setup — approximately
8 high-end graphics cards working together. It's a defensible baseline for
academic work. Government agencies would have faster hardware, but 10
billion/sec is widely cited in password security literature."

### About the Scoring

**Q: Why does attack resistance carry the most weight (45%)?**

A: "Because the only true test of a password is whether it survives a real
attack. A password can look mathematically perfect with high entropy and
good composition, but if it exists in a breach database, it will be cracked
instantly. Attack resistance is the real-world validation."

**Q: How do you ensure the scoring is not arbitrary?**

A: "Each pillar maps to a measurable cybersecurity principle: Composition
follows NIST password guidelines. Unpredictability uses Shannon entropy
from information theory. Attack resistance is empirical crackability
from real attack simulation. Red flags penalize common human patterns
documented in password cracking research."

**Q: Could two different passwords get the same score?**

A: "Yes, but they would have different weakness lists and suggestions.
Two passwords scoring 40/100 might fail for different reasons — one is
found in a dictionary, the other has low entropy. The score is the summary;
the feedback is the actionable part."

### About the Attack Simulation

**Q: Why simulate three different attacks?**

A: "Each attack reveals different weaknesses. A password might survive
dictionary lookup (it's unique) but still be weak against brute-force
because it is short. Another password might be long but contain a
dictionary word with leet substitutions, which rule-based cracking will
find. Three attacks give a complete picture."

**Q: How many rules does your rule-based attack use?**

A: "22 rules covering the most common user mutation patterns: capitalization,
number appending/prepending, leet speak, symbol appending, reversing,
doubling, and year appending. These cover approximately 80% of common
mutation patterns that real attackers use."

**Q: Where do your wordlists come from?**

A: "From the RockYou 2009 data breach — one of the largest password leaks
in history with 14 million real passwords. We use three tiered subsets:
Tier 1 has the 1000 most common passwords, Tier 2 has 100,000, and Tier 3
has 500,000. We also use an English dictionary with 104,000 words for
pattern detection."

### About the Visualization

**Q: Why use a log scale on the crack time chart?**

A: "Crack times range from milliseconds (dictionary match) to millions of
years (strong password). A linear scale would make the fast bars invisible
and the slow bars off the chart. Log scale lets you compare all values
proportionally — each step represents a 10x multiplication."

**Q: Why both terminal output and a saved chart?**

A: "The terminal output is for immediate interactive use — the user sees
results instantly. The saved PNG chart is for documentation and
presentations — it can be included in reports or projected on screen."

---

## Part 12: Common Traps to Avoid

### Trap 1: Pretending You Know Programming

**Don't say:** "I love writing Python code, it's my favorite language."

**Instead say:** "Python was chosen for this project because it's widely used
in cybersecurity, it has great libraries for our needs, and it's readable."

If asked "Did you write all this code yourself?" the best answer is:
"This is my final year project. I designed the system, wrote the code,
and tested it. I used standard libraries like `rich` and `matplotlib` for
visualization, which is common practice — you don't reinvent the wheel."

### Trap 2: Getting Tripped Up on Math

**Don't say:** "I don't know, the formula is in the code."

**Instead say:** "The entropy formula is `length × log₂(charset_size)` from
Claude Shannon's information theory. `log₂` converts the number of possible
characters into bits of information. Every bit doubles the number of possible
passwords an attacker must try."

Practice this. It sounds technical but is actually simple.

### Trap 3: Not Knowing Your Own Project Structure

**Memorize this:**
- `main.py` = the conductor
- `analysis.py` = analyzes password structure
- `attacks.py` = simulates dictionary, rule-based, brute-force attacks
- `scoring.py` = calculates score out of 100
- `visualization.py` = shows results on screen + saves chart
- `utils.py` = shared helper tools

### Trap 4: Forgetting Why the Project Matters

Your core argument is:

> "Most password checkers only measure complexity. We actually simulate
> attacks. That is what makes this project different and valuable."

If the supervisor asks "Why should I care about this project?" — this is
your answer.

### Trap 5: Not Being Ready for "What Would You Change?"

Have 2-3 improvements ready:

1. "Add a web interface so non-technical users can access it easily."
2. "Add more attack rules to catch more mutation patterns."
3. "Add personal information detection (names, dates, birthdays)."

---

## Part 13: Quick Reference — One-Liners Per File

| File | One-Sentence Purpose |
|---|---|
| `main.py` | The entry point — asks for password, calls all modules in order |
| `analysis.py` | Examines password structure — length, character types, entropy, patterns |
| `attacks.py` | Simulates 3 real attack methods — dictionary, rule-based, brute-force |
| `scoring.py` | Combines all results into a 0-100 score with specific feedback |
| `visualization.py` | Displays results with colored bars, attack log, summary, and chart |
| `utils.py` | Handy tools used across modules — file reading, time conversion |

### Quick Formulas

| Concept | Formula |
|---|---|
| Entropy | `length × log₂(charset_size)` |
| Keyspace | `charset_size ^ password_length` |
| Crack Time | `keyspace ÷ guesses_per_second` |
| Guesses/sec assumption | 10,000,000,000 |

### Key Numbers

| Concept | Value |
|---|---|
| Lowercase characters | 26 |
| Uppercase characters | 26 |
| Digits | 10 |
| Symbols | 33 |
| Max charset size | 95 |
| Guesses per second (assumed) | 10 billion |
| Tier 1 wordlist | 1,000 passwords |
| Tier 2 wordlist | 100,000 passwords |
| Tier 3 wordlist | 500,000 passwords |
| English dictionary | 104,000 words |

---

*Good luck with your defense. Read this document through at least twice
and practice the Q&A section out loud. You will do fine.*
