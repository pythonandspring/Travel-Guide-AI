import pandas as pd
import csv

with open('travelling/filter_data/place_info.csv', mode='r') as file:
    record_list = csv.DictReader(file)
    record_list = list(record_list)

data = pd.DataFrame(record_list)

def get_countries():
    countries = data['country'].unique()
    return countries


def get_states():
    states = data['state'].unique()
    return states


def get_cities():
    cities = data['city'].unique()
    return cities


def get_place():
    place = data['name'].unique()
    return place

print(get_cities())
print(get_countries())

print(get_states())

print(get_place())
