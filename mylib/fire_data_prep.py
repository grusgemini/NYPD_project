import pandas as pd

def load_file(file_path):
    df = pd.read_csv(file_path)
    return df

#Usuwamy wszystkie kolumny poza gminą, województwem i zsumowanymi kategoriami
#Zmieniamy nazwy kolumn i zmieniamy wszystko na lower case w celu uproszczenia analizy
def column_processing(df):
    df = df.drop(columns=[col for col in df.columns if not col.startswith(('Woj', 'Gm', 'OGÓŁEM', 'RAZEM'))])
    df.columns = ['woj', 'gmina', 'total', 'ob. uzytecznosci publicznej', 'ob. mieszkalne', 'ob. produkcyjne', 'ob. magazynowe', 'transport', 'lasy', 'uprawy', 'inne', 'wybuchy']
    for col in ['woj', 'gmina']:
        df[col] = df[col].str.lower()
    return df

def sum_by_gmina(df):
    cols_to_sum = ['total', 'ob. uzytecznosci publicznej', 'ob. mieszkalne', 'ob. produkcyjne', 'ob. magazynowe', 'transport', 'lasy', 'uprawy', 'inne', 'wybuchy']
    df_summed = df.groupby(['woj','gmina'])[cols_to_sum].sum()
    return df_summed

def final_fire_data(file_path):
    df = load_file(file_path)
    df_dropped = drop_columns(df) 
    df_newnames = change_col_names(df_dropped)
    df_lowercase = lower_case(df_newnames)
    final_df = sum_by_gmina(df_lowercase)
    return final_df
