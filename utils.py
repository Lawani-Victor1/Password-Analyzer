"""
utils.py — Shared Helper Functions
====================================
PURPOSE:  Functions used across multiple modules live here so no module
          imports from another module. Keeps dependencies clean.
"""

import os
import math


def normalize(password):
    """
    WHY:  Attackers don't care about case — they try lowercase first.
          Normalizing ensures our dictionary match catches 'Password'
          even if the wordlist entry is 'password'.
    WHAT: Converts password to lowercase and strips surrounding whitespace.
    """
    return password.strip().lower()


def load_wordlist(filepath):
    """
    WHY:  Wordlists are just text files with one word per line.
          This function turns them into a Python list for fast searching.
    WHAT: Reads a wordlist file, returns a list of stripped lowercase words.
          Returns empty list if file not found (so attacks don't crash).
    """
    if not os.path.exists(filepath):
        return []
    words = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            words.append(line.strip())
    return words


def seconds_to_readable(seconds):
    """
    WHY:  "1012847189 seconds" means nothing to a user.
          "32 years" is immediately understandable.
    WHAT: Converts raw seconds into human-readable time string.
    """
    if seconds < 1:
        return "less than 1 second"
    if seconds < 60:
        return f"{int(seconds)} second{'s' if seconds != 1 else ''}"
    if seconds < 3600:
        mins = int(seconds // 60)
        return f"{mins} minute{'s' if mins != 1 else ''}"
    if seconds < 86400:
        hrs = int(seconds // 3600)
        return f"{hrs} hour{'s' if hrs != 1 else ''}"
    if seconds < 2592000:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''}"
    if seconds < 31536000:
        months = int(seconds // 2592000)
        return f"{months} month{'s' if months != 1 else ''}"
    years = int(seconds // 31536000)
    return f"{years} year{'s' if years != 1 else ''}"


def apply_leet(word):
    """
    WHY:  L33tspeak is the most common substitution trick users try.
          Attackers know every replacement — we simulate what they do.
    WHAT: Applies common l33t substitutions to a word.
          Used by the rule-based attack to generate mutated forms.
    """
    leet_map = {
        "a": "@", "e": "3", "i": "1", "o": "0",
        "s": "$", "t": "7", "l": "1", "b": "8",
    }
    result = ""
    for char in word:
        result += leet_map.get(char, char)
    return result
