#!/usr/bin/env python3

import requests
import sys
import argparse

parser = argparse.ArgumentParser(description='Get the weather for zip codes or lat/lon in the US.')
parser.add_argument('-z', metavar=' zip code', dest='zip', help='get weather by US zip code')
parser.add_argument('-la', metavar='lattitude', dest='lat', help='get weather by latitude/longitude')
parser.add_argument('-ln', metavar='longitude', dest='lon', help='get weather by latitude/longitude')
args = parser.parse_args()

# Function that uses the geonames API to convert US zip codes to lattitude/longitude
def get_lat_long(zip):
    base_zip_url = 'http://api.geonames.org/postalCodeLookupJSON?postalcode=' + str(zip) + '&country=US&username=jzeller'
    response = requests.get(base_zip_url)
    response_data = response.json()

    coord = dict()
    coord['lat'] = str(response_data['postalcodes'][0]['lat'])
    coord['lng'] = str(response_data['postalcodes'][0]['lng'])

    return coord

# Function that finds the closest NWS station by lattitude/longitude
def get_gridpoints(lat, lon):
    base_points_url = 'https://api.weather.gov/points/'
    location_points = lat + ',' + lon 
    call_points_url = base_points_url + location_points + '/stations'

    response = requests.get(call_points_url)
    response_data = response.json()

    closest_station = response_data['features'][0]['id']

    return closest_station

# Function that gets the latest weather data from the NWS station
def get_weather_data(closest_station):
    closest_station_url = closest_station + '/observations/latest'

    response = requests.get(closest_station_url)
    response_data = response.json()

    return response_data

if args.zip is not None:
    coord = get_lat_long(args.zip)
    closest_station = get_gridpoints(coord['lat'], coord['lng'])
else:
    closest_station = get_gridpoints(args.lat, args.lon)

weather_data = get_weather_data(closest_station)

weather_data_titles = {
    'temperature': 'Temperature',
    'dewpoint': 'Dewpoint',
    'windChill': 'Wind Chill',
    'windDirection': 'Wind Direction',
    'windSpeed': 'Wind Speed',
    'windGust': 'Wind Gust',
    'barometricPressure': 'Barometric Pressure',
    'visibility': 'Visibility',
}

for key, value in sorted(weather_data_titles.items()):
    unit_code = weather_data['properties'][key]['unitCode']
    unit_value = weather_data['properties'][key]['value']

    if unit_code == 'unit:degC':
        unit_value = round((unit_value * 9/5) + 32)
    elif unit_code == 'unit:Pa':
        unit_value = round(unit_value * 0.00029530, 2)

    print(value + ": " + str(unit_value))
