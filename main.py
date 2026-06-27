"""
main.py — Entry Point / CLI Handler
=====================================
PURPOSE:  The face of the application. Handles user interaction,
          calls each module in order, and passes data between them.

DATA FLOW:
  User Input (password)
       ↓
  main.py ──→ analysis.py  ──→ analysis_result
       ↓
  main.py ──→ attacks.py   ──→ attack_result
       ↓
  main.py ──→ scoring.py   ──→ final_score
       ↓
  main.py ──→ visualization.py ──→ terminal output + PNG file

THE CONCEPT:
  Each module is independent. main.py is just the "conductor" that
  passes the session dictionary through each processing step.
  This makes the code easy to understand, test, and extend.
"""

import os
import getpass
import sys

from rich.console import Console
from rich.prompt import Prompt

# Import each module — each one is independent
from analysis import analyze
from attacks import simulate_attacks
from scoring import calculate_score
from visualization import display_results

console = Console()


def get_base_dir():
    """
    WHY:  When running from different directories, we need to reliably
          find the wordlists/ and output/ folders.
    WHAT: Returns the directory where main.py is located.
    """
    return os.path.dirname(os.path.abspath(__file__))


def display_banner():
    """
    WHY:  First impression — a clean, professional banner sets the tone.
    WHAT: Prints the welcome banner using rich formatting.
    """
    banner = """
    ╔══════════════════════════════════════════════╗
    ║         PASSWORD SECURITY ANALYZER           ║
    ║         with Attack Simulation v1.0          ║
    ╚══════════════════════════════════════════════╝
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("This tool analyzes password strength by simulating\n"
                  "real-world attack techniques.\n")


def run_analysis(password, base_dir):
    """
    WHY:  Runs all four modules in sequence, passing the session
          dictionary through each step. This is the core pipeline.

    WHAT: Orchestrates the full analysis pipeline.
          Returns nothing — results are displayed directly.
    """
    wordlist_dir = os.path.join(base_dir, "wordlists")
    output_dir = os.path.join(base_dir, "output")

    # ── STEP 1: Analysis Engine ───────────────────────────────────
    console.print("\n[1/4] Running analysis...")
    analysis_result = analyze(password, wordlist_dir)

    # ── STEP 2: Attack Simulation ─────────────────────────────────
    console.print("[2/4] Simulating attacks...")
    attack_result = simulate_attacks(
        password,
        analysis_result["charset"]["charset_size"],
        wordlist_dir,
    )

    # ── STEP 3: Scoring Engine ────────────────────────────────────
    console.print("[3/4] Calculating score...")
    final_score = calculate_score(analysis_result, attack_result)

    # ── STEP 4: Visualization ─────────────────────────────────────
    console.print("[4/4] Generating report...\n")
    display_results(analysis_result, attack_result, final_score, output_dir)


def main():
    """
    WHY:  Main entry point. Handles the CLI loop.
          Users can analyze multiple passwords in one session.
    """
    # Save the original directory so we work relative to main.py
    base_dir = get_base_dir()

    display_banner()

    while True:
        # ── GET PASSWORD ──────────────────────────────────────────
        try:
            password = getpass.getpass("Enter password to analyze: ")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Goodbye![/yellow]")
            break

        if not password:
            console.print("[red]Password cannot be empty.[/red]")
            continue

        # ── RUN THE FULL PIPELINE ─────────────────────────────────
        run_analysis(password, base_dir)

        # ── ASK TO CONTINUE ───────────────────────────────────────
        again = Prompt.ask(
            "\nAnalyze another password?",
            choices=["y", "n"],
            default="y",
        )
        if again.lower() != "y":
            console.print("[cyan]Stay secure! Goodbye.[/cyan]")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)
