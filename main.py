import argparse
import os
import pandas as pd
from mylib import data_processing as dp
from mylib import statistics as stat 



def main():


    parser = argparse.ArgumentParser()

    parser.add_argument('--input_directory', type=str, help='Path to directory containing files with data.')
    parser.add_argument('--output_directory', type=str, help='Path to directory to save the results of analysis.')

    args = parser.parse_args()

    input_dir = args.input_directory
    output_dir = args.output_directory
    

# READING THE FILES
   
    alcohol_data = dp.load_csv_file(os.path.join(input_dir, "alcohol_data.csv"))  #/Users/kacper/Desktop/NYPD_project/data/alcohol_data.csv
    fire_incidents_data = dp.load_excel_file(os.path.join(input_dir, "fire_incidents.xlsx"))  #/Users/kacper/Desktop/NYPD_project/data/fire_incidents.xlsx
    population_data = dp.load_excel_file(os.path.join(input_dir, "population_data.xls"))  #/Users/kacper/Desktop/NYPD_project/data/area_data.xlsx
    area_data = dp.load_excel_file(os.path.join(input_dir, "area_data.xlsx"))  #/Users/kacper/Desktop/NYPD_project/data/population_data.xls 


#PROCESSING THE ALCOHOL DATA

    alcohol_cols_to_drop = ['Numer zezwolenia', 'Nazwa firmy', 'Kod pocztowy', 'Adres', 'Województwo', 'Data ważnosci']
    alcohol_data = dp.drop_columns(alcohol_data, alcohol_cols_to_drop)
    alcohol_data = dp.delete_spaces(alcohol_data, 'Miejscowość')
    alcohol_data = dp.cut_after_comma(alcohol_data, 'Miejscowość')
    alcohol_data = dp.count_unique(alcohol_data)

#PROCESSING THE FIRE INCIDENTS DATA

    fire_columns_to_drop = ['Województwo', 'Powiat', 'Ogółem zdarzeń rok 2023', 'Pożary rok 2023', 'Miejscowe zagrożenia rok 2023', 'Alarmy fałszywe rok 2023'] 
    fire_incidents_data = dp.drop_columns(fire_incidents_data, fire_columns_to_drop)

#PROCESSING THE POPULATION DATA

    population_data = dp.load_excel_file(os.path.join(input_dir, "population_data.xls"), 8)  #/Users/kacper/Desktop/NYPD_project/data/area_data.xlsx
    population_data = population_data.iloc[:,[1,2]]
    population_data.columns = ['Kod', 'Populacja']


#PROCESSING THE AREA DATA

    area_columns_to_drop = ['Powierzchnia [ha]', 'Unnamed: 4', 'Unnamed: 5']
    area_data = dp.drop_columns(area_data, area_columns_to_drop)
    area_data = dp.delete_spaces(area_data, 'TERYT')
    area_data = dp.delete_prefix(area_data, 'TERYT', '0')
    area_data = dp.drop_rows(area_data, [1,2,3])

#MERGIN THE DATA



#CALCULATING STATISTICS


#SAVING THE RESULTS 
    print("Analysis complete. Results have been saved in:", output_dir)


if __name__ == "__main__":
    main()
