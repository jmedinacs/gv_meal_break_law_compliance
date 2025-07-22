"""
data_io.py

Handles all input/output operations for the Golden Valley Break Risk Pipeline.

This module centralizes the loading and saving of all datasets and reports used 
throughout the meal break compliance workflow, including:

- Raw timecard data
- Cleaned datasets (with standard formatting and missing value handling)
- Processed data with computed violations (e.g., shift length, waiver status)
- Monthly violation summary reports
- Employee-level reports (both detailed and aggregated)
- Logs for incomplete records (e.g., missing clock-in/clock-out)

All file paths are relative to a standardized project directory structure to 
ensure modularity and portability across clients.

This separation of I/O logic ensures cleaner pipelines, easier testing, and 
centralized maintenance.

Author: John Medina
Created: July 15, 2025
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

def load_detailed_employee_violation_dataset(filename="missing_name"):
    """
    Load a detailed (row-level) employee violation dataset for a given month.

    This function reads a CSV file from the 'detailed' report folder containing
    individual timecard records where a violation was flagged. Each row typically
    represents a shift and includes metadata such as clock times, waiver status, 
    and violation reason.

    Args:
        filename (str): Base name of the file (e.g., 'apr_2024'). Do not include extensions.

    Returns:
        pd.DataFrame: DataFrame with detailed violation records for that month.

    Raises:
        FileNotFoundError: If the expected CSV file is not found in the directory.
    """
    basepath = "../../report/employee_level_violation_report/detailed"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}_employee_violation_report.csv not found!")

    filepath = os.path.join(basepath, f"{filename}_employee_violation_report.csv")
    df = pd.read_csv(filepath)

    if df.shape[1] == 1:
        df = df.squeeze()

    print(f"{filename}_employee_violation_report.csv loaded!")
    return df

def load_aggregated_employee_violation_dataset(filename="missing_name"):
    """
    Load an aggregated (employee-level) violation summary for a given month.

    This function reads a CSV file from the 'aggregated' report folder containing
    violation counts per employee. Each row summarizes how many times an employee 
    triggered each type of violation during the selected month.

    Args:
        filename (str): Base name of the file (e.g., 'apr_2024'). Do not include extensions.

    Returns:
        pd.DataFrame: DataFrame containing one row per employee with violation counts.

    Raises:
        FileNotFoundError: If the expected CSV file is not found in the directory.
    """
    basepath = "../../report/employee_level_violation_report/aggregated"

    if not os.path.exists(basepath):
        raise FileNotFoundError(f"{filename}_aggregated_employee_violation_report.csv not found!")

    filepath = os.path.join(basepath, f"{filename}_aggregated_employee_violation_report.csv")
    df = pd.read_csv(filepath)

    if df.shape[1] == 1:
        df = df.squeeze()

    print(f"{filename}_aggregated_employee_violation_report.csv loaded!")
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
    
def save_detailed_employee_violation_report(df,filename="missing_name"):
    """
    Save the detailed (row-level) employee violation DataFrame to a CSV file.

    This function writes the provided DataFrame to the `detailed` subfolder 
    inside the `employee_level_violation_report` directory. The file includes 
    one row per shift where a violation occurred, with full context for HR or audit review.

    Args:
        df (pd.DataFrame): The DataFrame containing row-level violation records.
        filename (str): The base name for the output file (e.g., 'apr_2024').

    Returns:
        None
    """
    output_path = f"../../report/employee_level_violation_report/detailed/{filename}_employee_violation_report.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"{filename}_employee_violation_report saved to detailed employee level report folder")
    
def save_aggregated_employee_violation_report(df,filename="missing_name"):
    """
    Save the aggregated (employee-level summary) violation DataFrame to a CSV file.

    This function writes the provided DataFrame to the `aggregated` subfolder 
    inside the `employee_level_violation_report` directory. Each row in the 
    output summarizes violation counts for an individual employee.

    Args:
        df (pd.DataFrame): The DataFrame containing aggregated violation counts per employee.
        filename (str): The base name for the output file (e.g., 'apr_2024').

    Returns:
        None
    """
    output_path = f"../../report/employee_level_violation_report/aggregated/{filename}_aggregated_employee_violation_report.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"{filename}_aggregated_employee_violation_report saved to aggregated employee level report folder")
    
def save_employee_level_ytd(df,filename="missing_name"):
    """
    Saves the year-to-date (YTD) employee-level violation summary to a CSV file.

    This function writes the provided aggregated DataFrame to the 
    'employee_ytd' subfolder inside the 'yearly_report' directory. 
    Each row in the output summarizes total violations per employee across all months.

    Parameters:
        df (pd.DataFrame): DataFrame containing YTD violation counts per employee.
        filename (str): Base name for the output file (e.g., '2024').

    Returns:
        None
    """
    output_path = f"../../report/yearly_report/employee_ytd/{filename}_employee_ytd_report.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"{filename}_employee_ytd_report saved to employee ytd folder")
    


if __name__ == '__main__':
    pass  # This module is utility-focused and not meant to be executed directly
