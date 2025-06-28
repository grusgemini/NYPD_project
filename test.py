import pandas as pd
import numpy as np
import os
import openpyxl 
import xlrd
from importlib import reload
from mylib import data_processing as dp

reload(dp)


input_dir = '/Users/kacper/Desktop/NYPD_project/data/'

alc_path = '/Users/kacper/Desktop/NYPD_project/data/alcohol_data.csv'
area_path = '/Users/kacper/Desktop/NYPD_project/data/Wykaz_powierzchni_wg_stanu_na_01012025_ha_km2.xlsx'
fires_path = '/Users/kacper/Desktop/NYPD_project/data/fire_incidents.xlsx'
pop_path = '/Users/kacper/Desktop/NYPD_project/data/Tabela_IV.xls'



alcohol_data = dp.load_csv_file(alc_path)

alcohol_cols_to_drop = ['Numer zezwolenia', 'Nazwa firmy', 'Kod pocztowy', 'Adres', 'Województwo', 'Data ważności']
alcohol_data = dp.drop_columns(alcohol_data, alcohol_cols_to_drop)
alcohol_data = dp.delete_spaces(alcohol_data, 'Miejscowość')
alcohol_data = dp.cut_after_comma(alcohol_data, 'Miejscowość')
alcohol_data = dp.count_unique(alcohol_data, 'Miejscowość')
print(alcohol_data.head())





fire_incidents_data = dp.load_excel_file(os.path.join(input_dir, "fire_incidents.xlsx"), 0) 
fire_columns_to_drop = ['Województwo', 'Powiat', 'Ogółem zdarzeń rok 2023', 'Pożary rok 2023', 'Miejscowe zagrożenia rok 2023', 'Alarmy fałszywe rok 2023'] 
fire_incidents_data = dp.drop_columns(fire_incidents_data, fire_columns_to_drop)
fire_incidents_data = dp.lower_the_case(fire_incidents_data, 'Gmina')
fire_incidents_data['TERYT'] = fire_incidents_data['TERYT'].astype(str)
print(fire_incidents_data.head())





population_data = dp.load_excel_file(os.path.join(input_dir, "population_data.xls"), 8)  #/Users/kacper/Desktop/NYPD_project/data/area_data.xlsx
population_data = population_data.iloc[:,[0,1,2]]
population_data.columns = ['Nazwa jednostki','Kod', 'Populacja']
population_data = dp.delete_prefix(population_data, 'Kod', '0')
population_data = dp.drop_last_char(population_data, 'Kod')
population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'M-W.')
population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'G.')
population_data = dp.delete_prefix(population_data, 'Nazwa jednostki', 'M. ')
population_data = dp.lower_the_case(population_data, 'Nazwa jednostki')
print(population_data.head())



area_data = dp.load_excel_file(os.path.join(input_dir, "area_data.xlsx"), 0)  #/Users/kacper/Desktop/NYPD_project/data/population_data.xls 
area_columns_to_drop = ['Powierzchnia [ha]', 'Unnamed: 4', 'Unnamed: 5']
area_data = dp.drop_columns(area_data, area_columns_to_drop)
area_data = dp.lower_the_case(area_data, 'Nazwa jednostki')
area_data = dp.delete_spaces(area_data, 'TERYT')
area_data = dp.delete_spaces(area_data, 'Nazwa jednostki')
area_data = dp.delete_prefix(area_data, 'TERYT', '0')
area_data = dp.drop_last_char(area_data, 'TERYT')
area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-miasto')
area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-obszarwiejski')
print(area_data.head())



data = dp.custom_merge(area_data, population_data, 'TERYT', 'Kod')
data1 = dp. c

print(data.head())

fire_incidents_data['TERYT'] = fire_incidents_data['TERYT'].astype(str)
data1 = dp.custom_merge(fire_incidents_data, data, 'TERYT', 'TERYT')
data1 = dp.drop_columns(data1, ['Kod', 'Nazwa jednostki'])
print(data1.head())


data2 = dp.custom_merge(data1, alcohol_data, 'Gmina', 'Miejscowość')
print(data2.head())


fap

fa = dp.custom_merge(fire_incidents_data, area_data, 'TERYT', 'TERYT')
fa = dp.drop_columns(fa, ['Gmina', 'Nazwa jednostki'])
a_p = dp.drop_columns(a_p, 'Kod')
fap = dp.custom_merge(fa, population_data, 'TERYT', 'Kod')
fap = dp.drop_columns(fap, 'Kod')
fap['TERYT'] = fap['Nazwa jednostki']
fap = dp.drop_columns(fap, 'Nazwa jednostki')
fap = dp.lower_the_case(fap, 'TERYT')
fapa = dp.custom_merge(fap, alcohol_data, )
print(fap.head())

print(population_data.columns)


area_population = dp.custom_merge(area_data, population_data, 'TERYT', 'Kod')
area_population_fire = dp.custom_merge(area_population, fire_incidents_data, 'TERYT', 'TERYT')
area_population_fire_alcohol = dp.custom_merge(area_population_fire, alcohol_data, 'Nazwa jednostki_x', 'Miejscowość')
final_data = dp.drop_columns(area_population_fire_alcohol, ['TERYT', 'Nazwa jednostki_x', 'Kod', 'Miejscowość', 'Gmina'])
final_data = final_data[['Nazwa jednostki_y', 'Populacja', 'Powierzchnia [km2]', 'Count', 'Ogółem zdarzeń rok 2024', 'Pożary rok 2024', 'Miejscowe zagrożenia rok 2024', 'Alarmy fałszywe rok 2024']]

print(area_population_fire_alcohol.head())
print(final_data.sort_values(by = 'Count', ascending = False))


alcohol_vs_population = dp.custom_merge(alcohol_data, population_data, 'Miejscowość', 'Nazwa jednostki')
print(alcohol_vs_population.sort_values(by = 'Count', ascending = False))

corr1 = alcohol_vs_population["Count"].corr(alcohol_vs_population["Populacja"])
print(corr1)

output_dir = '/Users/kacper/Desktop/NYPD_project/results'

dp.save_results("Correlation between population and number of alcohol selling companies", corr1, os.path.join(output_dir, "Corr_alcohol_vs_population.txt"))

fire_vs_alcohol = dp.custom_merge(fire_incidents_data, alcohol_data, 'Gmina', 'Miejscowość')
print(fire_vs_alcohol.head())
corr_fire_vs_alc = fire_vs_alcohol["Count"].corr(fire_vs_alcohol["Miejscowe zagrożenia rok 2024"])
print(corr_fire_vs_alc)


fire_vs_population = dp.custom_merge(fire_incidents_data, population_data, 'TERYT', 'Kod')
print(fire_vs_population.head())
corr_all_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Ogółem zdarzeń rok 2024"])
print(corr_all_fire_vs_pop)
corr_actual_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Pożary rok 2024"])
print(corr_actual_fire_vs_pop)
corr_false_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Alarmy fałszywe rok 2024"])
print(corr_false_fire_vs_pop)


fire_vs_area = dp.custom_merge(fire_incidents_data, area_data, 'TERYT', 'TERYT')
corr_all_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Ogółem zdarzeń rok 2024"])
corr_actual_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Pożary rok 2024"])
corr_false_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Alarmy fałszywe rok 2024"])

print(corr_all_fire_vs_area)
print(corr_actual_fire_vs_area)
print(corr_false_fire_vs_area)