import requests
import json
import argparse
import sys
import dotenv
import os

# load api key from .env file
dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')


# write a function that takes a city name and returns the current weather for that city
def get_weather(city):
    '''
    Get the current weather for a city. Handles exceptions using try/except.
    Args: city (str): The city to get the weather for.
    Returns: dict: The weather data.
    
    '''
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as err:
        print(f'Error occured while fetching the weather: {err}')
        sys.exit(1)

# print the data in a readable format
def print_weather(data):
    print(data)
    print(f'Current weather in {data["name"]}:')
    print(f'{data["weather"][0]["main"]} - {data["weather"][0]["description"]}')
    print(f'Temperature: {data["main"]["temp"]}')
    print(f'Feels like: {data["main"]["feels_like"]}')
    print(f'Humidity: {data["main"]["humidity"]}')
    print(f'Wind speed: {data["wind"]["speed"]}')

# write main function to take in command line arguments using argparse
def main():
    parser = argparse.ArgumentParser(description='Get the current weather for a city.')
    parser.add_argument('city', help='The city to get the weather for.')
    args = parser.parse_args()
    city = args.city
    data = get_weather(city)
    print_weather(data)

if __name__ == '__main__':
    main()