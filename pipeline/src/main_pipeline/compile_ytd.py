"""
Year-to-Date Violation Report Compiler
--------------------------------------

This script consolidates all monthly violation summary reports into a single year-to-date (YTD) report
for the Golden Valley timecard compliance pipeline. It scans a designated folder for individual monthly
`*_violation_report.csv` files, merges them into a single DataFrame, and saves the combined result to a
centralized `yearly_report` directory.

Key Features:
- Automatically compiles all available monthly reports for a given year
- Outputs a clean, concatenated CSV ready for Tableau or Excel use
- Supports modular updates without reprocessing historical data
- Designed to support automated reporting workflows and dashboard refreshes

Typical Use Case:
Run this script independently to generate or update the YTD report after a new monthly violation file
has been added to the system, without rerunning the full data pipeline.

Author: John Medina
Created: July 16, 2025
"""


import pandas as pd
import os
from data_utils.data_io import load_violation_summary 


def compile_ytd_violation_summary(report_year="missing_year",report_folder="../../report/monthly_violation_report", output_path ="../../report/yearly_report/2024"):
    """
    Compiles all monthly *_violation_report.csv files into a single YTD summary.

    Args:
        report_folder (str): Path to folder containing monthly violation reports.
        output_path (str): Path to save the compiled YTD summary CSV.

    Returns:
        pd.DataFrame: Combined summary DataFrame.
    """
    
    all_summaries = []
    
    for fname in os.listdir(report_folder):
        full_path = os.path.join(report_folder, fname)
        df = pd.read_csv(full_path)
        all_summaries.append(df)
        
    if not all_summaries:
        print("No violation reports found.")
        return None 
    
    output_path = os.path.join(output_path,"ytd_report_compiled.csv")
    ytd_df = pd.concat(all_summaries, ignore_index=True) 
    ytd_df.to_csv(output_path, index=False)
    print("YTD Summary saved to: yearly_report folder.")
    
    return ytd_df



if __name__ == '__main__':
    compile_ytd_violation_summary() # Recompile ytd report without running the whole pipeline