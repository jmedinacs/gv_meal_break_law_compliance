"""
Data Cleaning Script for Timecard Compliance Pipeline
-----------------------------------------------------
This module handles the initial cleaning steps for the Golden Valley timecard dataset.
Key tasks include:
- Inspecting the raw data
- Converting time strings to datetime objects
- Logging and removing rows with missing shift start/end times
- Imputing missing lunch start times when lunch end is available

Intended for use in the gv_break_risk_pipeline project.

Author: John Medina
Created: July 15, 2025
"""

from data_utils.data_io import load_raw_data, save_clean_data, log_missing_shift_rows
from datetime import timedelta
import pandas as pd 


def inspect_data(df):
    """
    Prints basic data inspection results, including:
    - DataFrame info
    - Summary statistics
    - Count of missing values per column

    Args:
        df (pd.DataFrame): The DataFrame to inspect.

    Returns:
        None
    """
    print(df.info())
    print(df.describe())
    print(df.isnull().sum())


def handle_missing_shift_rows(df, filename="missing_name"):
    """
    Logs and removes rows with missing clock_in or clock_out values.
    These rows are unusable for compliance checks or calculating shift length.

    Args:
        df (pd.DataFrame): Input timecard data.
        filename (str): Filename prefix used for logging the excluded rows.

    Returns:
        pd.DataFrame: Cleaned DataFrame excluding invalid rows.
    """
    # Identify rows with either clock_in or clock_out missing
    mask_missing = df["clock_in"].isna() | df["clock_out"].isna()
    df_missing = df[mask_missing].copy()

    # Tag issue reason for logging
    df_missing["issue_reason"] = df_missing.apply(
        lambda row: "Missing clock_in" if pd.isna(row["clock_in"])
        else "Missing clock_out" if pd.isna(row["clock_out"])
        else "Missing both", axis=1
    )

    print("Missing shift count: ",len(df_missing))
    # Save excluded rows to a log
    log_missing_shift_rows(df_missing, filename)

    # Return only rows with complete shift times
    return df[~mask_missing].copy()


def impute_lunch_start(df):
    """
    Imputes missing lunch_start values when lunch_end is available by subtracting 30 minutes.

    Args:
        df (pd.DataFrame): Input DataFrame with time columns.

    Returns:
        pd.DataFrame: DataFrame with imputed lunch_start values where applicable.
    """
    # Identify rows where lunch_start is missing but lunch_end is present
    mask = df["lunch_start"].isna() & df["lunch_end"].notna()

    # Impute lunch_start as 30 minutes before lunch_end
    df.loc[mask, "lunch_start"] = df.loc[mask, "lunch_end"] - timedelta(minutes=30)

    return df


def convert_time_to_date_time(df):
    """
    Converts clock and lunch columns from string to datetime objects using format %H:%M:%S.

    Args:
        df (pd.DataFrame): DataFrame with raw time strings.

    Returns:
        pd.DataFrame: DataFrame with converted datetime columns.
    """
    time_format = "%H:%M:%S"

    df["lunch_end"] = pd.to_datetime(df["lunch_end"], format=time_format, errors="coerce")
    df["lunch_start"] = pd.to_datetime(df["lunch_start"], format=time_format, errors="coerce")
    df["clock_in"] = pd.to_datetime(df["clock_in"], format=time_format, errors="coerce")
    df["clock_out"] = pd.to_datetime(df["clock_out"], format=time_format, errors="coerce")

    return df


def clean_data(filename="missing_name"):
    """
    Master function to execute all cleaning steps on the input dataset.

    Steps:
    1. Load the raw dataset from file
    2. Inspect structure, stats, and missing data
    3. Convert all time-related columns to datetime
    4. Log and remove rows missing shift start or end
    5. Check and impute missing lunch_start (if lunch_end exists)
    6. Save cleaned data

    Args:
        filename (str): The name of the raw CSV file (without .csv extension).

    Returns:
        None
    """
    # STEP 1: Load raw timecard data
    df = load_raw_data(filename)

    # STEP 2: View structure and nulls for initial validation
    inspect_data(df)

    # STEP 3: Convert all time fields to datetime for safe calculations
    df = convert_time_to_date_time(df)

    # STEP 4: Remove rows with missing shift start or end times (log them for review)
    df = handle_missing_shift_rows(df, filename)
    
    # Step 5: Impute missing lunch start if a corresponding lunch_end exists
    df = impute_lunch_start(df)

    # Optional save: Uncomment when ready to persist cleaned data
    #save_clean_data(df, filename)
    
    return df


if __name__ == '__main__':
    clean_data("timecards_dec_2024")
