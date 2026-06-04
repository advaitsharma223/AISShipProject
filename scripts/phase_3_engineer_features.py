"""
Phase 3: Feature Engineering Script - THE RUNNER/ORCHESTRATOR

THIS FILE IS JUST THE ENTRY POINT - IT CALLS THE ACTUAL FEATURE ENGINEERING LOGIC.

The actual feature engineering happens in: src/feature_engineering.py
This script just:
1. Imports the feature engineering functions
2. Specifies input/output paths
3. Runs the pipeline
4. Reports results

Architecture:
- src/feature_engineering.py = Contains ALL the feature engineering LOGIC and FUNCTIONS
- This file = RUNNER that calls those functions

To run: python scripts/phase_3_engineer_features.py
"""

import sys
sys.path.insert(0, 'src')

from src.feature_engineering import engineer_features


def main():
    input_file = 'data/processed/cleaned_data.csv'
    output_file = 'data/processed/featured_data.csv'

    engineer_features(input_file, output_file)

    print("[DONE] Phase 3 Complete")
    print("[NEXT] Phase 4: Model Training")


if __name__ == '__main__':
    main()
