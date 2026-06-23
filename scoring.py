"""
scoring.py — Module 3: Scoring and Feedback Engine
=====================================================
PURPOSE:  Take ALL results from analysis and attack modules,
          calculate a weighted score out of 100, classify it,
          and generate human-readable feedback.

DATA FLOW:  main.py → scoring.py(analysis_result, attack_result)
             → final_score dict → main.py

THE CONCEPT:
  Most online password strength meters are misleading (they only check
  length + character types). Our scoring system is unique because it
  rewards REAL attack resistance — not just how "complex" the password
  looks. This is the key innovation for your project.
"""

GUESSES_PER_SECOND = 10_000_000_000


def score_composition(analysis):
    """
    WHY:  Composition is the "raw materials" of the password.
          Longer passwords + more character types = harder to crack.

    Scoring breakdown:
      - Length (12 points max): longer = exponentially harder
      - Character Variety (8 points max): 2 pts per type used

    Total: 20 points
    """
    length = analysis["length"]
    charset = analysis["charset"]
    score = 0

    # ── LENGTH SCORE (12 pts max) ────────────────────────────────
    if length >= 16:
        score += 12
    elif length >= 12:
        score += 11
    elif length >= 10:
        score += 9
    elif length >= 8:
        score += 6
    elif length >= 6:
        score += 3
    # 1-5 chars = 0 points

    # ── CHARACTER VARIETY SCORE (8 pts max — 2 pts per type) ────
    if charset["lowercase"]:
        score += 2
    if charset["uppercase"]:
        score += 2
    if charset["digits"]:
        score += 2
    if charset["symbols"]:
        score += 2

    return score


def score_unpredictability(analysis):
    """
    WHY:  A password that's long but entirely predictable (like
          "aaaaaaaa") is still weak. This pillar measures true
          randomness.

    Scoring breakdown:
      - Entropy (12 pts max): based on mathematical unpredictability
      - Pattern absence (8 pts max): penalized for each detected pattern

    Total: 20 points
    """
    entropy = analysis["entropy"]
    patterns = analysis["patterns"]
    score = 0

    # ── ENTROPY SCORE (12 pts max) ───────────────────────────────
    if entropy >= 60:
        score += 12
    elif entropy >= 50:
        score += 9
    elif entropy >= 36:
        score += 6
    elif entropy >= 28:
        score += 3
    # Below 28 = 0 points

    # ── PATTERN ABSENCE SCORE (8 pts max, start at 8, deduct) ───
    pattern_score = 8
    if patterns["keyboard_walk"]:
        pattern_score -= 3
    if patterns["repeated_chars"]:
        pattern_score -= 2
    if patterns["leet_speak"]:
        pattern_score -= 2
    if patterns["sequential"]:
        pattern_score -= 1

    # Passphrase penalty: multiple dictionary words = predictable
    embedded = patterns.get("embedded_words", [])
    if len(embedded) >= 2:
        pattern_score -= 3

    score += max(0, pattern_score)
    return score


def score_attack_resistance(attack, analysis=None):
    """
    WHY:  This is the MOST IMPORTANT pillar (45% of total).
          A password that fails under real attack is weak — period.
          This is what makes our tool different from any online checker.

    Scoring breakdown:
      - Dictionary attack survival (15 pts): found = 0, not found = 15
      - Rule-based attack survival (15 pts): same principle
      - Brute-force resistance (15 pts): based on estimated crack time

    Total: 45 points
    """
    score = 0

    # ── DICTIONARY ATTACK (15 pts) ───────────────────────────────
    if not attack["dictionary"]["found"]:
        score += 15

    # ── RULE-BASED ATTACK (15 pts) ───────────────────────────────
    if not attack["rule_based"]["found"]:
        score += 15

    # ── BRUTE-FORCE RESISTANCE (15 pts) ──────────────────────────
    bf_time = attack["brute_force"]["crack_time_seconds"]

    # Passphrase penalty: if password is made of dictionary words,
    # brute-force time overestimates security — attackers use word
    # combinations, not character-by-character search.
    is_passphrase = False
    if analysis:
        embedded = analysis.get("patterns", {}).get("embedded_words", [])
        if len(embedded) >= 2:
            is_passphrase = True
            # Approximate brute-force via word combinations
            word_count = len(embedded)
            dict_size = 10000  # typical attacker's wordlist
            word_keyspace = dict_size ** word_count
            word_bf_time = word_keyspace / GUESSES_PER_SECOND
            bf_time = min(bf_time, word_bf_time)

    if bf_time >= 31536000:  # 1 year+
        score += 15
    elif bf_time >= 2592000:  # 1 month+
        score += 12
    elif bf_time >= 86400:    # 1 day+
        score += 9
    elif bf_time >= 3600:     # 1 hour+
        score += 6
    elif bf_time >= 60:       # 1 minute+
        score += 3
    # Under 1 minute = 0 points

    return score


def score_red_flags(analysis):
    """
    WHY:  Some passwords have structural flaws that scream "weak"
          even before attacks run. These are penalty deductions.

    Starts at 15. Deducts for each red flag. Minimum 0.
    Total: 15 points
    """
    patterns = analysis["patterns"]
    score = 15

    if patterns["common_word_embedded"]:
        score -= 5
    if patterns["predictable_structure"]:
        score -= 4
    if analysis.get("only_first_upper", False):
        score -= 3

    # Passphrase penalty: multiple dictionary words in sequence
    embedded = patterns.get("embedded_words", [])
    if len(embedded) >= 2:
        score -= 5

    return max(0, score)


def classify(total_score):
    """
    WHY:  A number like "42/100" is abstract. Labels are immediately
          understood by anyone.

    WHAT: Maps a numeric score to a classification string.
    """
    if total_score <= 25:
        return "Very Weak"
    elif total_score <= 50:
        return "Weak"
    elif total_score <= 75:
        return "Moderate"
    elif total_score <= 90:
        return "Strong"
    else:
        return "Very Strong"


def generate_feedback(analysis, attack):
    """
    WHY:  Users need to know WHY their password is weak and HOW to fix it.
          Generic advice ("use a stronger password") is useless.
          Specific, actionable feedback changes behavior.

    WHAT: Scans all results and builds a list of weakness messages
          and corresponding suggestions.
    """
    weaknesses = []
    suggestions = []

    # ── DICTIONARY FOUND ─────────────────────────────────────────
    if attack["dictionary"]["found"]:
        weaknesses.append(
            f"Found in {attack['dictionary']['tier']} wordlist "
            f"(matched: '{attack['dictionary']['matched_word']}')"
        )
        suggestions.append(
            "Don't use real words or common passwords. "
            "Use a random passphrase or a password manager."
        )

    # ── RULE-BASED FOUND ─────────────────────────────────────────
    if attack["rule_based"]["found"]:
        weaknesses.append(
            f"Simple mutation of common word ('{attack['rule_based']['base_word']}') "
            f"via {attack['rule_based']['rule_applied']}"
        )
        suggestions.append(
            "Don't rely on character substitutions (@ for a, 0 for o). "
            "Attackers know every trick."
        )

    # ── SHORT LENGTH ─────────────────────────────────────────────
    if analysis["length"] < 8:
        weaknesses.append("Password is too short (under 8 characters)")
        suggestions.append("Use at least 12 characters for adequate security")
    elif analysis["length"] < 12:
        weaknesses.append("Password is moderately short (under 12 characters)")
        suggestions.append("Aim for 12+ characters — each extra character "
                           "exponentially increases cracking time")

    # ── MISSING CHARACTER TYPES ──────────────────────────────────
    missing = []
    if not analysis["charset"]["uppercase"]:
        missing.append("uppercase letters")
    if not analysis["charset"]["digits"]:
        missing.append("digits")
    if not analysis["charset"]["symbols"]:
        missing.append("symbols")

    if missing:
        weaknesses.append(f"Missing character types: {', '.join(missing)}")
        suggestions.append(
            "Use a mix of uppercase, lowercase, digits, and symbols. "
            "Each type exponentially increases cracking difficulty."
        )

    # ── PATTERNS ─────────────────────────────────────────────────
    if analysis["patterns"]["keyboard_walk"]:
        weaknesses.append("Contains keyboard pattern — first thing attackers try")
        suggestions.append("Avoid adjacent keyboard sequences like 'qwerty' or '12345'")

    if analysis["patterns"]["repeated_chars"]:
        weaknesses.append("Contains repeated characters (e.g., 'aaa', '111')")
        suggestions.append("Avoid repeating the same character — it adds no real security")

    if analysis["patterns"]["sequential"]:
        weaknesses.append("Contains sequential characters ('abc', '321')")
        suggestions.append("Avoid letter or number sequences — they're predictable")

    if analysis["patterns"]["leet_speak"]:
        weaknesses.append("Contains leetspeak substitutions — easily reversed by attackers")
        suggestions.append("Leetspeak (p@ssw0rd) doesn't fool modern attackers — they reverse it automatically")

    if analysis["patterns"]["predictable_structure"]:
        weaknesses.append("Follows Capital+word+numbers structure — extremely common")
        suggestions.append("Don't just capitalize the first letter and add numbers at the end")

    if analysis["patterns"]["common_word_embedded"]:
        weaknesses.append("Contains a common dictionary word")
        suggestions.append("Avoid real words entirely. Use random character strings.")

    # ── PASSPHRASE DETECTED ──────────────────────────────────────
    embedded = analysis["patterns"].get("embedded_words", [])
    if len(embedded) >= 2:
        words_str = ", ".join(embedded[:4])
        weaknesses.append(
            f"Password is a passphrase of {len(embedded)} dictionary words "
            f"({words_str}) — vulnerable to word-combination attacks"
        )
        suggestions.append(
            "Passphrases are better than single words but still weak against "
            "word-combination attacks. Use random character strings instead."
        )

    # ── LOW ENTROPY ──────────────────────────────────────────────
    if analysis["entropy"] < 36:
        weaknesses.append(f"Low entropy ({analysis['entropy']} bits) — mathematically predictable")
        suggestions.append("Increase length and use all character types for higher entropy")

    return weaknesses, suggestions


# ─────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT — called by main.py
#  Runs all scoring functions and returns the complete result.
# ─────────────────────────────────────────────────────────────────
def calculate_score(analysis_result, attack_result):
    """
    WHY:  Orchestrator — runs all four pillar scorers, classifies
          the total, and generates feedback.

    WHAT: Returns the final_score dict displayed to the user.
    """
    comp = score_composition(analysis_result)
    unpre = score_unpredictability(analysis_result)
    resist = score_attack_resistance(attack_result, analysis_result)
    reds = score_red_flags(analysis_result)

    total = comp + unpre + resist + reds
    classification = classify(total)
    weaknesses, suggestions = generate_feedback(analysis_result, attack_result)

    return {
        "pillar_scores": {
            "composition": comp,
            "unpredictability": unpre,
            "attack_resistance": resist,
            "red_flags": reds,
        },
        "total": total,
        "classification": classification,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }
