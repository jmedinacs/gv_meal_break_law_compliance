"""
data_io.py

Handles all file input/output operations for the Golden Valley Break Risk Pipeline.

This module centralizes the loading and saving of:
- Raw data (original timecards)
- Cleaned data (after initial preprocessing)
- Processed data with violation flags
- Monthly summary reports
- Logs of rows with missing shift times (for client follow-up)

All paths are standardized and relative to the repo's structure for easy portability.

Author: John Medina
Date: July 15, 2025
"""

import os
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype 



def load_raw_data(filename="missing_name"):
    """
    Loads a raw CSV file from the '../../data/raw/' directory.

    Parameters:
        filename (str): Name of the raw CSV file (no extension)

    Returns:
        pd.DataFrame: Raw dataset

    Raises:
        FileNotFoundError: If the directory is missing
    """
    basepath = "../../data/raw"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}.csv not found!")

    filepath = os.path.join(basepath, f"{filename}.csv")
    df = pd.read_csv(filepath)

    print(f"{filename}.csv loaded!")
    return df


def load_clean_data(filename="missing_name"):
    """
    Loads a cleaned dataset from the '../../data/cleaned/' directory.

    Parameters:
        filename (str): Name of the cleaned file (no extension)

    Returns:
        pd.DataFrame or pd.Series: Cleaned dataset. If only one column, returns as Series.
    """
    basepath = "../../data/cleaned"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}.csv not found!")

    filepath = os.path.join(basepath, f"{filename}_cleaned.csv")
    df = pd.read_csv(filepath)

    if df.shape[1] == 1:
        df = df.squeeze()

    print(f"{filename}_cleaned.csv loaded!")
    return df


def load_processed_violation_dataset(filename="missing_name"):
    """
    Loads a processed dataset with shift violation analysis results.

    Parameters:
        filename (str): File stem (e.g., 'timecards_june_2024')

    Returns:
        pd.DataFrame or pd.Series: Dataset with lunch_needed, violation_reason, etc.
    """
    basepath = "../../data/processed"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}.csv not found!")

    filepath = os.path.join(basepath, f"{filename}_violation_data.csv")
    df = pd.read_csv(filepath)

    if df.shape[1] == 1:
        df = df.squeeze()

    print(f"{filename}_violation_data.csv loaded!")
    return df

def load_violation_summary(filename="missing_name"):
    """
    Loads the summary report for the month.

    Parameters:
        filename (str): File stem (e.g., 'timecards_june_2024')

    Returns:
        pd.DataFrame or pd.Series: Dataset with lunch_needed, violation_reason, etc.
    """
    basepath = "../../report/monthly_violation_report"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}.csv not found!")

    filepath = os.path.join(basepath, f"{filename}_violation_report.csv")
    df = pd.read_csv(filepath)

    if df.shape[1] == 1:
        df = df.squeeze()

    print(f"{filename}_violation_report.csv loaded!")
    return df


def save_clean_data(df, filename="missing_name"):
    """
    Saves a cleaned dataset to the '../../data/cleaned/' directory.

    Parameters:
        df (pd.DataFrame): Cleaned data
        filename (str): Base name (no extension)

    Returns:
        None
    """
    basepath = "../../data/cleaned"
    os.makedirs(basepath, exist_ok=True)
    filepath = os.path.join(basepath, f"{filename}_cleaned.csv")

    # Convert datetime columns to time string format if they are datetime type
    for col in ["clock_in", "lunch_start", "lunch_end", "clock_out"]:
        if col in df.columns and is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%H:%M:%S')

    df.to_csv(filepath, index=False)
    print(f"Saved {filename}_cleaned data to cleaned folder.")


def log_missing_shift_rows(df, filename="missing_name"):
    """
    Logs rows with missing clock_in or clock_out times for client follow-up.

    Parameters:
        df (pd.DataFrame): Rows with incomplete shift data
        filename (str): Base name (no extension)

    Returns:
        None
    """
    basepath = "../../report/missing_log"
    os.makedirs(basepath, exist_ok=True)

    filepath = os.path.join(basepath, f"{filename.lower().replace(' ', '_')}_missing_shift_time.csv")
    df.to_csv(filepath, index=False)

    print(f"\n{filename}_missing_shift_time.csv saved to missing_log folder")


def save_processed_violation_dataset(df, filename="missing_name"):
    """
    Saves the final processed dataset with violation results to the processed folder.

    Parameters:
        df (pd.DataFrame): DataFrame with shift_length, lunch_needed, and violation columns
        filename (str): Base name (no extension)

    Returns:
        None
    """
    basepath = "../../data/processed/"
    os.makedirs(basepath, exist_ok=True)

    filepath = os.path.join(basepath, f"{filename.lower().replace(' ', '_')}_violation_data.csv")
    df.to_csv(filepath, index=False)

    print(f"\n{filename}_violation_data.csv saved to processed folder")


def save_violation_summary(df_summary, filename="missing_name"):
    """
    Saves a one-row monthly summary report to the reports folder.

    Parameters:
        df_summary (pd.DataFrame): One-row summary of violations
        filename (str): Base name (no extension)

    Returns:
        None
    """
    output_path = f"../../report/monthly_violation_report/{filename}_violation_report.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_summary.to_csv(output_path, index=False)

    print(f"{filename}_violation_report saved to monthly violation report folder")


if __name__ == '__main__':
    pass  # This module is utility-focused and not meant to be executed directly
