"""
attacks.py — Module 2: Attack Simulation
==========================================
PURPOSE:  Simulate how a real attacker would attempt to crack the password.
          Three attack types: dictionary, rule-based mutation, and
          brute-force estimation.

DATA FLOW:  main.py → attacks.py → attack_result dict → main.py

THE CONCEPT:
  A password can look strong on paper but still be terrible in practice.
  The only real test is: would it survive a real attack?
  We simulate three techniques that real attackers use.
"""

import math
import os

from utils import normalize, load_wordlist, seconds_to_readable, apply_leet


# ─────────────────────────────────────────────────────────────────
#  BRUTE-FORCE SPEED ASSUMPTION
#  WHY: Attackers use GPUs that can try billions of passwords per
#       second. 10 billion/sec represents a modern setup (e.g.,
#       8x RTX 4090s cracking NTLM hashes). This is realistic and
#       defensible in your presentation.
# ─────────────────────────────────────────────────────────────────
GUESSES_PER_SECOND = 10_000_000_000


def dictionary_attack(password, wordlist_dir="wordlists"):
    """
    WHY:  ~90% of real-world attacks start with dictionary wordlists.
          RockYou alone has 14 million real passwords. If your password
          is in there, it's game over instantly.

    WHAT: Checks the password against 3 tiers of wordlists.
          Tier 1 (1000) → Tier 2 (100k) → Tier 3 (500k)
          Returns whether found, which tier, and the matched word.
    """
    normalized = normalize(password)
    tiers = [
        ("Tier 1", "tier1_top1000.txt"),
        ("Tier 2", "tier2_rockyou_100k.txt"),
        ("Tier 3", "tier3_extended.txt"),
    ]

    for tier_name, filename in tiers:
        filepath = os.path.join(wordlist_dir, filename)
        wordlist = load_wordlist(filepath)
        for word in wordlist:
            if normalized == word:
                return {
                    "found": True,
                    "tier": tier_name,
                    "matched_word": word,
                }

    return {"found": False, "tier": None, "matched_word": None}


def rule_based_attack(password, wordlist_dir="wordlists"):
    """
    WHY:  Smart attackers don't just try dictionary words — they mutate them.
          Hashcat (the industry standard) has a full rule engine. We simulate
          9 common rules that cover most user tricks.

    WHAT: Applies 9 mutation rules to every word in Tier 1 + Tier 2.
          If any variant matches the password, we report which rule exposed it.
    """
    normalized = normalize(password)
    rules = [
        ("R1: Capitalize first letter", lambda w: w.capitalize()),
        ("R2: All caps", lambda w: w.upper()),
        ("R3: Append 1", lambda w: w + "1"),
        ("R3: Append 12", lambda w: w + "12"),
        ("R3: Append 123", lambda w: w + "123"),
        ("R3: Append 1234", lambda w: w + "1234"),
        ("R4: Prepend 1", lambda w: "1" + w),
        ("R4: Prepend 12", lambda w: "12" + w),
        ("R4: Prepend 123", lambda w: "123" + w),
        ("R5: L33tspeak", lambda w: apply_leet(w)),
        ("R6: Append !", lambda w: w + "!"),
        ("R6: Append @", lambda w: w + "@"),
        ("R6: Append #", lambda w: w + "#"),
        ("R7: Reverse", lambda w: w[::-1]),
        ("R8: Double", lambda w: w + w),
        ("R9: Append 2020", lambda w: w + "2020"),
        ("R9: Append 2021", lambda w: w + "2021"),
        ("R9: Append 2022", lambda w: w + "2022"),
        ("R9: Append 2023", lambda w: w + "2023"),
        ("R9: Append 2024", lambda w: w + "2024"),
        ("R9: Append 2025", lambda w: w + "2025"),
        ("R9: Append 2026", lambda w: w + "2026"),
    ]

    # Load Tier 1 + Tier 2 wordlists as base words
    base_words = []
    for filename in ["tier1_top1000.txt", "tier2_rockyou_100k.txt"]:
        filepath = os.path.join(wordlist_dir, filename)
        base_words.extend(load_wordlist(filepath))

    # Test every base word mutated by every rule
    for base_word in base_words:
        for rule_name, rule_func in rules:
            mutated = rule_func(base_word)
            if mutated == normalized:
                return {
                    "found": True,
                    "base_word": base_word,
                    "rule_applied": rule_name,
                    "mutated_form": mutated,
                }

    return {"found": False, "base_word": None, "rule_applied": None, "mutated_form": None}


def brute_force_estimator(password, charset_size):
    """
    WHY:  Even if the password isn't in any wordlist, an attacker can
          try every possible combination. This calculates how long that
          would take — the ultimate measure of password strength.

    THE MATH:
      Keyspace = charset_size ^ password_length
      Time (sec) = keyspace / guesses_per_second

    WHAT: Returns estimated crack time in seconds + human-readable form.
    """
    pw_length = len(password)

    # Calculate keyspace (total possible combinations)
    keyspace = charset_size ** pw_length

    # Calculate crack time
    crack_time_seconds = keyspace / GUESSES_PER_SECOND

    return {
        "charset_size": charset_size,
        "password_length": pw_length,
        "keyspace": keyspace,
        "crack_time_seconds": crack_time_seconds,
        "crack_time_readable": seconds_to_readable(crack_time_seconds),
    }


# ─────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT — called by main.py
#  Runs ALL three attack simulations and returns a single dict.
# ─────────────────────────────────────────────────────────────────
def simulate_attacks(password, charset_size, wordlist_dir="wordlists"):
    """
    WHY:  Orchestrator — runs all three attacks in sequence.
          Even if dictionary finds it, we still run the others
          for a complete report (the user needs to see ALL weaknesses).

    WHAT: Returns the attack_result dict passed to scoring.py.
    """
    return {
        "dictionary": dictionary_attack(password, wordlist_dir),
        "rule_based": rule_based_attack(password, wordlist_dir),
        "brute_force": brute_force_estimator(password, charset_size),
    }
