"""
Phase 2: Data Cleaning Script - THE RUNNER/ORCHESTRATOR

THIS FILE IS JUST THE ENTRY POINT - IT CALLS THE ACTUAL CLEANING LOGIC.

The actual cleaning happens in: src/preprocessing.py
This script just:
1. Imports the cleaning functions
2. Specifies input/output paths
3. Runs the pipeline
4. Reports results

Architecture:
- src/preprocessing.py = Contains ALL the cleaning LOGIC and FUNCTIONS
- This file = RUNNER that calls those functions

To run: python scripts/phase_2_clean_data.py
"""

import sys
sys.path.insert(0, 'src')

from src.preprocessing import clean_data


def main():
    input_file = 'data/raw/ais_data.csv'
    output_file = 'data/processed/cleaned_data.csv'

    clean_data(input_file, output_file)

    print("[DONE] Phase 2 Complete")
    print("[NEXT] Phase 3: Feature Engineering")


if __name__ == '__main__':
    main()
