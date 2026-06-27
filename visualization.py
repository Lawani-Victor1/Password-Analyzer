"""
visualization.py — Module 4: Visualization Module
====================================================
PURPOSE:  Present all analysis results in a clear, visual format
          directly in the terminal. Also saves a crack-time chart
          as a PNG file for inclusion in reports.

DATA FLOW:  main.py → visualization.py(all results) → terminal + PNG

THE CONCEPT:
  A wall of text is hard to digest. Visuals make strengths and
  weaknesses immediately obvious. We use the `rich` library for
  terminal formatting and `matplotlib` for the crack-time chart.
"""

import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout

console = Console()


def display_strength_meter(final_score):
    """
    WHY:  A progress bar is instantly readable — you can see the
          score at a glance without reading numbers.
    WHAT: Renders an ASCII progress bar colored by severity.
    """
    total = final_score["total"]
    classification = final_score["classification"]

    # Choose color based on classification
    if total <= 25:
        color = "red"
    elif total <= 50:
        color = "orange1"  # rich supports xterm colors
    elif total <= 75:
        color = "yellow"
    elif total <= 90:
        color = "green"
    else:
        color = "bright_green"

    bar_len = 30
    filled = int(bar_len * total / 100)
    bar = "=" * filled + "-" * (bar_len - filled)
    styled_bar = f"[{color}][{bar}][/{color}]"

    console.print(Panel(
        f"\n  Overall Strength: {styled_bar}  {total}/100\n"
        f"  Classification: [bold {color}]{classification}[/bold {color}]\n",
        title="[bold]Password Strength Report[/bold]",
        border_style=color,
    ))


def display_pillar_breakdown(final_score):
    """
    WHY:  Showing the breakdown by pillar helps users understand
          WHERE their password lost points. This teaches them what
          matters for password security.
    WHAT: Renders four mini progress bars, one per scoring pillar.
    """
    pillars = final_score["pillar_scores"]
    max_scores = {
        "composition": 20,
        "unpredictability": 20,
        "attack_resistance": 45,
        "red_flags": 15,
    }
    labels = {
        "composition": "Composition      ",
        "unpredictability": "Unpredictability ",
        "attack_resistance": "Attack Res.     ",
        "red_flags": "Red Flags       ",
    }

    for key, max_val in max_scores.items():
        val = pillars[key]
        bar_len = 20
        filled = int(bar_len * val / max_val)
        bar = "=" * filled + "-" * (bar_len - filled)
        bar_color = "red" if val <= max_val * 0.3 else "yellow" if val <= max_val * 0.6 else "green"
        console.print(f"  [{bar_color}]{labels[key]} [{bar}]  {val}/{max_val}[/{bar_color}]")


def display_attack_log(attack_result):
    """
    WHY:  Users need to see EXACTLY what happened during each attack.
          This demystifies how password cracking works and makes the
          results credible.
    WHAT: Step-by-step display of each attack's attempt and outcome.
    """
    console.print("\n[bold underline]Attack Simulation Log[/bold underline]")
    console.print("─" * 60)

    # ── DICTIONARY ATTACK ────────────────────────────────────────
    dict_res = attack_result["dictionary"]
    console.print("\n[bold cyan][Dictionary Attack][/bold cyan]")
    if dict_res["found"]:
        console.print(f"  [red]✓ FOUND[/red] in {dict_res['tier']} "
                      f"(matched: '[bold]{dict_res['matched_word']}[/bold]')")
    else:
        console.print("  [green]✗ Not found[/green] in any tier")

    # ── RULE-BASED ATTACK ────────────────────────────────────────
    rule_res = attack_result["rule_based"]
    console.print("\n[bold cyan][Rule-based Attack][/bold cyan]")
    if rule_res["found"]:
        console.print(f"  Base word   : [bold]{rule_res['base_word']}[/bold]")
        console.print(f"  Rule applied: {rule_res['rule_applied']}")
        console.print(f"  Mutated form: [bold]{rule_res['mutated_form']}[/bold]")
        console.print("  [red]✓ MATCH FOUND[/red]")
    else:
        console.print("  [green]✗ No mutation matched[/green]")

    # ── BRUTE-FORCE ESTIMATE ─────────────────────────────────────
    bf = attack_result["brute_force"]
    console.print("\n[bold cyan][Brute-force Estimate][/bold cyan]")
    console.print(f"  Charset size    : {bf['charset_size']} characters")
    console.print(f"  Password length : {bf['password_length']} characters")
    console.print(f"  Keyspace        : {bf['keyspace']:,.0f} combinations")
    console.print(f"  Estimated time  : [bold]{bf['crack_time_readable']}[/bold]")

    console.print("\n" + "─" * 60)


def display_summary_report(analysis_result, final_score):
    """
    WHY:  A clean, printable summary at the end for screenshots
          or inclusion in the project report.
    WHAT: Displays key metrics, weaknesses, and suggestions.
    """
    console.print("\n" + "═" * 60)
    console.print("[bold]           PASSWORD ANALYSIS REPORT[/bold]")
    console.print("═" * 60)

    analysis = analysis_result
    score = final_score

    # Summary metrics
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("Password Length", f"{analysis['length']} characters")

    # Character types used
    types_used = []
    cs = analysis["charset"]
    if cs["lowercase"]:
        types_used.append("lowercase")
    if cs["uppercase"]:
        types_used.append("uppercase")
    if cs["digits"]:
        types_used.append("digits")
    if cs["symbols"]:
        types_used.append("symbols")
    table.add_row("Character Types", ", ".join(types_used))

    table.add_row("Entropy", f"{analysis['entropy']} bits")
    table.add_row("Overall Score", f"{score['total']} / 100")
    table.add_row("Classification", f"[bold]{score['classification']}[/bold]")

    console.print(table)

    # Weaknesses
    if score["weaknesses"]:
        console.print("\n[bold red]WEAKNESSES DETECTED:[/bold red]")
        for w in score["weaknesses"]:
            console.print(f"  • {w}")

    # Suggestions
    if score["suggestions"]:
        console.print("\n[bold green]SUGGESTIONS:[/bold green]")
        for s in score["suggestions"]:
            console.print(f"  • {s}")

    console.print("═" * 60 + "\n")


def save_crack_time_chart(attack_result, output_dir="output"):
    """
    WHY:  A visual chart showing crack times across attack types is
          powerful for presentations and the written report. The log
          scale is necessary because times range from milliseconds to
          millions of years.

    WHAT: Saves a horizontal bar chart as report.png in output/.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        console.print("[yellow]matplotlib not installed — skipping chart[/yellow]")
        return

    bf = attack_result["brute_force"]
    bf_seconds = bf["crack_time_seconds"]

    # Build crack time data
    # Dictionary attack: either 0 (found) or keyspace/rate for full search
    if attack_result["dictionary"]["found"]:
        dict_time = 0.001  # Found instantly — milliseconds
    else:
        dict_time = bf_seconds  # Would need full brute-force

    if attack_result["rule_based"]["found"]:
        rule_time = 0.01  # Found quickly — a few milliseconds
    else:
        rule_time = bf_seconds  # Would need full brute-force

    # Create the chart
    attack_types = ["Dictionary\nAttack", "Rule-based\nAttack", "Brute-force\nEstimate"]
    times = [dict_time, rule_time, bf_seconds]

    # Use log scale for readability (times range from ms to years)
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["#e74c3c" if t < 60 else "#f39c12" if t < 86400 else "#27ae60"
              for t in times]
    bars = ax.barh(attack_types, times, color=colors)

    ax.set_xscale("log")
    ax.set_xlabel("Estimated Crack Time (seconds, log scale)")
    ax.set_title("Password Crack Time by Attack Type")

    # Add time labels on bars
    from utils import seconds_to_readable
    for bar, time_val in zip(bars, times):
        label = seconds_to_readable(time_val)
        ax.text(bar.get_width() * 1.1, bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=9)

    plt.tight_layout()

    # Save
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "report.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    console.print(f"[green]Chart saved to: {filepath}[/green]")


# ─────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT — called by main.py
#  Runs ALL visualization functions in display order.
# ─────────────────────────────────────────────────────────────────
def display_results(analysis_result, attack_result, final_score, output_dir="output"):
    """
    WHY:  Orchestrator — displays everything in the right order
          so the user gets a smooth, professional report flow.
    WHAT: No return value — just renders output to terminal + file.
    """
    display_strength_meter(final_score)
    display_pillar_breakdown(final_score)
    display_attack_log(attack_result)
    display_summary_report(analysis_result, final_score)
    save_crack_time_chart(attack_result, output_dir)
