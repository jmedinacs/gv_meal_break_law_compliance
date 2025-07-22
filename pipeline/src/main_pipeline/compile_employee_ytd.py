"""
compile_employee_ytd.py

Generates a year-to-date (YTD) employee-level violation summary by aggregating 
monthly pre-processed employee violation reports.

This script loads all CSVs from the 'aggregated' reports folder, where each file 
contains per-employee violation counts for a specific month. It combines these 
files, groups by employee_id, and sums all numeric violation columns to produce 
a comprehensive YTD view of employee compliance.

The final summary is saved as a CSV to the 'yearly_report/employee_ytd/' directory.

Usage:
    Run this script directly or call compile_employee_ytd() from a parent pipeline script.

Assumptions:
    - All monthly reports follow the naming convention:
      timecards_<month_year>_aggregated_employee_violation_report.csv
    - All relevant files are stored in:
      ../../report/employee_level_violation_report/aggregated/

Output:
    - A single CSV file summarizing total violations per employee for the entire year.

Author: John Medina
Date: July 21, 2025
"""


import os
import pandas as pd
import data_utils.data_io as dataIO


def compile_employee_ytd(ytd_filename="employee_ytd_2024"):
    """
    Compiles a year-to-date (YTD) violation summary for all employees by 
    combining monthly aggregated employee-level reports.

    This function loads all monthly CSVs from the 'aggregated' report folder,
    concatenates them, and summarizes total violations per employee.

    Parameters:
        filename (str): Base name for the output file (no extension).

    Returns:
        pd.DataFrame: Final YTD summary DataFrame with one row per employee
    """
    aggregated_dir = "../../report/employee_level_violation_report/aggregated"
    files = [
        f for f in os.listdir(aggregated_dir)
        if f.endswith("_aggregated_employee_violation_report.csv")
    ]

    if not files:
        print("No aggregated employee reports found.")
        return None

    all_months = []

    for file in files:
        filepath = os.path.join(aggregated_dir, file)
        try:
            df = pd.read_csv(filepath)
            all_months.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Combine all months into one DataFrame
    full_df = pd.concat(all_months, ignore_index=True)

    # Group by employee and sum all numeric columns
    ytd_df = full_df.groupby("employee_id").sum(numeric_only=True).reset_index()
    ytd_df.sort_values(by="total_violations", ascending=False, inplace=True)

    # Save to yearly report folder using your data_io method
    dataIO.save_employee_level_ytd(ytd_df, ytd_filename)

    return ytd_df


if __name__ == '__main__':
    compile_employee_ytd(ytd_filename="2024")
