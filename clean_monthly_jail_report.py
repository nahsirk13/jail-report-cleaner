import pandas as pd


def load_excel_file(filepath, n_preview_rows=3):
    """
    Loads Excel file

    Args:
        filepath (str): path to Excel file
        n_preview_rows (int): number of rows to preview

    Returns:
        pandas.DataFrame: df created from Excel file
    """
    data_frame = pd.read_excel(filepath)
    print ("Loaded file: ", filepath)
    print("\tShape (Rows x Columns): ", data_frame.shape)
    print("\tPreview Rows: \n", data_frame.head(n_preview_rows))
    return data_frame



def make_columns_to_snake_case(columns):
    """
    Turns the column names into snake_case

    Args:
        columns (pandas.Dataframe.columns): columns from source data frame

    Returns:
        columns (pandas.Dataframe.columns): columns with newly formatted names
    """
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
    """
    Makes dataframe with a report date column as first column with month, year, and date as last day of month.
    Deletes the old reporting month and year columns. Assumes column names already in snake case.

    Args:
        data_frame (pandas.DataFrame): source dataframe without report_date column

    Returns:
        pandas.DataFrame: New dataframe with changes
    """

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



def clean_jurisdiction_name(data_frame):
    """
    Changes jurisdiction name to only include the country name with no extra spaces, provided that it include
    'sheriff,' 'correction,' or 'work,' and makes sure it is the 2nd column in the df. Assumes column names already in snake case.

    Args:
        data_frame (pandas.DataFrame): source dataframe with raw jurisdiction name

    Returns:
        columns_to_snake (pandas.Dataframe.columns): columns with newly formatted names

    Raises:
        ValueError: if the markers for where the county name ends are not present. May produce NaN error for names if so.
    """
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
            raise ValueError("jurisdiction_name has name without 'sheriff', 'correction', or 'work', please check input")
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


def get_dataframe_by_col_keywords(data_frame, keyword):
    """
    Returns data frame only with columns matching keyword, useful for test printing data types by keyword

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


def cast_col_by_keyword(data_frame, keyword, type):
    """
    Returns data frame only with columns matching keyword, useful for test printing data types by keyword

    Args:
        data_frame (pandas.DataFrame): Source dataframe/table
        keyword (string): Keyword to search columns for

    Returns:
        pandas.DataFrame: Data frame only with columns matching keyword
    """
    for col in data_frame.columns:
        if keyword.lower() in col.lower():
            if type == 'datetime' or type == 'date':
                data_frame[col] = pd.to_datetime(data_frame[col], errors='coerce')  # coerce results in NaT or NaN if unmatching type found
            elif type == 'int' or type == 'integer':
                data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce').astype('Int64')
            elif type == 'float':
                data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')
            elif type == 'str' or type == 'string' :
                data_frame[col] = data_frame[col].astype(str)
            else:
                print("Invalid type argument entered. Options are 'datetime', 'int', 'float', and 'str'")
    return data_frame


def fully_process_excel(filepath):
    # load raw excel file
    df = load_excel_file(filepath, 5)

    # turn to snake case
    df.columns = make_columns_to_snake_case(df.columns)

    # report date func
    df = make_report_date_column(df)

    # clean jurisdiction name
    df = clean_jurisdiction_name(df)

    # tests to see dtypes by keyword (commented out)
    # print(df.dtypes)
    # print(get_dataframe_by_col_keywords(df, "#").dtypes)
    # print(get_dataframe_by_col_keywords(df, "date").dtypes)

    #cast data types based on keywords contained in them observed in tests
    cast_col_by_keyword(df, "#", "int")
    cast_col_by_keyword(df, "encounters", "int")
    cast_col_by_keyword(df, "inmates", "int")
    cast_col_by_keyword(df, "cases", "int")
    cast_col_by_keyword(df, "sentenced", "int")
    cast_col_by_keyword(df, "total", "int")
    cast_col_by_keyword(df, "appointments", "int")
    cast_col_by_keyword(df, "occurrences", "int")

    cast_col_by_keyword(df, "date", "datetime")

    name = filepath.split("/")[-1].split(".")[0]  #get name of file by splitting/removing the directory path

    df.to_csv(f"processed_data/processed_{name}.csv", index=False)  #finally, output to csv file



if __name__ == "__main__":
    fully_process_excel("data/june_2024.xlsx")
    fully_process_excel("data/july_2024.xlsx")
    fully_process_excel("data/august_2024.xlsx")


