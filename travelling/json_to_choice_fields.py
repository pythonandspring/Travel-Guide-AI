import pandas as pd
import json

# file_path = r"c:\Users\desai\OneDrive\Documents\Travel Guide Using AI\Travel-Guide-AI\travelling\Data\Location.json"
file_path = r"F:\____INFY_____\Travel-Guide-AI\travelling\Data\Location.json"

with open(file_path, mode='r') as file:
    data = json.load(file)


def flatten_json(data):
    flatten_data = []

    def recurse(state, city, place):
        flatten_data.append({
            'state': state,
            'city': city,
            'place': place
        })
    
    for state, cities in data.items():
        for city, places in cities.items():
            for place in places:
                recurse(state,city,place)

    return flatten_data


df = pd.DataFrame(flatten_json(data))


def extract_state():
    global df

    states = [state for state in df['state'].unique()]
    return states


def extract_cities(state: str) -> list:
    global df

    cities = df[df['state'] == state]['city'].unique()
    cities = [city for city in cities]
    return cities


def extract_place(city: str) -> list:
    global df

    places = df[df['city'] == city]['place'].unique()
    places = [place for place in places]
    return places













