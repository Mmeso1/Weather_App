
import json
from flask import Blueprint, render_template, request, session,jsonify,redirect,flash
import requests
from flask import request, jsonify
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Load environment variables from .env file
load_dotenv()


views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    city = request.args.get('city')
    default_city = "Germany"

    if city:
        weather_data = get_weather_details(city)
    else:
        weather_data = get_weather_details(default_city)

    if weather_data is None:
        return render_error_message(city if city else default_city)

    bbox = f"{weather_data['longitude'] - 0.1},{weather_data['latitude'] - 0.1},{weather_data['longitude'] + 0.1},{weather_data['latitude'] + 0.1}"
    return render_template('home.html', title='Home', weather_data=weather_data, map=bbox)

@views.route('/more_info/<int:day>', methods=['GET'])
def more_info(day):
    city = request.args.get('city')
    weather_data = get_weather_details(city)

    return render_template('more_info.html', title='More Info', selected_day=day, weather_data=weather_data)

@views.route('/future_cast/<int:day>', methods=['GET'])
def future_cast(day):
    city = request.args.get('city')
    weather_data = get_weather_details(city)

    return render_template('future_cast.html', title=f'Day {day + 1}', selected_day=day, weather_data=weather_data)

def render_error_message(city):
    flash(f"Weather data for {city} not found.\nInvalid city name or no city provided.", "error")
    return redirect ('/')

def get_weather_details(city):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {
        "q": city,
        "days": "3"  # Fetch data for 3 days
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        # Organize the weather data using the helper function
        weather_data = organize_weather_data(data)

        # To get the weather data info if the time is not yet gone
        for forecast_entry in weather_data['forecast_data']:
            forecast_entry['hourly_data'] = filter_hourly_data(forecast_entry['hourly_data'])


        return weather_data
    else:
        # Handle errors here, such as invalid city name or API rate limits
        return None
    
def organize_weather_data(data):
    location = data['location']
    current_data = data['current']
    forecast_data = data['forecast']['forecastday']

    # Initialize the main weather data dictionary
    weather_data = {
        'city': location['name'],
        'country': location['country'],
        'date': current_data['last_updated_epoch'],
        'weather_description': current_data['condition']['text'],
        'time': current_data['last_updated'],
        'temperature': current_data['temp_c'],
        'feels_like_temperature': current_data['feelslike_c'],
        'longitude': location['lon'],
        'latitude': location['lat'],
        'icon': current_data['condition']['icon'],
        'chance_of_rain': ['chance_of_rain'],
        'chance_of_snow': ['chance_of_snow'],
        'cloud': current_data['cloud'],
        'dewpoint_c': ['dewpoint_c'],
        'dewpoint_f': ['dewpoint_f'],
        'forecast_data': []
    }

    # Organize forecast data for the current day and the next two days
    for forecast in forecast_data[:3]:
        forecast_entry = {
            'date': forecast['date_epoch'],
            'weather_description': forecast['day']['condition']['text'],
            'icon': forecast['day']['condition']['icon'],
            'max_temp_c': forecast['day']['maxtemp_c'],
            'max_temp_f': forecast['day']['maxtemp_f'],
            'min_temp_c': forecast['day']['mintemp_c'],
            'min_temp_f': forecast['day']['mintemp_f'],
            'avg_temp_c': forecast['day']['avgtemp_c'],
            'avg_temp_f': forecast['day']['avgtemp_f'],
            'max_wind_mph': forecast['day']['maxwind_mph'],
            'max_wind_kph': forecast['day']['maxwind_kph'],
            'total_precip_mm': forecast['day']['totalprecip_mm'],
            'total_precip_in': forecast['day']['totalprecip_in'],
            'total_snow_cm': forecast['day']['totalsnow_cm'],
            'avg_visibility_km': forecast['day']['avgvis_km'],
            'avg_visibility_miles': forecast['day']['avgvis_miles'],
            'avg_humidity': forecast['day']['avghumidity'],
            'chance_of_rain': forecast['day']['daily_chance_of_rain'],
            'chance_of_snow': forecast['day']['daily_chance_of_snow'],
            'sunrise': forecast['astro']['sunrise'],
            'sunset': forecast['astro']['sunset'],
            'moonrise': forecast['astro']['moonrise'],
            'moonset': forecast['astro']['moonset'],
            'moon_phase': forecast['astro']['moon_phase'],
            'moon_illumination': forecast['astro']['moon_illumination'],
            'is_moon_up': forecast['astro']['is_moon_up'],
            'is_sun_up': forecast['astro']['is_sun_up'],
            'hourly_data': []
        }

        # Organize hourly weather data for each day
        hourly_forecast_data = forecast['hour']
        for hourly_data in hourly_forecast_data:
            hourly_entry = {
                'time_epoch': hourly_data['time_epoch'],
                'time': hourly_data['time'],
                'temp_c': hourly_data['temp_c'],
                'temp_f': hourly_data['temp_f'],
                'is_day': hourly_data['is_day'],
                'weather_description': hourly_data['condition']['text'],
                'wind_mph': hourly_data['wind_mph'],
                'wind_kph': hourly_data['wind_kph'],
                'wind_degree': hourly_data['wind_degree'],
                'wind_dir': hourly_data['wind_dir'],
                'pressure_mb': hourly_data['pressure_mb'],
                'pressure_in': hourly_data['pressure_in'],
                'precip_mm': hourly_data['precip_mm'],
                'precip_in': hourly_data['precip_in'],
                'humidity': hourly_data['humidity'],
                'cloud': hourly_data['cloud'],
                'feelslike_c': hourly_data['feelslike_c'],
                'feelslike_f': hourly_data['feelslike_f'],
                'windchill_c': hourly_data['windchill_c'],
                'windchill_f': hourly_data['windchill_f'],
                'heatindex_c': hourly_data['heatindex_c'],
                'heatindex_f': hourly_data['heatindex_f'],
                'dewpoint_c': hourly_data['dewpoint_c'],
                'dewpoint_f': hourly_data['dewpoint_f'],
                'will_it_rain': hourly_data['will_it_rain'],
                'chance_of_rain': hourly_data['chance_of_rain'],
                'will_it_snow': hourly_data['will_it_snow'],
                'chance_of_snow': hourly_data['chance_of_snow'],
                'vis_km': hourly_data['vis_km'],
                'vis_miles': hourly_data['vis_miles'],
                'gust_mph': hourly_data['gust_mph'],
                'gust_kph': hourly_data['gust_kph'],
                'uv': hourly_data['uv']
            }

            forecast_entry['hourly_data'].append(hourly_entry)

        weather_data['forecast_data'].append(forecast_entry)

    return weather_data

def filter_hourly_data(hourly_data):
    current_time_epoch = int(datetime.now().timestamp())

    # Define a time window (e.g., 15 minutes) around the current time
    time_window = timedelta(minutes=50).total_seconds()

    # Filter out hourly data within the time window
    filtered_hourly_data = [entry for entry in hourly_data if current_time_epoch - time_window <= entry['time_epoch'] <= current_time_epoch]

    return filtered_hourly_data
