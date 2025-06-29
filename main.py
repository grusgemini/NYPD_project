import argparse
import os
import pandas as pd 
from fapa_analysis_lib import data_processing as dp


def main():


    parser = argparse.ArgumentParser()

    parser.add_argument('--input_directory', type=str, help='Path to directory containing files with data.')
    parser.add_argument('--output_directory', type=str, help='Path to directory to save the results of analysis.')

    args = parser.parse_args()

    input_dir = args.input_directory
    output_dir = args.output_directory
    

# READING THE FILES
    alcohol_data = dp.load_csv_file(os.path.join(input_dir, "alcohol_data.csv"))  #/Users/kacper/Desktop/NYPD_project/data/alcohol_data.csv
    fire_incidents_data = dp.load_excel_file(os.path.join(input_dir, "fire_incidents.xlsx"), 0)   #/Users/kacper/Desktop/NYPD_project/data/fire_incidents.xlsx
    population_data = dp.load_excel_file(os.path.join(input_dir, "population_data.xls"), 8)  #/Users/kacper/Desktop/NYPD_project/data/area_data.xlsx
    area_data = dp.load_excel_file(os.path.join(input_dir, "area_data.xlsx"), 0)  #/Users/kacper/Desktop/NYPD_project/data/population_data.xls 


#PROCESSING THE ALCOHOL DATA
    alcohol_cols_to_drop = ['Numer zezwolenia', 'Nazwa firmy', 'Kod pocztowy', 'Adres', 'Województwo', 'Data ważności']
    alcohol_data = dp.drop_columns(alcohol_data, alcohol_cols_to_drop)
    alcohol_data = dp.delete_spaces(alcohol_data, 'Miejscowość')
    alcohol_data = dp.cut_after_comma(alcohol_data, 'Miejscowość')
    alcohol_data = dp.count_unique(alcohol_data, 'Miejscowość')

#PROCESSING THE FIRE INCIDENTS DATA
    fire_columns_to_drop = ['Województwo', 'Powiat', 'Ogółem zdarzeń rok 2023', 'Pożary rok 2023', 'Miejscowe zagrożenia rok 2023', 'Alarmy fałszywe rok 2023'] 
    fire_incidents_data = dp.drop_columns(fire_incidents_data, fire_columns_to_drop)
    fire_incidents_data = dp.lower_the_case(fire_incidents_data, 'Gmina')
    fire_incidents_data['TERYT'] = fire_incidents_data['TERYT'].astype(str)


#PROCESSING THE POPULATION DATA
    population_data = population_data.iloc[:,[0,1,2]]
    population_data.columns = ['Nazwa jednostki','Kod', 'Populacja']
    population_data = dp.delete_prefix(population_data, 'Kod', '0')
    population_data = dp.delete_prefix(population_data, 'Nazwa jednostki', 'M. ')
    population_data = dp.drop_last_char(population_data, 'Kod')
    population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'M-W.')
    population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'G.')
    population_data = dp.lower_the_case(population_data, 'Nazwa jednostki')



#PROCESSING THE AREA DATA
    area_columns_to_drop = ['Powierzchnia [ha]', 'Unnamed: 4', 'Unnamed: 5']
    area_data = dp.drop_columns(area_data, area_columns_to_drop)
    area_data = dp.lower_the_case(area_data, 'Nazwa jednostki')
    area_data = dp.delete_spaces(area_data, 'TERYT')
    area_data = dp.delete_spaces(area_data, 'Nazwa jednostki')
    area_data = dp.delete_prefix(area_data, 'TERYT', '0')
    area_data = dp.drop_last_char(area_data, 'TERYT')
    area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-miasto')
    area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-obszarwiejski')

#ALCOHOL VS POPULATION
    alcohol_vs_population = dp.custom_merge(alcohol_data, population_data, 'Miejscowość', 'Nazwa jednostki')
    corr_alc_vs_pop = alcohol_vs_population["Count"].corr(alcohol_vs_population["Populacja"])

#FIRE INCIDENTS VS ALCOHOL 
    fire_vs_alcohol = dp.custom_merge(fire_incidents_data, alcohol_data, 'Gmina', 'Miejscowość')
    corr_all_fire_vs_alc = fire_vs_alcohol["Count"].corr(fire_vs_alcohol["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_alc = fire_vs_alcohol["Count"].corr(fire_vs_alcohol["Pożary rok 2024"])
    corr_false_fire_vs_alc = fire_vs_alcohol["Count"].corr(fire_vs_alcohol["Alarmy fałszywe rok 2024"])

#FIRE INCIDENTS VS POPULATION
    fire_vs_population = dp.custom_merge(fire_incidents_data, population_data, 'TERYT', 'Kod')
    corr_all_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Pożary rok 2024"])
    corr_false_fire_vs_pop = fire_vs_population["Populacja"].corr(fire_vs_population["Alarmy fałszywe rok 2024"])

#FIRE INCIDENTS VS AREA
    fire_vs_area = dp.custom_merge(fire_incidents_data, area_data, 'TERYT', 'TERYT')
    corr_all_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Pożary rok 2024"])
    corr_false_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(fire_vs_area["Alarmy fałszywe rok 2024"])


#SAVING THE RESULTS 

    results = pd.DataFrame({
        'correlation':['Correlation between population and number of alcohol selling companies: ', 
                       'Correlation between number of all fire incidents and number of alcohol selling companies: ',
                       'Correlation between number of actual fire incidents and number of alcohol selling companies: ',
                       'Correlation between number of false reports of fire incidents and number of alcohol selling companies: ',
                       'Correlation between number of all fire incidents and population: ',
                       'Correlation between number of actual fire incidents and population: ',
                       'Correlation between number of false reports of fire incidents and population: ',
                       'Correlation between number of all fire incidents and area: ',
                       'Correlation between number of actual fire incidents and area: ',
                       'Correlation between number of false reports of fire incidents and area: '],

        'value': [corr_alc_vs_pop, 
                  corr_all_fire_vs_alc,
                  corr_actual_fire_vs_alc,
                  corr_false_fire_vs_alc,
                  corr_all_fire_vs_pop,
                  corr_actual_fire_vs_pop,
                  corr_false_fire_vs_pop, 
                  corr_all_fire_vs_area,
                  corr_actual_fire_vs_area,
                  corr_false_fire_vs_area]
    })

    results.to_csv(os.path.join(output_dir, "Results.txt"), sep='\t', index=False, header = False)


    print("Analysis complete. Results have been saved in:", output_dir)


if __name__ == "__main__":
    main()
