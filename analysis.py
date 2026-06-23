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
import os

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
                              "$": "s", "7": "t", "8": "b", "5": "s",
                              "4": "a", "2": "z", "6": "g", "9": "g"})


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


def load_dictionary(wordlist_dir):
    """Load English dictionary words into a set for fast lookup."""
    path = os.path.join(wordlist_dir, "dictionary.txt")
    words = load_wordlist(path)
    return set(w.lower() for w in words if len(w) >= 4)


def decompose_words(text, word_set):
    """Greedily decompose text into dictionary words (min 4 chars).
    Returns list of matched words or empty list if insufficient coverage.
    """
    s = text.lower()
    matched = []
    i = 0
    while i < len(s):
        best = None
        for j in range(len(s), i, -1):
            chunk = s[i:j]
            if len(chunk) >= 4 and chunk in word_set:
                best = chunk
                break
        if best:
            matched.append(best)
            i += len(best)
        else:
            i += 1
    total_chars = sum(len(w) for w in matched)
    if total_chars >= len(s) * 0.7 and len(matched) >= 2:
        return matched
    return []


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
        "embedded_words": [],
    }

    # Load word lists once
    tier1 = load_wordlist(f"{wordlist_dir}/tier1_top1000.txt")
    dictionary = load_dictionary(wordlist_dir)

    # ── KEYBOARD WALK CHECK ──────────────────────────────────
    for walk in KEYBOARD_WALKS:
        if walk in lower_pw:
            patterns["keyboard_walk"] = True
            break

    # ── REPEATED CHARACTERS CHECK ────────────────────────────
    for i in range(len(lower_pw) - 2):
        if lower_pw[i] == lower_pw[i + 1] == lower_pw[i + 2]:
            patterns["repeated_chars"] = True
            break

    # ── L33TSPEAK CHECK ──────────────────────────────────────
    # Count actual substitutions, then check if l33t-reversed form
    # contains a dictionary word (min 2 substitutions required)
    cleaned = password.translate(LEET_REVERSE)
    if cleaned != password:
        substitutions = sum(1 for a, b in zip(password, cleaned) if a != b)
        cleaned_lower = cleaned.lower()
        if substitutions >= 2:
            if cleaned_lower in dictionary or cleaned_lower in tier1:
                patterns["leet_speak"] = True
            else:
                # Check if any dictionary word is a substring of the cleaned form
                for i in range(len(cleaned_lower)):
                    for j in range(i + 4, min(i + 20, len(cleaned_lower) + 1)):
                        if cleaned_lower[i:j] in dictionary:
                            patterns["leet_speak"] = True
                            break
                    if patterns["leet_speak"]:
                        break

    # ── SEQUENTIAL CHECK ─────────────────────────────────────
    for i in range(len(lower_pw) - 2):
        c1, c2, c3 = ord(lower_pw[i]), ord(lower_pw[i + 1]), ord(lower_pw[i + 2])
        if c2 - c1 == 1 and c3 - c2 == 1:
            patterns["sequential"] = True
            break
        if c1 - c2 == 1 and c2 - c3 == 1:
            patterns["sequential"] = True
            break

    # ── COMMON WORD EMBEDDED + PASSPHRASE CHECK ──────────────
    # Check tier1 common passwords first
    for word in tier1:
        if word in lower_pw and len(word) >= 3:
            patterns["common_word_embedded"] = True
            break

    # Check English dictionary for embedded words
    cleaned = password.translate(LEET_REVERSE).lower()
    for word in dictionary:
        if len(word) < 4:
            continue
        if word in lower_pw or word in cleaned:
            patterns["common_word_embedded"] = True
            break

    # Try passphrase decomposition on both raw and l33t-cleaned versions
    words = decompose_words(password, dictionary)
    if not words and cleaned != lower_pw:
        words = decompose_words(cleaned, dictionary)
    if words:
        patterns["embedded_words"] = words

    # ── PREDICTABLE STRUCTURE CHECK ──────────────────────────
    # Capital + lowercase word + numbers at end (e.g., "Password123", "Password123!")
    if len(password) >= 5 and password[0].isupper():
        # Find where trailing digits start (strip trailing symbols)
        rest = password[1:]
        trailing_digits = ""
        i = len(rest) - 1
        while i >= 0 and not rest[i].isalpha():
            if rest[i].isdigit():
                trailing_digits = rest[i] + trailing_digits
            i -= 1
        middle = rest[:i + 1]
        if trailing_digits and len(trailing_digits) >= 1:
            if middle and any(c.islower() for c in middle) and all(c.islower() or c.isdigit() for c in middle):
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
