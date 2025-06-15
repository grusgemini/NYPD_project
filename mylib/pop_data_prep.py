import pandas as pd

def load_file(file_path):
    df = pd.read_excel(file_path, skiprows=8, usecols='A:C')
    return df

#Zmieniamy nazwy kolumn i zmieniamy wszystko na lower case w celu uproszczenia analizy
def column_processing(df):
    df.columns = ['gmina', 'kod', 'populacja']
    df = df.drop('kod')
    df['gmina'] = df['gmina'].str.lower()
    return df

def sum_by_gmina(df):
    cols_to_sum = ['total', 'ob. uzytecznosci publicznej', 'ob. mieszkalne', 'ob. produkcyjne', 'ob. magazynowe', 'transport', 'lasy', 'uprawy', 'inne', 'wybuchy']
    df_summed = df.groupby(['woj','gmina'])[cols_to_sum].sum()
    return df_summed

def final_pop_data(file_path):
    df = column_processing(load_file(file_path))
    final_df = sum_by_gmina(df_lowercase)
    return final_df
