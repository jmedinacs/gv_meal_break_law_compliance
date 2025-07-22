'''
detect_break_violations.py
Created on Jul 16, 2025

Author: John Medina

This module handles shift duration calculation and violation detection based on California labor law 
compliance rules. It builds on top of the cleaned timecard dataset and flags cases where required 
meal periods were missed or delayed, depending on waiver status and shift length.

The final output includes:
- A new column `shift_length_minutes`
- Compliance check results in `violation_reason`
- A boolean `violation_flag` column for easy filtering
- Saved output file with all computed fields
'''

import cleaning.explore_and_initial_clean as cleaning
import data_utils.data_io as util_data
import pandas as pd 
from data_utils.data_io import save_processed_violation_dataset, load_clean_data
from cleaning.explore_and_initial_clean import convert_time_to_date_time, clean_data


def compute_shift_length(df):
    """
    Computes total shift length in minutes for each row.

    This subtracts clock_in from clock_out and stores the result in 
    a new column called 'shift_length_minutes'. This is the base 
    feature used to determine whether a meal break is required.
    """
    df["shift_length_minutes"] = (df["clock_out"] - df["clock_in"]).dt.total_seconds() / 60
    return df 


def check_for_violation(df):
    """
    Applies California labor logic to flag required meal breaks and possible violations.

    Adds three new columns to the DataFrame:
    - 'lunch_needed': True if the shift length legally requires a meal break
    - 'violation_reason': Explanation for the violation, or 'no_violation' if compliant
    - 'violation_flag': Boolean flag for easy filtering of violations

    Violation logic:
    - No waiver and lunch_start is missing: 'missed_lunch'
    - No waiver and lunch starts after 5 hours: 'late_lunch_no_waiver'
    - Waiver signed but lunch starts after 6 hours: 'late_lunch_waiver'
    """
    
    # Determine if lunch is legally required based on waiver and shift length
    df["lunch_needed"] = (
        (~df["waiver_signed"] & (df["shift_length_minutes"] >= 300)) |   # No waiver: 5h+
        (df["waiver_signed"] & (df["shift_length_minutes"] > 360))       # Waiver: strictly over 6h
    )
    
    # Start by assuming all shifts are compliant
    df["violation_reason"] = "no_violation"
    
    # Case 1: Lunch is needed but lunch_start is missing
    df.loc[
        df["lunch_needed"] & df["lunch_start"].isna(),
        "violation_reason"
    ] = "missed_lunch"
    
    # Case 2: No waiver and lunch started too late
    df.loc[
        (df["lunch_needed"]) &
        (~df["waiver_signed"]) & # Waiver not signed
        (df["lunch_start"] >= df["clock_in"] + pd.Timedelta(hours=5)),
        "violation_reason"
    ] = "late_lunch_no_waiver"
    
    # Case 3: Waiver signed but lunch still exceeded 6-hour rule
    df.loc[
        (df["lunch_needed"]) & 
        (df["waiver_signed"]) & # Waiver signed
        (df["lunch_start"] > df["clock_in"] + pd.Timedelta(hours=6)),
        "violation_reason"
    ] = "late_lunch_waiver"
    
    # Create a simple True/False flag for violations
    df["violation_flag"] = df["violation_reason"] != "no_violation"
    
    return df 

def check_missed_lunch_five_hour_shift(df):
    """
    Counts the number of missed lunch violations that occurred on exactly 5-hour shifts.

    This function helps assess whether employees may be misunderstanding 
    the meal period requirement for 5-hour shifts. Under California law, 
    a meal period is still required unless a valid waiver is signed.

    Parameters:
        df (pd.DataFrame): The processed timecard dataset containing 
            'violation_reason' and 'shift_length_minutes' columns.

    Returns:
        None
    """

    missed_lunch_5hr_count = df[
        (df["violation_reason"]== "missed_lunch") &
        (df["shift_length_minutes"]==300)
    ].shape[0]
    
    print(f"\n5-hour shifts with missed lunch: {missed_lunch_5hr_count}")


def detect_break_violations(filename="missing_name"):
    """
    Main pipeline to detect lunch break violations for a given cleaned timecard dataset.

    Steps:
    1. Loads the cleaned dataset
    2. Inspects and prints structure
    3. Calculates shift length
    4. Flags meal break violations
    5. Saves the processed dataset to the appropriate output folder
    """
    print("\nDetect Break Violations Phase Initialized\n")
    
    # Step 1: Load the cleaned dataset (after initial cleaning stage)
    df = load_clean_data(filename)
    
    # Step 2: Convert time to datetime (saving converts it to string)
    df = convert_time_to_date_time(df)
    
    # Step 3: Quick structure and null check (for transparency)
    cleaning.inspect_data(df)
    
    # Step 3: Add a new column for total shift length
    df = compute_shift_length(df)
    
    # Step 4: Run rule-based logic to flag violations
    df = check_for_violation(df)
    
    # Step 5: Save the enriched dataset with flags and reasoning
    save_processed_violation_dataset(df, filename)
    
    # Optional: Re-inspect to confirm post-processing structure
    cleaning.inspect_data(df)
    
    # Check if 5-hour shifts with missed lunch are significantly represented
    check_missed_lunch_five_hour_shift(df)


if __name__ == '__main__':
    detect_break_violations("timecards_dec_2024")
