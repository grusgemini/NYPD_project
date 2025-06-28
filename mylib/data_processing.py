import pandas as pd

def load_excel_file(filepath: str, rows_to_skip: int) -> pd.DataFrame:
    """Loads an excel file as a Data Frame
    :param file_path: Path to the CSV file that we want to load
    :param rows_to_skio: How many rows you would like to drop from the top
    """
    return pd.read_excel(io=filepath, skiprows=rows_to_skip)


def load_csv_file(filepath: str) -> pd.DataFrame:
    """Loads a CSV file as a Data Frame
    :param file_path: Path to the CSV file that we want to load"""
    return pd.read_csv(filepath)


def lower_the_case(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Lowers the case of text in given column of a data frame. 
    :param data: Input dataframe
    :param column: Column that will be lowercased
    """
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    data = data.copy()
    data[column] = data[column].astype(str).str.lower()
    return data


def drop_columns(data: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Deletes given columns form a data frame.
    :param data: Input dataframe
    :param column: List of names of columns to drop"""
    
    data = data.copy()
    data = data.drop(columns = columns)
    return data


def drop_rows_by_index(data: pd.DataFrame, rows: list) -> pd.DataFrame:
    """Deletes given rows form a data frame.
    :param data: Input dataframe
    :param rows: List of numbers of rows to drop"""
    data = data.copy()
    rows = list(map(lambda x: x -1, rows))
    data = data.drop(index = data.iloc[rows].index)
    return data


def drop_rows_by_suffix(data: pd.DataFrame, column: str, suffix: str) -> pd.DataFrame:
    """Deletes rows where entries in a given column end with given suffixes
    :param data: Input dataframe
    :param column: Column where we look for entries with suffix
    :param suffixes: Suffix 
    """
    data = data.copy()
    data = data[~data[column].str.endswith(suffix)]
    return data


def drop_rows_by_prefix(data: pd.DataFrame, column: str, prefix: str) -> pd.DataFrame:
    """Deletes rows where entries in a given column start with given prefix
    :param data: Input dataframe
    :param column: Column where we look for entries with prefix
    :param prefix: Prexif 
    """
    data = data.copy()
    data = data[~data[column].str.startswith(prefix)]
    return data


def delete_prefix(data: pd.DataFrame, column: str, prefixes: list) -> pd.DataFrame:
    """Deletes a given prefix in a column of a dataframe.
    :param data: Input DataFrame
    :param column: Name of the column where the prefixes need to be removed
    :param prefixes: List of strings with prefixes to be removed
    """
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    data = data.copy()
    data[column] = (
        data[column]
        .astype(str)
        .apply(lambda x: next((x[len(p) :] for p in prefixes if x.startswith(p)), x))
    )
    return data


def delete_spaces(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Deletes spaces in a column of a dataframe.
    :param data: Input DataFrame
    :param column: Name of the column where the prefixes need to be removed
    """ 
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    data = data.copy()
    data[column] = data[column].str.replace(' ', '', regex=False) 
    return data


def cut_after_comma(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Cuts the string after a comma
    :param data: Input data frame
    :param column: Column where we want to modify the strings
    """
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    data = data.copy()
    data[column] = data[column].str.replace(r',.*', '', regex=True)
    return data


def drop_last_char(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Removes the last character from strings in a given column
    :param data: Input dataframe
    :param column: Column from which the last character is to be deleted
    """
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    data = data.copy()
    data[column] = data[column].astype(str).str[:-1]
    return data


def count_unique(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Counts unique string values in a given column of a data frame. Returns a dataframe with two columns-    
    the unique values and a number of occurences in the original data frame.
    :param data: Input data frame
    :param column: Column where we want to count the unique string values
    """ 
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")
    
    counter = data[column].apply(lambda x: str(x).lower())
    counter = counter.value_counts().reset_index()
    counter.columns = [column, "Count"]
    return counter


def custom_merge(data1: pd.DataFrame, data2: pd.DataFrame, column1: str, column2: str) -> pd.DataFrame:
    """Merges two DataFrames using different column names.
    :param data1: Input data frame
    :param data2: Second input data frame
    :param column1: Column name to merge on in data1
    :param column2: Column name to merge on in data2
    """
    return pd.merge(data1, data2, left_on=column1, right_on=column2, how='inner')


def save_results(title: str, value: float, filename: str):
    """Creating a table and saving results to csv file
    :param title: Name of value we want to save
    :param value: The value
    :param filename: Path to file where result is going to be saved
    """
    table = pd.DataFrame({title: [value]})
    table.to_csv(filename, index=False)

