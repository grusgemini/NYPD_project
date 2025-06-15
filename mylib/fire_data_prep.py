import pandas as pd


def load_file(file_path):
    df = pd.read_csv(file_path)
    return df

def change_col_names(df):
    df.columns = ['woj', 'powiat', 'gmina', 'total', 'ob. uzytecznosci publicznej', 'ob. mieszkalne', 'ob. produkcyjne', 'ob. magazynowe', 'transport', 'lasy', 'uprawy', 'inne', 'wybuchy']
    return df

def drop_columns(df):
    df = df.drop(columns=[col for col in df.columns if not col.startswith(('Woj', 'Pow', 'Gm', 'OGÓŁEM', 'RAZEM'))])
    return df

def lower_case(df):
    for col in ['woj', 'powiat', 'gmina']:
        df[col] = df[col].str.lower()
    return df


def final_fire_data(file_path):
    df = load_file(file_path)
    df_dropped = drop_columns(df) 
    df_newnames = change_col_names(df_dropped)
    final_df = lower_case(df_newnames)

    return final_df







#def data_merge()    