import argparse
from mylib import fire_data_prep, alc_data_prep, pop_data_prep, area_data_prep, analysis


parser = argparse.ArgumentParser()


parser.add_argument('alc_data', type=str, help='Path to CSV file containing data about alcohol selling concessions Poland')
parser.add_argument('area_data', type=str, help='Path to XLSX file containing data about area of administrative regions in Poland')
parser.add_argument('fires_data', type=str, help='Path to CSV file containing data about fire incidents in Poland')
parser.add_argument('pop_data', type=str, help='Path to XLS file containing data about population Poland')

args = parser.parse_args()

alc_path = args.alc_data
area_path = args.area_data
fires_path = args.fires_data
pop_path = args.pop_data


alcohol = pd.read_csv(alc_path, skiprows=4)
area = pd.read_excel(area_path)
fires = pd.read_csv(fires_path, skiprows=4)
pop = pd.read_excel(pop_path)
