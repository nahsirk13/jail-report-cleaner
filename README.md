# Jail Report Cleaner

This script cleans and processes monthly jail population Excel files and saves them as cleaned CSVs. It standardizes column names, fixes data types, adds a report date column, and cleans up the jurisdiction names.

## What I Did

I started by writing down the steps I thought I'd need, then built the script using functions for each part. Having separate modular functions made it easier to test pieces one at a time and also reuse them later if needed. For example, to build the `report_date`, I first converted the year and month columns to strings, combined them into dates, and adjusted them to the last day of the month.

## Notes and Fixes

- Some jurisdiction names didn’t include “sheriff” like I expected — I found others like “corrections” and “work furlough” and added checks for those too.
- To keep things fast and readable, I used `df["column"]` indexing which is efficient.
- For fixing types, I noticed columns with `#` in the name were usually numeric. I made a function to test printing those columns so I could easily look through them before converting them.
- I used keyword matching to cast columns by type (like anything with “date” was changed to datetime). I made helper functions for this so I didn’t have to do it manually for 50+ columns.
- When cleaning some fields row-by-row, I used lists and rebuilt the column after processing.

## Assumptions I Made

- Every file has `reporting_year` and `reporting_month`
- Jurisdiction names include either “sheriff”, “correction”, or “work”
- Column names are messy but follow some keyword patterns

## How I Checked It Worked

I printed out dtypes before and after to make sure conversions looked right. I also checked the row counts stayed the same and printed any jurisdiction names that didn’t match the expected patterns.

## Running the Script

1. Put your Excel files in the `data/` folder
2. Run:
   ```bash
   python clean_monthly_jail_report.py
