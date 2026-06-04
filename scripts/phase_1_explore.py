"""
Phase 1: AIS Dataset Exploration
=================================

This script explores the AIS dataset to understand its structure,
quality, and characteristics before modeling.

Run with: python explore_data.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configure display and plotting
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)


def load_data():
    """Load the raw AIS data from CSV."""
    data_path = Path('data/raw/ais_data.csv')
    df = pd.read_csv(data_path)
    print(f"[OK] Data loaded successfully")
    print(f"  Shape: {df.shape[0]:,} rows, {df.shape[1]} columns\n")
    return df


def show_first_look(df):
    """Display basic information about the dataset."""
    print("="*80)
    print("STEP 1: FIRST LOOK AT DATA")
    print("="*80)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\n" + "="*80)
    print("\nData types and Info:")
    print(df.info())
    print()


def analyze_missing_data(df):
    """Analyze missing data in the dataset."""
    print("\n" + "="*80)
    print("STEP 2: MISSING DATA ANALYSIS")
    print("="*80)

    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    missing_summary = pd.DataFrame({
        'Missing_Count': missing,
        'Missing_Percentage': missing_pct
    }).sort_values('Missing_Percentage', ascending=False)

    print("\nMissing Data Summary:")
    print(missing_summary)

    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    missing_summary['Missing_Percentage'].plot(kind='barh', ax=ax, color='coral')
    ax.set_xlabel('Percentage Missing (%)')
    ax.set_title('Missing Data by Column')
    plt.tight_layout()
    plt.savefig('reports/01_missing_data.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Visualization saved: reports/01_missing_data.png")
    plt.close()


def analyze_target(df):
    """Analyze the target variable (shiptype)."""
    print("\n" + "="*80)
    print("STEP 3: TARGET VARIABLE ANALYSIS - SHIP TYPE DISTRIBUTION")
    print("="*80)

    ship_type_counts = df['shiptype'].value_counts()
    ship_type_pct = df['shiptype'].value_counts(normalize=True) * 100

    print(f"\nTotal unique ship types: {df['shiptype'].nunique()}\n")
    print("Counts and Percentages:")
    for ship_type, count in ship_type_counts.items():
        pct = ship_type_pct[ship_type]
        print(f"  {ship_type:20s}: {count:8,} records ({pct:5.2f}%)")

    # Check balance
    if ship_type_pct.min() / ship_type_pct.max() < 0.2:
        print("\n[WARNING]  WARNING: Data is highly imbalanced!")
        print(f"   Most common: {ship_type_pct.idxmax()} ({ship_type_pct.max():.1f}%)")
        print(f"   Least common: {ship_type_pct.idxmin()} ({ship_type_pct.min():.1f}%)")
        print("   This will affect modeling!")

    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ship_type_counts.plot(kind='bar', ax=axes[0], color='steelblue')
    axes[0].set_title('Ship Type Counts')
    axes[0].set_ylabel('Number of Records')
    axes[0].set_xlabel('Ship Type')
    axes[0].tick_params(axis='x', rotation=45)

    ship_type_pct.plot(kind='pie', ax=axes[1], autopct='%1.1f%%')
    axes[1].set_title('Ship Type Distribution (%)')
    axes[1].set_ylabel('')

    plt.tight_layout()
    plt.savefig('reports/02_ship_type_distribution.png', dpi=300, bbox_inches='tight')
    print("[OK] Visualization saved: reports/02_ship_type_distribution.png")
    plt.close()


def analyze_numerical_features(df):
    """Analyze numerical features."""
    print("\n" + "="*80)
    print("STEP 4: NUMERICAL FEATURES ANALYSIS")
    print("="*80)

    numerical_cols = ['sog', 'cog', 'heading', 'width', 'length', 'draught']

    print("\nStatistical Summary:")
    print(df[numerical_cols].describe())

    # Detailed statistics
    print("\n\nDetailed Statistics by Column:")
    for col in numerical_cols:
        print(f"\n{col}:")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Std Dev: {df[col].std():.2f}")
        print(f"  Min: {df[col].min():.2f}")
        print(f"  Max: {df[col].max():.2f}")
        print(f"  Missing: {df[col].isnull().sum()} ({(df[col].isnull().sum()/len(df))*100:.1f}%)")

    # Visualize distributions
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, col in enumerate(numerical_cols):
        data = df[col].dropna()
        axes[idx].hist(data, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'Distribution of {col}')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')

        mean_val = data.mean()
        median_val = data.median()
        axes[idx].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        axes[idx].axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.2f}')
        axes[idx].legend()

    plt.tight_layout()
    plt.savefig('reports/03_numerical_distributions.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Visualization saved: reports/03_numerical_distributions.png")
    plt.close()


def compare_ship_types(df):
    """Compare features across ship types - YOUR KEY QUESTION."""
    print("\n" + "="*80)
    print("STEP 5: YOUR KEY QUESTION - SHIP TYPE CHARACTERISTICS")
    print("What are the common characteristics of different ship types?")
    print("="*80)

    numerical_cols = ['sog', 'cog', 'heading', 'width', 'length', 'draught']

    print("\nAverage Features by Ship Type:")
    print("="*80)
    ship_type_features = df.groupby('shiptype')[numerical_cols].mean()
    print(ship_type_features.round(2))

    print("\n\nKey Insights - Which ship types stand out:")
    for col in numerical_cols:
        max_type = ship_type_features[col].idxmax()
        min_type = ship_type_features[col].idxmin()
        max_val = ship_type_features[col].max()
        min_val = ship_type_features[col].min()

        print(f"\n{col}:")
        print(f"  Highest: {max_type} ({max_val:.2f})")
        print(f"  Lowest: {min_type} ({min_val:.2f})")
        print(f"  Difference: {max_val - min_val:.2f} (This shows {col} VARIES by ship type!)")

    # Box plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, col in enumerate(numerical_cols):
        data_to_plot = df[[col, 'shiptype']].dropna()
        sns.boxplot(data=data_to_plot, x='shiptype', y=col, ax=axes[idx])
        axes[idx].set_title(f'{col} by Ship Type')
        axes[idx].tick_params(axis='x', rotation=45)
        axes[idx].set_xlabel('Ship Type')
        axes[idx].set_ylabel(col)

    plt.tight_layout()
    plt.savefig('reports/04_features_by_ship_type.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Visualization saved: reports/04_features_by_ship_type.png")
    plt.close()


def analyze_categorical_features(df):
    """Analyze categorical features."""
    print("\n" + "="*80)
    print("STEP 6: CATEGORICAL FEATURES ANALYSIS")
    print("="*80)

    print("\nNavigational Status Distribution:")
    nav_status = df['navigationalstatus'].value_counts()
    print(nav_status)

    # Visualize
    fig, ax = plt.subplots(figsize=(12, 6))
    nav_status.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_title('Distribution of Navigational Status')
    ax.set_ylabel('Count')
    ax.set_xlabel('Status')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('reports/05_navigational_status.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Visualization saved: reports/05_navigational_status.png")
    plt.close()


def print_summary(df):
    """Print final summary."""
    print("\n\n")
    print("="*80)
    print("PHASE 1 EXPLORATION SUMMARY")
    print("="*80)

    print(f"\n[DATA] DATASET SIZE")
    print(f"  • Total records: {len(df):,}")
    print(f"  • Total features: {df.shape[1]}")
    print(f"  • Target variable: shiptype")

    print(f"\n[BALANCE] CLASS BALANCE")
    print(f"  • Unique ship types: {df['shiptype'].nunique()}")
    ship_type_pct = df['shiptype'].value_counts(normalize=True) * 100
    max_pct = ship_type_pct.max()
    min_pct = ship_type_pct.min()
    print(f"  • Most common: {max_pct:.1f}% of data")
    print(f"  • Least common: {min_pct:.1f}% of data")
    if min_pct / max_pct < 0.2:
        print(f"  • [WARNING]  IMBALANCED DATA - will need to handle in modeling")

    print(f"\n[ALERT] MISSING DATA")
    missing_pct = (df.isnull().sum().sum() / (len(df) * df.shape[1])) * 100
    print(f"  • Overall missing: {missing_pct:.1f}%")
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        if null_pct > 0:
            print(f"  • {col}: {null_pct:.1f}% missing")

    print(f"\n[INSIGHT] KEY INSIGHTS")
    print(f"  • Different ship types have different typical characteristics")
    print(f"  • Features show clear patterns by ship type")
    print(f"  • Some features have more missing data than others")
    print(f"  • Data is ready for cleaning phase")

    print(f"\n[DONE] NEXT STEPS (Phase 2)")
    print(f"  1. Handle missing values strategically")
    print(f"  2. Check for and handle outliers")
    print(f"  3. Prepare clean dataset for feature engineering")

    print("\n" + "="*80)
    print("Phase 1 Complete!")
    print("="*80)
    print("\nAll visualizations saved to: reports/")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("AIS SHIP PREDICTION - PHASE 1: DATASET EXPLORATION")
    print("="*80 + "\n")

    # Load data
    df = load_data()

    # Run analyses
    show_first_look(df)
    analyze_missing_data(df)
    analyze_target(df)
    analyze_numerical_features(df)
    compare_ship_types(df)
    analyze_categorical_features(df)

    # Print summary
    print_summary(df)

    print("\n[OK] All visualizations saved to reports/ folder")
    print("[OK] Ready for Phase 2: Data Cleaning\n")


if __name__ == '__main__':
    main()