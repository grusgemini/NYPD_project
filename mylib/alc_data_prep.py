import pandas as pd
import numpy as np

def load_file(file_path):
    df = pd.read_csv(file_path)
    return df

#Usuwamy wszystkie kolumny poza miejscowością i województwem, bo są niepotrzebne.
#Dodajemy kolumnę z licznikiem skleów
#Zmieniamy nazwy kolumn
#Zmieniamy wszystko na lowercase dla uproszczenia analizy
def column_processing(df):
    df = df.drop(columns=[col for col in df.columns if not col.startswith(('Miejsc', 'Wojew'))])
    df['count'] = np.ones(len(df))
    df.columns = ['miasto', 'woj', 'liczba sklepów']
    for col in ['miasto', 'woj']:
        df[col] = df[col].str.lower()
    return df

#Po przejrzeniu danych w kolumnie "Miejscowość" pojawiaja się zbędne spacje utrudniające grupowanie i analizę danych. Ponadto 
#niektóre miejscowości mają wsie po przecinku. Nie będziemy analizować z taką dokładnością.  
#Usuwamy tez prefix "woj. ", który jest niepotrzebny.
def delete_stuff(df):
    df['miasto'] = df['miasto'].str.replace(' ', '', regex=False)
    df['miasto'] = df['miasto'].str.replace(r',.*', '', regex=True)
    df['woj'] = df['woj'].str.removeprefix('woj. ')
    return df

#Sumujemy po miastach, zeby wiedziec ile jest w danym miescie sklepow alkoholowych
def sum_by_miasto(df):
    df_summed = df.groupby(['miasto','woj'])[['liczba sklepów']].sum()
    return df_summed

def final_alc_data(file_path):
    df_columns_processed = column_processing(load_file(file_path))
    df_no_stuff = delete_stuff(df_columns_processed)
    final_df = sum_by_miasto(df_no_stuff)
    return final_df

