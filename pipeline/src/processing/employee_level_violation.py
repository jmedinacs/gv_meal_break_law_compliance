"""
employee_violation_reports.py

This module generates employee-level violation reports for meal break compliance.
It processes a cleaned and violation-tagged timecard dataset to produce:

1. A detailed (row-level) report of all shifts where violations occurred.
2. An aggregated (employee-level) summary report of violation counts by type.

Outputs are saved in pre-defined 'detailed' and 'aggregated' report folders, respectively.
These reports support HR, legal, and operational analysis for ongoing compliance tracking.

Created on Jul 19, 2025
@author: jarpy
"""

from data_utils.data_io import (
    load_processed_violation_dataset,
    save_detailed_employee_violation_report,
    save_aggregated_employee_violation_report
)

def aggregate_employee_violations(df, filename="missing_name"):
    """
    Aggregate meal break violations by employee and save a summary report.

    This function generates a DataFrame that summarizes each employee's
    violation counts by type (missed lunch, late with/without waiver)
    and a total count. Only employees with at least one violation are included.

    Args:
        df (pd.DataFrame): A filtered DataFrame containing only rows with violations.
                           Must include 'employee_id' and 'violation_reason'.
        filename (str): Base name used for saving the output CSV file (e.g., 'apr_2024').

    Returns:
        None
    """
    # Count types of violations per employee (creates a column for each type)
    violation_counts = (
        df
        .groupby(["employee_id", "violation_reason"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Ensure all expected violation types exist (add zeros if any are missing this month)
    for col in ["missed_lunch", "late_lunch_no_waiver", "late_lunch_waiver"]:
        if col not in violation_counts.columns:
            violation_counts[col] = 0

    # Add total violation count across all types
    violation_counts["total_violations"] = violation_counts[
        ["missed_lunch", "late_lunch_no_waiver", "late_lunch_waiver"]
    ].sum(axis=1)

    # Save to the aggregated report folder
    save_aggregated_employee_violation_report(violation_counts, filename)
    print(f"detailed employee level violation for {filename} saved to report folder.")


def create_violation_list(df, filename="missing_name"):
    """
    Filter the dataset to include only rows where a violation occurred,
    and save a row-level report for HR or auditing use.

    Args:
        df (pd.DataFrame): The full timecard DataFrame including 'violation_flag' column.
        filename (str): Base name used for saving the output CSV file.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only violation rows.
    """
    # Filter for shifts where violation_flag is True
    df_violations = df[df["violation_flag"] == True].copy()

    # Save to the detailed report folder
    save_detailed_employee_violation_report(df_violations, filename)
    print(f"detailed aggregated employee level violation for {filename} saved to report folder.")

    return df_violations


def process_employee_level_analysis(filename="missing_name"):
    """
    Run the full employee-level reporting workflow for a given dataset.

    This function performs the complete analysis pipeline:
    - Loads the processed (violation-tagged) timecard dataset
    - Creates a detailed list of violation rows
    - Aggregates employee-level violation counts
    - Saves both reports to their respective output folders

    Args:
        filename (str): Base name of the dataset to load (e.g., 'apr_2024' or 'timecards_jan_2024').

    Returns:
        None
    """
    # Load the cleaned and violation-tagged timecard dataset
    df = load_processed_violation_dataset(filename)

    # Create and save a detailed list of all shifts with violations
    df_violations = create_violation_list(df, filename)

    # Aggregate and save a summary report by employee
    aggregate_employee_violations(df_violations, filename)


if __name__ == '__main__':
    # Run the employee-level report generator for the specified file
    process_employee_level_analysis(filename="timecards_dec_2024")
