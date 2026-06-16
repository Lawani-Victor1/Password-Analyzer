# Password Security Analyzer with Attack Simulation

> A Python CLI tool that analyzes password strength by simulating real-world attack techniques: dictionary lookup, rule-based mutation, and brute-force estimation.

**Final Year Project — HND Computer Science**

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Project Structure

```
├── main.py            # Entry point — orchestrates all 4 modules
├── analysis.py        # Module 1: Password composition & pattern analysis
├── attacks.py         # Module 2: Dictionary, rule-based, brute-force simulation
├── scoring.py         # Module 3: Pillar scoring (0-100) + feedback generation
├── visualization.py   # Module 4: Rich terminal output + matplotlib chart
├── utils.py           # Shared helpers
├── requirements.txt   # rich, matplotlib
├── wordlists/         # Tiered RockYou subsets (1K / 100K / 500K)
├── output/            # Generated charts
├── docs/
│   ├── study_guide.md              # Full study guide with Q&A per module
│   ├── conceptual_framework.md     # Academic framework document
│   └── password_analyzer_blueprint.md  # Original design blueprint
└── README.md
```

See `docs/study_guide.md` for module-by-module explanations and likely supervisor questions with model answers.
