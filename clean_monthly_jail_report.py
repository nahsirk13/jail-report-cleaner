import pandas as pd   #using alias "pd" for easy referencing
import numpy as np
import calendar
from datetime import date


#
    # params: filepath (String), n_preview_rows (int)
    # n_preview_rows - optional param set to 3 by default, prints preview rows to console
    #
def load_excel_file(filepath, n_preview_rows=3):
    data_frame = pd.read_excel(filepath)
    print ("Loaded file: ", filepath)
    print("\tShape (Rows x Columns): ", data_frame.shape)
    print("\tPreview Rows: \n", data_frame.head(n_preview_rows))

    return data_frame


    #params
def make_columns_to_snake_case(columns):
    columns = columns.str.strip()  #remove leading and trailing spaces
    columns = columns.str.lower()  #chars to lowercase
    columns = columns.str.replace(' ', '_') # replace
    return columns


    #  Takes in dataframe, returns dataframe with report_date column as first column in date time format
    #              and deletes reporting_year & reporting_month columns
    #  params: data_frame
    #  NOTE: calls get_first_day_of_month function
    #  NOTE: this function assumes the column names are already in snake case

def make_report_date_column(data_frame):

    # convert year and month columns to string
    year_str = data_frame["reporting_year"].astype(str)
    month_str = data_frame["reporting_month"].astype(str)

    # make report date string series, adjust to date time and adjust to last of month
    report_date_strings = year_str + "-" + month_str + "-" + "01"    #for now set day to first of month
    report_date_series = pd.to_datetime(report_date_strings) + pd.offsets.MonthEnd(0)

    #insert report_date column into dataframe
    data_frame.insert(0, "report_date", report_date_series)

    # delete old columns, axis=1 means deleting column and not row
    data_frame = data_frame.drop(["reporting_month", "reporting_year"], axis=1)

    return data_frame


    # Only keeps county name in jurisdiction name column. Assumes column names in snakecase and general format
    #      of jurisdiction name in "<county name> Sherrif's ...> format, raises value error if not.
    #      Also makes sure the column is second column in dataframe.

def clean_jurisdiction_name(data_frame):
    jurisdiction_strings = data_frame["jurisdiction_name"].astype(str)  #series of strings with jurisdiction names
    cleaned_list = []        # store temporarily in list of strings and iterate
    for name in jurisdiction_strings:
        if "sheriff" in name.lower():
            index = name.lower().find("sheriff")   # find index at start of sheriff
        elif "correction" in name.lower():
            index = name.lower().find("correction")
        elif "work" in name.lower():
            index = name.lower().find("work")
        else:
            print("Debug:", name.lower(), "/n")   #debugging line
            raise ValueError("jurisdiction_name has name without 'sheriff', please check input")
        cleaned_name = name[:index].strip() # separate from beginning of string ending at index of 'sheriff', etc.
        cleaned_list.append(cleaned_name)  # append to the cleaned lust

    cleaned_series = pd.Series(cleaned_list)  #turn list back to pd series
    cleaned_series = cleaned_series.astype(str)
    data_frame["jurisdiction_name"] = cleaned_series   #replace dataframe

    # make sure jurisdiction name in index 1 of dataframe
    if data_frame.columns.get_loc("jurisdiction_name") != 1:
        data_frame = data_frame.drop("jurisdiction_name", axis=1)  # delete column if it's not in right index position
        data_frame.insert(1, "jurisdiction_name", cleaned_series)   # insert again in correct position

    return data_frame


    # Returns data frame only with columns
    # params: data_frame, keyword (string)
def get_dataframe_by_col_keywords(data_frame, keyword):
    """
    Returns data frame only with columns matching keyword

    Args:
        data_frame (pandas.DataFrame): Source dataframe/table
        keyword (string): Keyword to search columns for

    Returns:
        pandas.DataFrame: Data frame only with columns matching keyword
    """
    matching_columns = []

    for col in data_frame.columns:
        if keyword.lower() in col.lower():
            matching_columns.append(col)
    series = pd.Series(matching_columns)
    new_df = pd.DataFrame(data_frame[series])
    return new_df






# test code
if __name__ == "__main__":

    #load raw excel file
    df = load_excel_file("data/july_2024.xlsx", 5)

    #turn to snake case
    df.columns = make_columns_to_snake_case(df.columns)

    # report date func
    df = make_report_date_column(df)


    # clean jurisdiction name
    df = clean_jurisdiction_name(df)

    # test to see dtypes by keyword
    print(get_dataframe_by_col_keywords(df, "#").dtypes)
    print(get_dataframe_by_col_keywords(df, "date").dtypes)




