"""
analysis.py — Module 1: Password Analysis Engine
==================================================
PURPOSE:  Break down the password and measure its theoretical strength
          before any attack is simulated.

DATA FLOW:  main.py → analysis.py → analysis_result dict → main.py

THE CONCEPT:
  Before we simulate attacks, we need to understand what the password
  is made of. This is like a doctor taking vitals before a diagnosis.
  We measure:
    - Length (longer = better)
    - Character variety (more types = harder to brute-force)
    - Entropy (mathematical measure of unpredictability)
    - Patterns (humans are predictable — we catch that)
"""

import math

from utils import load_wordlist


# ─────────────────────────────────────────────────────────────────
#  KEYBOARD WALKS — common sequences attackers check first
#  WHY: Users type patterns (qwerty, asdf) because they're easy
#       to remember. Attackers know this and check them instantly.
# ─────────────────────────────────────────────────────────────────
KEYBOARD_WALKS = [
    "qwerty", "qwertz", "asdfgh", "asdf", "zxcvbn", "zxcv",
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1qaz2wsx", "qazwsx", "qweasd",
    # Horizontal runs
    "qwer", "wert", "erty", "rtyu", "tyui", "yuio", "uiop",
    "asdf", "sdfg", "dfgh", "fghj", "ghjk", "hjkl",
    "zxcv", "xcvb", "cvbn", "vbnm",
    # Number sequences
    "1234", "2345", "3456", "4567", "5678", "6789",
    "0987", "9876", "8765", "7654", "6543", "5432", "4321",
]

# ─────────────────────────────────────────────────────────────────
#  L33TSPEAK SUBSTITUTION MAP
#  WHY: Users think replacing letters with similar-looking symbols
#       makes passwords "secure." Attackers have these in their
#       rule sets. "p@ssw0rd" is still "password" to a computer.
# ─────────────────────────────────────────────────────────────────
LEET_REVERSE = str.maketrans({"@": "a", "3": "e", "1": "i", "0": "o",
                              "$": "s", "7": "t", "8": "b", "5": "s"})


def get_length(password):
    """
    WHY:  Length is the single most important factor in password strength.
          Every additional character exponentially increases the keyspace.
    WHAT: Returns the number of characters in the password.
    """
    return len(password)


def detect_charset(password):
    """
    WHY:  A password with only lowercase letters has 26 possible characters
          per position. Adding uppercase (26), digits (10), and symbols (33)
          increases the search space exponentially.
    WHAT: Scans the password and identifies which character types are present.
          Calculates charset_size for entropy and brute-force estimation.
    """
    result = {
        "lowercase": False,
        "uppercase": False,
        "digits": False,
        "symbols": False,
    }

    for char in password:
        if char.islower():
            result["lowercase"] = True
        elif char.isupper():
            result["uppercase"] = True
        elif char.isdigit():
            result["digits"] = True
        else:
            # Anything that's not a letter or digit = symbol
            result["symbols"] = True

    # Calculate total charset size for entropy math
    # Start at 0, add 26 for each character type present
    size = 0
    if result["lowercase"]:
        size += 26
    if result["uppercase"]:
        size += 26
    if result["digits"]:
        size += 10
    if result["symbols"]:
        # 33 common printable symbols
        size += 33

    result["charset_size"] = size
    return result


def calculate_entropy(password, charset_size):
    """
    WHY:  Entropy = the amount of "unpredictability" in the password.
          It's measured in bits. Every bit doubles the number of guesses
          an attacker needs to try.
          Formula: entropy = length * log2(charset_size)
          This is Claude Shannon's information theory — the gold standard.

    WHAT: Returns a float (bits of entropy) rounded to 2 decimal places.
    """
    if charset_size == 0:
        return 0.0
    return round(len(password) * math.log2(charset_size), 2)


def detect_patterns(password, wordlist_dir="wordlists"):
    """
    WHY:  Humans are terrible at randomness. We use patterns without
          realizing it. Attackers exploit every single one of these.
          This function catches the most common ones.

    WHAT: Checks the password for keyboard walks, repeated chars,
          l33tspeak, sequential runs, embedded dictionary words,
          and predictable structure (Capital+word+numbers).
    """
    lower_pw = password.lower()
    patterns = {
        "keyboard_walk": False,
        "repeated_chars": False,
        "leet_speak": False,
        "sequential": False,
        "common_word_embedded": False,
        "predictable_structure": False,
    }

    # ── KEYBOARD WALK CHECK ──────────────────────────────────
    # Check if any known keyboard sequence appears in the password
    for walk in KEYBOARD_WALKS:
        if walk in lower_pw:
            patterns["keyboard_walk"] = True
            break

    # ── REPEATED CHARACTERS CHECK ────────────────────────────
    # If any character repeats 3+ times consecutively (aaa, 111, @@@)
    for i in range(len(lower_pw) - 2):
        if lower_pw[i] == lower_pw[i + 1] == lower_pw[i + 2]:
            patterns["repeated_chars"] = True
            break

    # ── L33TSPEAK CHECK ──────────────────────────────────────
    # Reverse l33t substitutions and check if result is a dictionary word
    cleaned = password.translate(LEET_REVERSE)
    if cleaned != password:
        tier1 = load_wordlist(f"{wordlist_dir}/tier1_top1000.txt")
        if cleaned.lower() in tier1:
            patterns["leet_speak"] = True

    # ── SEQUENTIAL CHECK ─────────────────────────────────────
    # Check for ascending sequences: "abc", "123", "bcd", etc.
    for i in range(len(lower_pw) - 2):
        c1, c2, c3 = ord(lower_pw[i]), ord(lower_pw[i + 1]), ord(lower_pw[i + 2])
        # Ascending: a→b→c or 1→2→3
        if c2 - c1 == 1 and c3 - c2 == 1:
            patterns["sequential"] = True
            break
        # Descending: c→b→a or 3→2→1
        if c1 - c2 == 1 and c2 - c3 == 1:
            patterns["sequential"] = True
            break

    # ── COMMON WORD EMBEDDED CHECK ───────────────────────────
    # Check if any common word appears as a substring of the password
    tier1 = load_wordlist(f"{wordlist_dir}/tier1_top1000.txt")
    for word in tier1:
        if word in lower_pw and len(word) >= 3:
            patterns["common_word_embedded"] = True
            break

    # ── PREDICTABLE STRUCTURE CHECK ──────────────────────────
    # Capital + lowercase word + numbers at end (e.g., "Password123")
    # This is the #1 most common password structure pattern
    if len(password) >= 5:
        has_capital_start = password[0].isupper()
        has_numbers_end = password[-1].isdigit()
        middle = password[1:]
        # Check if middle part has at least one lowercase and rest are lowercase+digits
        if has_capital_start and has_numbers_end:
            if any(c.islower() for c in middle) and all(c.islower() or c.isdigit() for c in middle):
                patterns["predictable_structure"] = True

    return patterns


# ─────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT — called by main.py
#  Runs ALL analysis functions and returns a single result dict.
# ─────────────────────────────────────────────────────────────────
def analyze(password, wordlist_dir="wordlists"):
    """
    WHY:  This is the "orchestrator" — it runs every analysis function
          in order and packages the results into one dictionary.
    WHAT: Returns the analysis_result dict that gets passed to scoring.py.
    """
    charset = detect_charset(password)
    # Check if only first letter is capitalized (e.g., "Password")
    # This is a common pattern that weakens entropy despite having uppercase
    only_first_upper = (
        len(password) >= 2
        and password[0].isupper()
        and all(c.islower() for c in password[1:])
    )
    return {
        "length": get_length(password),
        "charset": charset,
        "entropy": calculate_entropy(password, charset["charset_size"]),
        "patterns": detect_patterns(password, wordlist_dir),
        "only_first_upper": only_first_upper,
    }
