"""
Feature Engineering Module - create meaningful predictors for ship type.

This file contains the reusable feature engineering logic for Phase 3.

Features we create:
1. Navigational status one-hot flags
2. Ship size category
3. Length-to-width ratio
4. Ship footprint area
5. Speed category
6. Depth-to-length ratio
7. Course-heading difference

These derived features capture domain knowledge about ships:
- How they move: speed, navigation status, course-heading alignment
- What they look like: size, shape, footprint
- How they sit in water: draft relative to length

Architecture:
- src/feature_engineering.py = reusable logic and functions
- scripts/phase_3_engineer_features.py = runner/entry point
- Phase 4 can import this module before training models

Usage:
  from src.feature_engineering import engineer_features
  engineer_features('input.csv', 'output.csv')
"""

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    'navigationalstatus',
    'sog',
    'cog',
    'heading',
    'shiptype',
    'width',
    'length',
    'draught',
]

NAV_STATUS_BUCKETS = {
    'Under way using engine': 'under_way_engine',
    'Constrained by her draught': 'constrained_by_draught',
    'Engaged in fishing': 'engaged_in_fishing',
    'Moored': 'moored',
    'Restricted maneuverability': 'restricted_maneuverability',
    'Reserved for future amendment [HSC]': 'reserved_hsc',
    'Under way sailing': 'under_way_sailing',
    'At anchor': 'at_anchor',
    'Unknown value': 'unknown',
}


def load_cleaned_data(filepath):
    """Load cleaned data from Phase 2."""
    print(f"[LOADING] Reading cleaned data from {filepath}")
    df = pd.read_csv(filepath)
    print(f"[OK] Loaded {len(df):,} records, {df.shape[1]} columns")
    return df


def validate_feature_inputs(df):
    """
    Confirm the cleaned data has the columns and values Phase 3 expects.

    Why: Feature engineering depends on columns like length and width. If a
    column is missing or a ratio denominator is invalid, we should fail early
    with a clear message instead of silently creating bad features.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for feature engineering: {missing_columns}")

    non_positive_dimensions = df[(df['width'] <= 0) | (df['length'] <= 0)]
    if len(non_positive_dimensions) > 0:
        raise ValueError(
            "Width and length must be positive before creating ratio features. "
            f"Found {len(non_positive_dimensions):,} invalid rows."
        )

    print("[VALIDATION] Required columns present and ratio denominators are valid")
    return df


def encode_navigational_status(df):
    """
    Convert navigational status text into one-hot numerical flags.

    Simple explanation:
    A model cannot directly use text like "Moored". One-hot encoding creates
    separate yes/no columns such as nav_status_moored.

    Technical explanation:
    One-hot encoding avoids fake ordering. An ordinal code like Moored=3 and
    At anchor=7 can accidentally imply that one status is mathematically larger
    than another. One-hot columns preserve category identity without adding
    that false ranking.
    """
    unique_count = df['navigationalstatus'].nunique()
    print(f"\n[FEATURE] One-hot encoding navigational status ({unique_count} unique values)")

    status_bucket = df['navigationalstatus'].map(NAV_STATUS_BUCKETS).fillna('other')
    status_dummies = pd.get_dummies(status_bucket, prefix='nav_status', dtype=int)

    expected_columns = [
        f"nav_status_{bucket}"
        for bucket in list(NAV_STATUS_BUCKETS.values()) + ['other']
    ]

    for column in expected_columns:
        if column not in status_dummies.columns:
            status_dummies[column] = 0

    df = pd.concat([df, status_dummies[expected_columns]], axis=1)

    print(f"  -> Created {len(expected_columns)} one-hot status columns")
    print("  -> Rare/unmodeled statuses grouped into: nav_status_other")

    return df


def create_ship_size_category(df):
    """
    Create ship size category from length.

    Why: Ship size is important for prediction. Categories make it
    interpretable and capture useful non-linear boundaries.

    Categories:
    - 0 Small: < 25m
    - 1 Medium: 25-100m
    - 2 Large: 100-200m
    - 3 Very large: >= 200m
    """
    print("\n[FEATURE] Creating ship size categories (from length)")

    def categorize_size(length):
        if length < 25:
            return 0
        if length < 100:
            return 1
        if length < 200:
            return 2
        return 3

    df['ship_size_category'] = df['length'].apply(categorize_size)

    dist = df['ship_size_category'].value_counts().sort_index()
    print(
        f"  -> Distribution: Small={dist.get(0, 0):,}, "
        f"Medium={dist.get(1, 0):,}, Large={dist.get(2, 0):,}, "
        f"VeryLarge={dist.get(3, 0):,}"
    )

    return df


def create_length_to_width_ratio(df):
    """
    Create length-to-width ratio.

    Why: Different ship types have different shapes. For example, cargo ships
    are usually long and narrow, while some working vessels are shorter and
    wider.
    """
    print("\n[FEATURE] Creating length-to-width ratio")

    df['length_width_ratio'] = df['length'] / df['width']

    print(f"  -> Mean ratio: {df['length_width_ratio'].mean():.2f}")
    print(
        f"  -> Range: {df['length_width_ratio'].min():.2f} "
        f"to {df['length_width_ratio'].max():.2f}"
    )

    return df


def create_ship_footprint_area(df):
    """
    Create ship footprint area from length and width.

    Why: Two ships can have similar lengths but very different widths. Area is
    a compact feature that approximates how much physical space the ship takes.
    """
    print("\n[FEATURE] Creating ship footprint area")

    df['ship_footprint_area'] = df['length'] * df['width']

    print(f"  -> Mean area: {df['ship_footprint_area'].mean():.2f} square meters")
    print(
        f"  -> Range: {df['ship_footprint_area'].min():.2f} "
        f"to {df['ship_footprint_area'].max():.2f}"
    )

    return df


def create_speed_category(df):
    """
    Create speed category from SOG (Speed Over Ground).

    Why: Speed reveals ship activity:
    - 0-2 knots: stationary or drifting
    - 2-8 knots: slow operation
    - 8-15 knots: normal transit
    - 15+ knots: fast movement
    """
    print("\n[FEATURE] Creating speed categories")

    def categorize_speed(sog):
        if sog < 2:
            return 0
        if sog < 8:
            return 1
        if sog < 15:
            return 2
        return 3

    df['speed_category'] = df['sog'].apply(categorize_speed)

    dist = df['speed_category'].value_counts().sort_index()
    print(
        f"  -> Distribution: Stationary={dist.get(0, 0):,}, "
        f"Slow={dist.get(1, 0):,}, Normal={dist.get(2, 0):,}, "
        f"Fast={dist.get(3, 0):,}"
    )

    return df


def create_depth_to_length_ratio(df):
    """
    Create depth-to-length ratio.

    Why: Different ships sit differently in the water. Normalizing draught by
    length makes draft patterns comparable across small and large ships.
    """
    print("\n[FEATURE] Creating depth-to-length ratio")

    df['depth_length_ratio'] = df['draught'] / df['length']

    print(f"  -> Mean ratio: {df['depth_length_ratio'].mean():.4f}")

    return df


def create_course_heading_delta(df):
    """
    Create circular difference between COG and heading.

    Simple explanation:
    COG is where the ship is moving. Heading is where the ship points. The
    difference can reveal drifting, turning, towing, or maneuvering.

    Technical detail:
    Angles wrap around at 360 degrees, so 359 and 1 are only 2 degrees apart,
    not 358. The modulo formula gives the smallest angular difference.
    """
    print("\n[FEATURE] Creating course-heading difference")

    df['course_heading_delta'] = np.abs((df['cog'] - df['heading'] + 180) % 360 - 180)

    print(f"  -> Mean delta: {df['course_heading_delta'].mean():.2f} degrees")
    print(
        f"  -> Range: {df['course_heading_delta'].min():.2f} "
        f"to {df['course_heading_delta'].max():.2f}"
    )

    return df


def drop_original_categorical(df):
    """
    Drop original navigational status column after one-hot encoding.

    Why: The output CSV should be model-ready and numerical.
    """
    df = df.drop('navigationalstatus', axis=1)
    print("\n[CLEANUP] Dropped original 'navigationalstatus' column (using one-hot flags)")

    return df


def print_feature_summary(df):
    """Print summary of engineered features."""
    nav_feature_count = len([col for col in df.columns if col.startswith('nav_status_')])

    print("\n" + "=" * 80)
    print("PHASE 3 FEATURE ENGINEERING SUMMARY")
    print("=" * 80)

    print(f"\nFinal dataset: {len(df):,} records, {df.shape[1]} columns")

    print("\nOriginal numerical features:")
    print("  - sog (speed over ground)")
    print("  - cog (course over ground)")
    print("  - heading (ship heading)")
    print("  - width (ship width)")
    print("  - length (ship length)")
    print("  - draught (ship draft)")

    print("\nTarget variable:")
    print(f"  - shiptype ({df['shiptype'].nunique()} categories)")

    print("\nNew engineered features:")
    print(f"  - nav_status_* ({nav_feature_count} one-hot categorical flags)")
    print("  - ship_size_category (0-3: Small, Medium, Large, VeryLarge)")
    print("  - length_width_ratio (continuous: shape ratio)")
    print("  - ship_footprint_area (continuous: length x width)")
    print("  - speed_category (0-3: Stationary, Slow, Normal, Fast)")
    print("  - depth_length_ratio (continuous: draft normalized by length)")
    print("  - course_heading_delta (continuous: circular angle difference)")

    print("\nReady for Phase 4 (Modeling)")
    print("=" * 80 + "\n")


def engineer_features(input_filepath, output_filepath):
    """
    Run the complete feature engineering pipeline.

    Input: cleaned data CSV from Phase 2
    Output: engineered feature CSV for Phase 4
    """
    print("\n" + "=" * 80)
    print("PHASE 3: FEATURE ENGINEERING PIPELINE")
    print("=" * 80)

    df = load_cleaned_data(input_filepath)
    df = validate_feature_inputs(df)

    print("\n[BEGINNING FEATURE ENGINEERING]")

    df = encode_navigational_status(df)
    df = create_ship_size_category(df)
    df = create_length_to_width_ratio(df)
    df = create_ship_footprint_area(df)
    df = create_speed_category(df)
    df = create_depth_to_length_ratio(df)
    df = create_course_heading_delta(df)
    df = drop_original_categorical(df)

    output_path = Path(output_filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_filepath, index=False)
    print(f"[SAVED] Engineered features to {output_filepath}")

    print_feature_summary(df)

    return df
