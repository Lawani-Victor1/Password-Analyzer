# Conceptual Framework
## Development of a Password Security Analyzer with Attack Simulation

---

## 1. Introduction

Passwords remain the most widely used mechanism for authenticating users in digital systems. Despite their prevalence, weak passwords continue to be one of the leading causes of security breaches globally. This project aims to develop a **Password Security Analyzer with Attack Simulation** — a Python-based command-line tool that evaluates the strength of passwords, simulates real-world attack techniques against them, and provides visual feedback to help users understand their exposure to threats.

The system is designed not just to rate passwords, but to *demonstrate* how attackers would actually approach cracking them — making the feedback concrete, educational, and actionable.

The system will be built using **Python** and delivered as a **Command-Line Interface (CLI) application**.

---

## 2. Conceptual Overview

The system operates on a simple but powerful flow:

```
User Input (Password)
        |
        v
+-------------------+
| Analysis Engine   |  ← Entropy, patterns, character sets
+-------------------+
        |
        v
+-------------------+
| Attack Simulation |  ← Dictionary, Brute-force, Rule-based
+-------------------+
        |
        v
+-------------------+
| Scoring Engine    |  ← Weighted strength score + weaknesses
+-------------------+
        |
        v
+-------------------+
| Visualization     |  ← Crack-time graphs, strength meter, report
+-------------------+
        |
        v
   Output / Report
```

---

## 3. System Modules

### Module 1 — Password Analysis Engine

**Purpose:** Break down the password and measure its theoretical strength before any attack is simulated.

**Inputs:** Raw password string from the user

**Processes:**
- Character set detection (lowercase, uppercase, digits, symbols)
- Length evaluation
- Strength estimation — evaluates how unpredictable the password is based on its length and the variety of character types used (letters, numbers, symbols)
- Pattern detection:
  - Keyboard walks (e.g., `qwerty`, `12345`)
  - Repeated characters (e.g., `aaa`, `111`)
  - Common substitutions / l33tspeak (e.g., `p@ssw0rd`)
  - Dictionary words embedded in password

**Outputs:** Strength score, detected patterns, character set report

---

### Module 2 — Attack Simulation Module

**Purpose:** Simulate how a real attacker would attempt to crack the given password.

**Inputs:** Password string, selected attack mode(s)

**Attack Types Simulated:**

| Attack Type | Description |
|---|---|
| **Dictionary Attack** | Tests the password against a wordlist of common passwords (e.g., rockyou.txt subset) |
| **Brute-force Estimator** | Calculates time-to-crack based on character set, length, and assumed hardware speed |
| **Rule-based Mutation** | Applies common transformations — capitalizing first letter, appending numbers, l33tspeak substitutions — to dictionary words and tests them |

**Outputs:** Match result (found / not found), estimated crack time, attack path taken

---

### Module 3 — Scoring and Feedback Engine

**Purpose:** Combine analysis and attack results into a single, human-readable strength score with specific feedback.

**Inputs:** Strength score, pattern flags, attack simulation results

**Processes:**
- Weighted scoring across: length, complexity, character variety, attack resistance
- Strength classification:

| Score Range | Classification |
|---|---|
| 0 – 25 | Very Weak |
| 26 – 50 | Weak |
| 51 – 75 | Moderate |
| 76 – 90 | Strong |
| 91 – 100 | Very Strong |

- Specific weakness explanations tied to score deductions
  - Example: *"This password was found in a dictionary wordlist — it would be cracked instantly."*
  - Example: *"Password uses only lowercase letters — brute-force crackable in under 2 minutes."*

**Outputs:** Final score, classification label, list of specific weakness messages, improvement suggestions

---

### Module 4 — Visualization Module

**Purpose:** Present results in a clear, visual format directly in the CLI.

**Inputs:** Score, attack results, crack time estimates

**Visual Outputs:**
- **Strength meter** — ASCII/terminal progress bar showing overall score
- **Crack time bar chart** — Estimated crack time across attack types (rendered with `matplotlib` or `rich`)
- **Attack simulation log** — Step-by-step display of what each attack attempted
- **Summary report** — Printable text summary of all findings

**Tools:** Python `rich` library (for CLI visuals), `matplotlib` (for charts saved as PNG)

---

## 4. Theoretical Foundations

| Concept | Application in This Project |
|---|---|
| **Password Unpredictability** | The longer a password and the more varied its characters, the harder it is to guess or crack |
| **Brute-force Complexity** | Time-to-crack estimates based on keyspace size and hardware speed assumptions |
| **Dictionary Attack Theory** | Real-world attackers use known password lists; simulated here with a curated wordlist |
| **Rule-based Attack Theory** | Attackers apply common mutations to wordlists; replicated in the mutation engine |
| **Security Feedback Design** | Specific, actionable feedback improves user behavior more than generic scores |

---

## 5. System Boundaries and Scope

**In Scope:**
- Single password analysis per session
- Three attack simulation modes (dictionary, brute-force estimation, rule-based)
- CLI interface with visual output
- Static wordlist (no live internet queries)

**Out of Scope:**
- Network-based or online password cracking
- Multi-user or database integration
- Password storage or management features

---

## 6. Expected Outcomes

Upon completion, the system will:

1. Accept a password from the user via CLI
2. Analyse it across strength, pattern, and character set dimensions
3. Simulate dictionary, brute-force, and rule-based attacks against it
4. Produce a scored report with specific, plain-language feedback
5. Visualize crack-time estimates and overall strength graphically

The project demonstrates practical application of cybersecurity principles — specifically offensive techniques used defensively — to educate users on real password risk.

---

*Final Year Project — HND Computer Science*
