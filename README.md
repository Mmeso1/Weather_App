# Weather_App
A weather app that was built with Python and Flask that tells you the weather of the day and next 2 days depending on the country, also the weather per hour of the day

## Getting Started
Clone the repository:
```bash
git clone https://github.com/Mmeso1/Weather_App.git
```

## Navigate to the project directory:
```bash
cd Weather_App
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Create a .env file in the project root and add the required environment variables:
```env
SECRET_KEY=your_secret_key_here
```

### Run the application:
``` bash
python Weather_App/__init__.py
```
-- The Flask app will be accessible at http://127.0.0.1:5000/.

## App Structure
The app consists of the following files and directories:

- Weather_App/__init__.py: Flask app initialization and configuration.
- Weather_App/views.py: Flask blueprint for defining routes and views.
- templates/index.html: HTML template for the main page.
- templates/future_cast.html: HTML template for the future forecast page.
- templates/home.html: HTML template for the home page.
- templates/more_info.html: HTML template for detailed weather information.

### Features
- Home Page: Enter the city to get current weather and a 2-day forecast.
- Future Forecast: View detailed hourly weather information for the next 2 days.
- More Info: Explore additional details such as temperature, time, and weather description.

### Built With
Flask: A micro web framework for Python.
OpenStreetMap: Used for displaying location maps.
jQuery: A fast, small, and feature-rich JavaScript library.

### Acknowledgments
Thanks to OpenWeather for providing weather data.
