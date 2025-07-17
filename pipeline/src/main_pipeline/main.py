"""
Golden Valley Timecard Compliance: Monthly Pipeline Execution
--------------------------------------------------------------

This script executes the full data processing pipeline for a single month's timecard data,
including data cleaning, violation detection, and report generation. It also updates the 
year-to-date (YTD) violation summary by compiling all monthly reports to date.

Pipeline Steps:
1. Clean raw timecard data
2. Detect missed or late lunch break violations
3. Generate a monthly summary report
4. Display a preview of the monthly report
5. Compile or update the full YTD report

This script is designed to be run each time a new monthly file is added to the system.

Author: John Medina
Created: July 16, 2025
"""

from cleaning.explore_and_initial_clean import clean_data
from processing.detect_break_violations import detect_break_violations
from processing.violation_summary_report import generate_monthly_violation_report
from data_utils.data_io import load_violation_summary
from main_pipeline.compile_ytd import compile_ytd_violation_summary

from tabulate import tabulate
import os
import sys


def main():
    """
    Executes the full pipeline for a given monthly timecard file:
    - Cleans the data
    - Detects break violations
    - Generates a summary report
    - Displays a preview of the report
    - Compiles an updated year-to-date (YTD) summary
    """
    # Set the target file name (exclude '.csv' extension)
    filename = "timecards_dec_2024"

    # Step 1: Clean the raw timecard data
    clean_data(filename)

    # Step 2: Detect violations related to meal break compliance
    detect_break_violations(filename)

    # Step 3: Generate a monthly summary report
    generate_monthly_violation_report(filename)

    # Step 4: Load and preview the generated report
    df = load_violation_summary(filename)
    print("\nMonthly Violation Report Preview:\n")
    print(tabulate(df.head(10), headers="keys", tablefmt="fancy_grid"))

    # Step 5: Recompile the year-to-date report with the latest month included
    compile_ytd_violation_summary()


if __name__ == '__main__':
    main()
