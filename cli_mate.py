import requests
import argparse
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
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as err:
        print(f'Error occured while fetching the weather for: {city}')
        return None

# write a function that take coordinates of a place and returns the current weather for that place
def get_weather_by_coords(lat, lon):
    '''
    Get the current weather for a place using coordinates.
    Args: lat (float): The latitude of the place.
          lon (float): The longitude of the place.
    Returns: dict: The weather data.
    
    '''
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as err:
        print(f'Error occured while fetching the weather for: {lat}, {lon}')
        return None

# print the data in a readable format
def print_weather(data):
    print('📍  Location:\t\t' + data['name'])
    print('🌤️  Current Weather:\t'+ data['weather'][0]['main'])
    print('🌡️  Temperature:\t' + str(data['main']['temp'])+'°C')
    print('💧  Humidity:\t\t' + str(data['main']['humidity'])+' %')
    print('💨  Wind speed:\t\t' + str(data['wind']['speed'])+' m/s')
    print('🧊 Pressure:\t\t' + str(data['main']['pressure'])+' hPa')
    

# write main function to take in command line arguments using argparse
# user can either enter a city name or coordinates
def main():
    parser = argparse.ArgumentParser(description='Get the current weather for a city or place.')
    parser.add_argument('-c', '--city', help='The city to get the weather for.')
    parser.add_argument('-lat', '--latitude', help='The latitude of the place.')
    parser.add_argument('-lon', '--longitude', help='The longitude of the place.')
    args = parser.parse_args()
    if args.city:
        data = get_weather(args.city)
        print_weather(data)
    elif args.latitude and args.longitude:
        data = get_weather_by_coords(args.latitude, args.longitude)
        print_weather(data)
    else:
        print('Please enter a city name or coordinates.')


if __name__ == '__main__':
    main()