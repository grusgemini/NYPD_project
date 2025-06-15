import pandas as pd
import argparse
from mylib import fire_data_prep, alc_data_prep, pop_data_prep, area_data_prep, analysis


parser = argparse.ArgumentParser()

parser.add_argument('fires_data', type=str, help='Path to CSV file containing data about fire incidents in Poland')
parser.add_argument('alc_data', type=str, help='Path to CSV file containing data about alcohol selling concessions Poland')
parser.add_argument('pop_data', type=str, help='Path to XLS file containing data about population Poland')
parser.add_argument('area_data', type=str, help='Path to XLSX file containing data about area Poland')

args = parser.parse_args()

fires_file = args.fires_data
alcohol_file = args.alc_data
pop_file = args.pop_data
area_file = args.area_data

fires = pd.read_csv(fires_file, skiprows=4)
alcohol = pd.read_csv(alcohol_file, skiprows=4)
pop = pd.read_excel(pop_file)
area = pd.read_excel(area_file)


