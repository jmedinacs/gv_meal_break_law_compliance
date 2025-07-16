'''
Created on Jul 16, 2025

@author: jarpy
'''

from cleaning.explore_and_initial_clean import clean_data
from processing.detect_break_violations import detect_break_violations
from processing.violation_summary_report import generate_monthly_violation_report
from data_utils.data_io import load_violation_summary
from tabulate import tabulate
import os 
import sys


def main():
    """ """
    filename="timecards_test_case" # Change to appropriate file name WITHOUT the .csv
    
    # Step 1: Clean the raw data. Assumption: raw data is in the data/raw folder
    clean_data(filename)
    
    # Step 2: Analyze data for violations
    detect_break_violations(filename)
    
    # Step 3: Create violation summary report
    generate_monthly_violation_report(filename)
    
    # Step 4: Load the monthly report and preview
    df = load_violation_summary(filename)
    
    # Step 5: Pretty print the actual contents of the report (not a summary)
    print("\n📄 Monthly Violation Report Preview:\n")
    print(tabulate(df.head(10), headers='keys', tablefmt='fancy_grid'))
    
    
    


if __name__ == '__main__':
    main()