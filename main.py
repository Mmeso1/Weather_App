from app import create_app
from dotenv import load_dotenv
from pprint import pprint
import requests
import os
# from jinja2 import Markup


load_dotenv()

app = create_app()

# Define custom Jinja2 filters to format date and time
def timestamp_to_date(timestamp):
    from datetime import datetime
    dt_object = datetime.utcfromtimestamp(timestamp)
    return dt_object.strftime('%A, %d %B %Y')

# Add the custom filter to the Jinja2 environment
app.jinja_env.filters['timestamp_to_date'] = timestamp_to_date

#I am leaving this here so i can know how to create my own filters incase his is the best way out
# @app.template_filter('weather_class')
# def weather_class(description):
#     weather_classes = {
#         'Clear': 'clear-weather',
#         'Sunny': 'sunny-weather',
#         'Rain': 'rainy-weather',
#         'Overcast': 'overcast-weather',
#         'Stormy': 'stormy-weather',
#         'Partly cloudy': 'cloudy-weather',      
#         'Cloudy': 'cloudy-weather',      
#     }

#     # Return the corresponding CSS class or 'default-weather' if not found
#     return weather_classes.get(description, 'default-weather')
   



if __name__ == '__main__':
    app.run(debug=True)