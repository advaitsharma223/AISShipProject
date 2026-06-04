"""
Data Preprocessing Module - THE ACTUAL CLEANING LOGIC

THIS FILE CONTAINS THE ACTUAL CLEANING OPERATIONS.
Each function performs a specific cleaning task based on decisions in DECISION_LOG.md.

Functions are reusable - imported by scripts/ files for execution.

Cleaning pipeline order:
1. load_raw_data() - Read CSV
2. remove_duplicate_rows() - Remove duplicates
3. handle_draught_missing() - Remove rows with missing draught (Decision 5)
4. handle_heading_missing() - Fill with median by ship type (Decision 6)
5. handle_width_length_missing() - Fill with median by ship type (Decision 7)
6. validate_ranges() - Remove out-of-range outliers
7. clean_data() - Main orchestrator combining all above

Architecture:
- This file (src/preprocessing.py) = LOGIC & FUNCTIONS
- Called by: scripts/phase_2_clean_data.py = RUNNER/ENTRY POINT
- Can also be imported by other phases (Phase 3, 4, etc.)

Usage:
  from src.preprocessing import clean_data
  clean_data('input.csv', 'output.csv')
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data(filepath):
    """Load raw AIS data from CSV."""
    print(f"[LOADING] Reading data from {filepath}")
    df = pd.read_csv(filepath)
    print(f"[OK] Loaded {len(df):,} records, {df.shape[1]} columns")
    return df


def remove_duplicate_rows(df):
    """Remove exact duplicate rows."""
    initial_count = len(df)
    df = df.drop_duplicates()
    removed = initial_count - len(df)

    if removed > 0:
        print(f"[CLEANING] Removed {removed} duplicate rows")
    else:
        print(f"[INFO] No duplicates found")

    return df


def handle_draught_missing(df):
    """
    DECISION 5: Remove rows with missing draught (7.1% of data).

    Rationale: Draught has sparse/unreliable reporting. Ships that don't report
    draught may be unreliable reporters overall. Better to have 330K high-quality
    records than 358K with guessed data.

    Trade-off: 7% data loss for higher quality.
    """
    initial_count = len(df)
    before_draught = len(df)

    # Remove rows with missing draught
    df = df.dropna(subset=['draught'])

    removed = before_draught - len(df)
    pct_removed = (removed / initial_count) * 100

    print(f"[CLEANING] Removed {removed:,} rows with missing draught ({pct_removed:.1f}%)")

    return df


def handle_heading_missing(df):
    """
    DECISION 6: Fill missing heading with median by ship type (5.8% of data).

    Rationale: Heading is predictable by ship type (Cargo ships move differently
    than Fishing boats). Only 5.8% missing (acceptable). Filling by type preserves
    realistic patterns without assuming global uniformity.

    Trade-off: Creates some artificial data, but preserves 5.8% of records with
    realistic values.
    """
    before = df['heading'].isnull().sum()

    # Fill with median heading for each ship type
    df['heading'] = df.groupby('shiptype')['heading'].transform(
        lambda x: x.fillna(x.median())
    )

    after = df['heading'].isnull().sum()
    filled = before - after

    print(f"[CLEANING] Filled {filled:,} missing heading values with median by ship type")

    return df


def handle_width_length_missing(df):
    """
    DECISION 7: Fill missing width/length with median by ship type (1% of data).

    Rationale: Width/Length are engineering specs - standardized by ship type.
    Every Cargo ship of a type is roughly same size. Only 1% missing (minimal).

    Trade-off: Creates artificial data, but width/length are highly predictable.
    """
    for col in ['width', 'length']:
        before = df[col].isnull().sum()

        # Fill with median for each ship type
        df[col] = df.groupby('shiptype')[col].transform(
            lambda x: x.fillna(x.median())
        )

        after = df[col].isnull().sum()
        filled = before - after

        if filled > 0:
            print(f"[CLEANING] Filled {filled:,} missing {col} values with median by ship type")

    return df


def handle_sog_cog_missing(df):
    """
    Handle missing SOG/COG - very small percentages (<1%).

    Decision: Remove rows with missing SOG or COG.
    Rationale: Speed and course are navigation-critical. Ships that don't report
    these are likely unreliable. Better to remove than guess.
    """
    initial = len(df)

    # Remove rows with missing SOG or COG
    df = df.dropna(subset=['sog', 'cog'])

    removed = initial - len(df)
    if removed > 0:
        print(f"[CLEANING] Removed {removed:,} rows with missing SOG/COG")

    return df


def validate_ranges(df):
    """
    Validate that numerical features are in realistic ranges.
    Remove outliers/errors.
    """
    initial = len(df)

    # Speed: 0-50 knots is realistic (max is ~60 for fastest ships)
    df = df[(df['sog'] >= 0) & (df['sog'] <= 60)]

    # Course/Heading: 0-360 degrees (enforced by AIS, but check anyway)
    df = df[(df['cog'] >= 0) & (df['cog'] <= 360)]
    df = df[(df['heading'] >= 0) & (df['heading'] <= 360)]

    # Ship dimensions: reasonable ranges in meters
    df = df[(df['width'] > 0) & (df['width'] <= 500)]  # Max width ~500m
    df = df[(df['length'] > 0) & (df['length'] <= 500)]  # Max length ~500m
    df = df[(df['draught'] > 0) & (df['draught'] <= 50)]  # Max draft ~50m

    removed = initial - len(df)
    if removed > 0:
        print(f"[CLEANING] Removed {removed:,} rows with out-of-range values")

    return df


def drop_unnecessary_columns(df):
    """Remove columns not needed for modeling."""
    # Drop the index column that came from CSV
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Drop MMSI (it's just a unique ID, not a feature)
    if 'mmsi' in df.columns:
        df = df.drop('mmsi', axis=1)

    print(f"[CLEANING] Dropped unnecessary columns (index, MMSI)")

    return df


def print_cleaning_summary(df_before, df_after):
    """Print summary of cleaning operations."""
    records_removed = len(df_before) - len(df_after)
    pct_removed = (records_removed / len(df_before)) * 100

    print("\n" + "="*80)
    print("PHASE 2 CLEANING SUMMARY")
    print("="*80)
    print(f"\nRecords before: {len(df_before):,}")
    print(f"Records after:  {len(df_after):,}")
    print(f"Records removed: {records_removed:,} ({pct_removed:.1f}%)")

    print(f"\nMissing data after cleaning:")
    missing = df_after.isnull().sum()
    if missing.sum() == 0:
        print(f"  ZERO missing values - data is clean!")
    else:
        for col, count in missing[missing > 0].items():
            print(f"  {col}: {count:,}")

    print(f"\nFinal dataset: {len(df_after):,} records ready for Phase 3")
    print("="*80 + "\n")


def clean_data(input_filepath, output_filepath):
    """
    Main orchestrator - runs complete cleaning pipeline.

    Input: Raw data CSV
    Output: Cleaned data CSV
    """
    print("\n" + "="*80)
    print("PHASE 2: DATA CLEANING PIPELINE")
    print("="*80 + "\n")

    # Load
    df = load_raw_data(input_filepath)
    initial_df = df.copy()

    # Clean (in order)
    print("\n[STEP 1] Removing duplicates")
    df = remove_duplicate_rows(df)

    print("\n[STEP 2] Handling missing draught (Decision 5)")
    df = handle_draught_missing(df)

    print("\n[STEP 3] Handling missing heading (Decision 6)")
    df = handle_heading_missing(df)

    print("\n[STEP 4] Handling missing width/length (Decision 7)")
    df = handle_width_length_missing(df)

    print("\n[STEP 5] Handling missing SOG/COG")
    df = handle_sog_cog_missing(df)

    print("\n[STEP 6] Validating value ranges")
    df = validate_ranges(df)

    print("\n[STEP 7] Dropping unnecessary columns")
    df = drop_unnecessary_columns(df)

    # Save
    output_path = Path(output_filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_filepath, index=False)
    print(f"\n[SAVED] Cleaned data to {output_filepath}")

    # Summary
    print_cleaning_summary(initial_df, df)

    return df
