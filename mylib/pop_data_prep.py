import pandas as pd
import numpy as np 
import openpyxl 


def setnames(df):
    df.columns = ['woj', 'powiat', 'gmina', 'total', 'ob. uzytecznosci publicznej', 'ob. mieszkalne', 'ob. produkcyjne', 'ob. magazynowe', 'transport', 'lasy']
    return df

def drop_columns(df):
    df = df.drop(columns=[col for col in df.columns if not col.startswith(('Woj', 'Pow', 'Gm', 'OGÓŁEM', 'RAZEM'))])
    return df

def lower_case(df):
    for col in ['woj', 'powiat', 'gmina']:
        df[col] = df[col].str.lower()

    return df








#def data_merge()    