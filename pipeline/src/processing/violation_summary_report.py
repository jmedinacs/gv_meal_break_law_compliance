'''
violation_summary_report.py
Created on Jul 16, 2025

Author: John Medina

This module generates a high-level monthly summary of lunch break compliance,
based on the processed timecard dataset with violation flags already applied.

The summary includes:
- Total valid shifts
- Number and percentage of violations
- A breakdown by violation type

This summary can be used for quick reporting, internal audits, or Tableau dashboards.
'''

import pandas as pd
from data_utils.data_io import save_violation_summary, load_processed_violation_dataset


def build_violation_summary(df, filename="missing_name"):
    """
    Builds a one-row summary DataFrame with violation statistics for a single month.

    Assumes the dataset contains pre-processed columns like:
    - 'violation_reason'
    - 'date' (used to infer the month)

    Parameters:
    - df: DataFrame containing the processed timecard data
    - filename: Optional label to pass along for logging or custom behavior

    Returns:
    - summary_df: A one-row DataFrame with total shifts, violation counts,
                  percentage of violations, and a breakdown by reason type.
    """
    
    total_shifts = len(df)
    violations = (df["violation_reason"] != "no_violation").sum()
    pct_violations = round(violations / total_shifts * 100, 1)
    
    # Count how many violations of each type occurred
    reason_counts = df["violation_reason"].value_counts().to_dict()
    
    summary = {
        "month": df["date"].iloc[0][:7],  # Assumes all data belongs to the same month
        "total_shifts": total_shifts,
        "violations": violations,
        "pct_violations": pct_violations,
        "missed_lunch": reason_counts.get("missed_lunch", 0),
        "late_lunch_no_waiver": reason_counts.get("late_lunch_no_waiver", 0),
        "late_lunch_waiver": reason_counts.get("late_lunch_waiver", 0)
    }
    
    return pd.DataFrame([summary])


def generate_monthly_violation_report(filename="missing_name"):
    """
    Loads the processed violation dataset and generates a monthly summary CSV.

    Steps:
    1. Loads the post-violation-logic dataset
    2. Builds a one-line summary of violation metrics
    3. Saves the summary to the reports folder using standard filename convention

    Parameters:
    - filename: Name of the dataset (e.g., 'timecards_june_2024') without the full path
    """
    print("\nGenerating Monthly Violation Summary Report\n")
    
    # Step 1: Load processed dataset with violation flags and reasons
    df = load_processed_violation_dataset(filename)

    # Step 2: Build a single-row summary from the DataFrame
    df_summary = build_violation_summary(df, filename)

    # Step 3: Save summary to ../../data/reports/
    save_violation_summary(df_summary, filename)


if __name__ == '__main__':
    generate_monthly_violation_report(filename="timecards_july_2024")
