# import pandas as pd
# import json

# file_path = r"c:\Users\desai\OneDrive\Documents\Travel Guide Using AI\Travel-Guide-AI\travelling\Data\Location.json"
# # file_path = r"F:\____INFY_____\Travel-Guide-AI\travelling\Data\Location.json"


# with open(file_path, mode='r') as file:
#     data = json.load(file)


# def flatten_json(data):
#     flatten_data = []

#     def recurse(country, state, city, place):
#         flatten_data.append({
#             'country': country,
#             'state': state,
#             'city': city,
#             'place': place
#         })
    
#     for country, states in data.items():
#         for state, cities in states.items():
#             for city, places in cities.items():
#                 for place, details in places.items():
#                     recurse(country, state, city, place)

#     return flatten_data


# df = pd.DataFrame(flatten_json(data))


# def extract_countries() -> list:
#     global df
#     countries = [country for country in df['country'].unique()]
#     return countries

# def extract_states(country: str = None) -> list:
#     global df
#     if country:
#         # Filter states by the provided country
#         states = df[df['country'] == country]['state'].unique()
#     else:
#         # Return all unique states if no country is provided
#         states = df['state'].unique()
    
#     states = [state for state in states]
#     return states


# def extract_cities(state: str = None) -> list:
#     global df
#     if state:
#         # Filter cities by the provided state
#         cities = df[df['state'] == state]['city'].unique()
#     else:
#         # Return all unique cities if no state is provided
#         cities = df['city'].unique()
    
#     cities = [city for city in cities]
#     return cities


# def extract_places(city: str = None) -> list:
#     global df
#     if city:
#         # Filter by city if provided
#         places = df[df['city'] == city]['place'].unique()
#     else:
#         # Get all unique places if no city is provided
#         places = df['place'].unique()
    
#     # Convert to list
#     places = [place for place in places]
#     return places

import pandas as pd
import json
import os

file_path = r"c:\Users\desai\OneDrive\Documents\Travel Guide Using AI\Travel-Guide-AI\travelling\Data\Location.json"
# file_path = r"F:\____INFY_____\Travel-Guide-AI\travelling\Data\Location.json"


with open(file_path, mode='r') as file:
    data = json.load(file)


def flatten_json(data):
    flatten_data = []

    def recurse(country, state, city, place):
        flatten_data.append({
            'country': country,
            'state': state,
            'city': city,
            'place': place
        })

    for country, states in data.items():
        for state, cities in states.items():
            for city, places in cities.items():
                for place in places.keys():
                    recurse(country, state, city, place)

    return flatten_data


# Create DataFrame
df = pd.DataFrame(flatten_json(data))


# Function to extract unique countries
def extract_countries() -> list:
    return df['country'].unique().tolist()


# Function to extract unique states filtered by country (optional)
def extract_states(country: str = None) -> list:
    if country:
        states = df[df['country'] == country]['state'].unique()
    else:
        states = df['state'].unique()
    return states.tolist()


# Function to extract unique cities filtered by state (optional)
def extract_cities(state: str = None) -> list:
    if state:
        cities = df[df['state'] == state]['city'].unique()
    else:
        cities = df['city'].unique()
    return cities.tolist()


# Function to extract unique places filtered by city (optional)
def extract_places(city: str = None) -> list:
    if city:
        places = df[df['city'] == city]['place'].unique()
    else:
        places = df['place'].unique()
    return places.tolist()


# Test the functions (Optional - For Debugging)
if __name__ == "__main__":
    print("Countries:", extract_countries())
    print("States in 'India':", extract_states('India'))
    print("Cities in 'Rajasthan':", extract_cities('Rajasthan'))
    print("Places in 'Jaipur':", extract_places('Jaipur'))









