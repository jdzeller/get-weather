import requests
import sys
import argparse

parser = argparse.ArgumentParser(description='Process Input.')
parser.add_argument('--lat', metavar='Latitude', dest='lat', help='latitude')
parser.add_argument('--lon', metavar='Longitude', dest='lon', help='longitude')
args = parser.parse_args()

def get_gridpoints(lat, lon):
    base_points_url = 'https://api.weather.gov/points/'
    location_points = lat + ',' + lon 
    call_points_url = base_points_url + location_points + '/stations'

    response = requests.get(call_points_url)
    response_data = response.json()

    closest_station = response_data['features'][0]['id']

    return closest_station

def get_weather_data(closest_station):
    closest_station_url = closest_station + '/observations/latest'

    response = requests.get(closest_station_url)
    response_data = response.json()

    return response_data

closest_station = get_gridpoints(args.lat, args.lon)
weather_data = get_weather_data(closest_station)

weather_data_titles = {
    'temperature': 'Temperature',
    'dewpoint': 'Dewpoint',
    'windDirection': 'Wind Direction',
    'windSpeed': 'Wind Speed',
    'windGust': 'Wind Gust',
    'barometricPressure': 'Barometric Pressure',
    'visibility': 'Visibility',
}

for key, value in weather_data_titles.items():
    unit_code = weather_data['properties'][key]['unitCode']
    unit_value = weather_data['properties'][key]['value']

    if unit_code == 'unit:degC':
        unit_value = round((unit_value * 9/5) + 32)

    print(value + ": " + str(unit_value))
