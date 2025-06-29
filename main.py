import argparse
import os
import pandas as pd
from fapa_analysis_lib import data_processing as dp
import cProfile


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        type=str,
        help="Path to directory containing files with data.",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to directory to save the results of analysis.",
    )

    args = parser.parse_args()

    input_dir = args.input
    #input_dir = '/Users/kacper/Desktop/NYPD_project_final/data'

    output_dir = args.output
    #output_dir = '/Users/kacper/Desktop/NYPD_project_final/results'


    # READING THE FILES
    alcohol_data = dp.load_csv_file(
        os.path.join(input_dir, "alcohol_data.csv")
    )  
    fire_incidents_data = dp.load_excel_file(
        os.path.join(input_dir, "fire_incidents.xlsx"), 0
    )  
    population_data = dp.load_excel_file(
        os.path.join(input_dir, "population_data.xls"), 7
    )
    area_data = dp.load_excel_file(
        os.path.join(input_dir, "area_data.xlsx"), 0
    )  

    # PROCESSING THE ALCOHOL DATA
    alcohol_cols_to_drop = [
        "Numer zezwolenia",
        "Nazwa firmy",
        "Kod pocztowy",
        "Adres",
        "Data ważności",
    ]
    alcohol_data = dp.drop_columns(alcohol_data, alcohol_cols_to_drop)
    alcohol_data = dp.delete_spaces(alcohol_data, "Miejscowość")
    alcohol_data = dp.cut_after_comma(alcohol_data, "Miejscowość")

    alcohol_data_cities = dp.count_unique(alcohol_data, 'Miejscowość')
    alcohol_data_cities['Miejscowość'] = alcohol_data_cities['Miejscowość'].astype(str)

    alcohol_data_voj = dp.count_unique(alcohol_data, 'Województwo')
    alcohol_data_voj = dp.delete_prefix(alcohol_data_voj, 'Województwo', ['woj.'])
    alcohol_data_voj['Województwo'] = alcohol_data_voj['Województwo'].str.strip()
    alcohol_data_voj['Województwo'] = alcohol_data_voj['Województwo'].astype(str)

    # PROCESSING THE FIRE INCIDENTS DATA
    fire_columns_to_drop = [
        "Powiat",
        "Ogółem zdarzeń rok 2023",
        "Pożary rok 2023",
        "Miejscowe zagrożenia rok 2023",
        "Alarmy fałszywe rok 2023",
    ]
    fire_incidents_data = dp.drop_columns(fire_incidents_data, fire_columns_to_drop)
    fire_incidents_data = dp.lower_the_case(fire_incidents_data, "Gmina")
    fire_incidents_data["TERYT"] = fire_incidents_data["TERYT"].astype(str)
    fires_in_voj = dp.drop_columns(fire_incidents_data, ['TERYT', 'Gmina'])
    fires_in_voj['Województwo'] = fires_in_voj['Województwo'].str.strip()
    fires_in_voj['Województwo'] = fires_in_voj['Województwo'].astype(str)
    fires_in_voj = fires_in_voj.groupby('Województwo', as_index=False).sum()    

    # PROCESSING THE POPULATION DATA
    population_data = population_data.iloc[:,[0,1,2]]
    population_data.columns = ['Nazwa jednostki','Kod', 'Populacja']
    population_data = dp.delete_prefix(population_data, 'Kod', '0')
    population_data = dp.drop_last_char(population_data, 'Kod')
    population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'M-W.')
    population_data = dp.drop_rows_by_prefix(population_data, 'Nazwa jednostki', 'G.')
    population_data = dp.delete_prefix(population_data, 'Nazwa jednostki', 'M.')
    population_data = dp.delete_prefix(population_data, 'Nazwa jednostki', '.')
    population_data = dp.lower_the_case(population_data, 'Nazwa jednostki')
    population_data = dp.delete_prefix(population_data, "Nazwa jednostki", ["woj."])
    population_data['Nazwa jednostki'] = population_data['Nazwa jednostki'].str.strip()
    population_data['Nazwa jednostki'] = population_data['Nazwa jednostki'].astype(str)
    

    # PROCESSING THE AREA DATA
    area_columns_to_drop = ['Powierzchnia [ha]', 'Unnamed: 4', 'Unnamed: 5']
    area_data = dp.drop_columns(area_data, area_columns_to_drop)    
    area_data = dp.lower_the_case(area_data, 'Nazwa jednostki')
    area_data = dp.delete_spaces(area_data, 'TERYT')
    area_data = dp.delete_spaces(area_data, 'Nazwa jednostki')
    area_data = dp.delete_prefix(area_data, 'TERYT', '0')
    area_data = dp.drop_last_char(area_data, 'TERYT')
    area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-miasto')
    area_data = dp.drop_rows_by_suffix(area_data, 'Nazwa jednostki', '-obszarwiejski')
    area_data= dp.delete_prefix(area_data, "Nazwa jednostki", ["woj."])

    # ALCOHOL VS POPULATION (VOIEVODSHIP)
    alcohol_vs_population_voj = dp.custom_merge(alcohol_data_voj, population_data, 'Województwo', 'Nazwa jednostki')
    corr_alc_vs_pop_voj = alcohol_vs_population_voj["Count"].corr(alcohol_vs_population_voj["Populacja"])
    
    # ALCOHOL VS POPULATION (CITIES)
    alcohol_vs_population_cities = dp.custom_merge(alcohol_data_cities, population_data, 'Miejscowość', 'Nazwa jednostki')
    corr_alc_vs_pop_cities = alcohol_vs_population_cities["Count"].corr(alcohol_vs_population_cities["Populacja"])
    
    # FIRE INCIDENTS VS ALCOHOL (VOIEVODSHIP)
    fires_vs_alcohol_voj = dp.custom_merge(alcohol_data_voj, fires_in_voj, 'Województwo', 'Województwo')
    corr_all_fire_vs_alc_voj = fires_vs_alcohol_voj["Count"].corr(fires_vs_alcohol_voj["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_alc_voj = fires_vs_alcohol_voj["Count"].corr(fires_vs_alcohol_voj["Pożary rok 2024"])
    corr_false_fire_vs_alc_voj = fires_vs_alcohol_voj["Count"].corr(fires_vs_alcohol_voj["Alarmy fałszywe rok 2024"])

    # FIRE INCIDENTS VS ALCOHOL (CITIES)
    fires_vs_alcohol_cities = dp.custom_merge(fire_incidents_data, alcohol_data_cities, "Gmina", 'Miejscowość')
    fires_vs_alcohol_cities = dp.drop_columns(fires_vs_alcohol_cities, ['TERYT', 'Województwo','Gmina'])
    fires_vs_alcohol_cities = fires_vs_alcohol_cities.groupby('Miejscowość', as_index = False).sum()
    corr_all_fire_vs_alc_cities = fires_vs_alcohol_cities["Count"].corr(fires_vs_alcohol_cities["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_alc_cities = fires_vs_alcohol_cities["Count"].corr(fires_vs_alcohol_cities["Pożary rok 2024"])
    corr_false_fire_vs_alc_cities = fires_vs_alcohol_cities["Count"].corr(fires_vs_alcohol_cities["Alarmy fałszywe rok 2024"])

    # FIRE INCIDENTS VS POPULATION (VOIEVODSHIP)
    fire_vs_populatio_voj = dp.custom_merge(fires_in_voj, population_data, 'Województwo', 'Nazwa jednostki')
    corr_all_fire_vs_pop_voj = fire_vs_populatio_voj["Populacja"].corr(fire_vs_populatio_voj["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_pop_voj = fire_vs_populatio_voj["Populacja"].corr(fire_vs_populatio_voj["Pożary rok 2024"])
    corr_false_fire_vs_pop_voj = fire_vs_populatio_voj["Populacja"].corr(fire_vs_populatio_voj["Alarmy fałszywe rok 2024"])

    # FIRE INCIDENTS VS POPULATION (CITIES)
    fire_vs_populatio_cities = dp.custom_merge(fire_incidents_data, population_data, 'Gmina', 'Nazwa jednostki')
    fire_vs_populatio_cities = dp.drop_columns(fire_vs_populatio_cities, ['TERYT', 'Województwo', 'Nazwa jednostki', 'Kod'])
    fire_vs_populatio_cities = fire_vs_populatio_cities.groupby('Gmina', as_index = False).sum()
    corr_all_fire_vs_pop_cities = fire_vs_populatio_cities["Populacja"].corr(fire_vs_populatio_cities["Ogółem zdarzeń rok 2024"])
    corr_actual_fire_vs_pop_cities = fire_vs_populatio_cities["Populacja"].corr(fire_vs_populatio_cities["Pożary rok 2024"])
    corr_false_fire_vs_pop_cities = fire_vs_populatio_cities["Populacja"].corr(fire_vs_populatio_cities["Alarmy fałszywe rok 2024"])   

    # FIRE INCIDENTS VS AREA
    fire_vs_area = dp.custom_merge(fire_incidents_data, area_data, "TERYT", "TERYT")
    corr_all_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(
        fire_vs_area["Ogółem zdarzeń rok 2024"]
    )
    corr_actual_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(
        fire_vs_area["Pożary rok 2024"]
    )
    corr_false_fire_vs_area = fire_vs_area["Powierzchnia [km2]"].corr(
        fire_vs_area["Alarmy fałszywe rok 2024"]
    )

    # SAVING THE RESULTS
    results = pd.DataFrame(
        {
            "correlation": [
                'Correlation between the number of alcohol selling concessions and population (voievodship): ',
                'Correlation between the number of alcohol selling concessions and population (cities): ',
                'Correlation between the number of all fire incidents and alcohol selling concessions (voievodship): ',
                'Correlation between the number of actual fire incidents and alcohol selling concessions(voievodship) : ',
                'Correlation between the number of false reports of fire incidents and alcohol selling concessions (voievodship): ',
                'Correlation between the number of all fire incidents and alcohol selling concessions (cities) : ',
                'Correlation between the number of actual fire incidents and alcohol selling concessions (cities) : ',
                'Correlation between the number of false reports of fire incidents and alcohol selling concessions (cities) : ',
                'Correlation between the number of all fire incidents and population (voievodship): ',
                'Correlation between the number of actual fire incidents and population (voievodship): ',
                'Correlation between the number of false reports of fire incidents and population (voievodship): ',
                'Correlation between the number of all fire incidents and population (cities): ',
                'Correlation between the number of actual fire incidents and population (cities): ',
                'Correlation between the number of false reports of fire incidents and population (cities): ',
                'Correlation between the number of all fire incidents and area: ',
                'Correlation between the number of actual fire incidents and area: ',
                'Correlation between the number of false reports of fire incidents ands area: '
            ],
            "value": [
                corr_alc_vs_pop_voj,
                corr_alc_vs_pop_cities,
                corr_all_fire_vs_alc_voj,
                corr_actual_fire_vs_alc_voj,
                corr_false_fire_vs_alc_voj,
                corr_all_fire_vs_alc_cities,
                corr_actual_fire_vs_alc_cities,
                corr_false_fire_vs_alc_cities,
                corr_all_fire_vs_pop_voj,
                corr_actual_fire_vs_pop_voj,
                corr_false_fire_vs_pop_voj,
                corr_all_fire_vs_pop_cities,
                corr_actual_fire_vs_pop_cities,
                corr_false_fire_vs_pop_cities,
                corr_all_fire_vs_area,
                corr_actual_fire_vs_area,
                corr_false_fire_vs_area
            ]
        }
    )

    results.to_csv(os.path.join(output_dir, "Results.txt"), sep="\t", index=False)

    print("Analysis complete. Results have been saved in:", output_dir)


if __name__ == "__main__":
        main()
 #   cProfile.run('main()')
 