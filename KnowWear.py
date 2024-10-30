import streamlit as st
import requests
from datetime import datetime
from http import HTTPStatus

location = "50014"
# Title for the Streamlit app
st.title("KnowWear")
st.subheader("When to Wear What")

def tomorrow_io(url):
    try:
        headers = {"accept": "application/json"}
        response = requests.get(url, headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            return data
        
        # Something went wrong
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            st.error("Error: Unauthorized. Check your API key.")
        elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            st.warning("Error: Rate limit exceeded. Try again later.")
        else:
            st.error(f"Error: Unexpected status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    return None  # Return None if there was an error

def get_current_weather():
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}%20US&units=imperial&apikey={st.secrets.Tomorrow_IO_Key}"
    return tomorrow_io(url)

def get_weather_forecast():
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}%20US&timesteps=1h&units=imperial&apikey={st.secrets.Tomorrow_IO_Key}"
    return tomorrow_io(url)

def get_weather_icon(weather_code):
    # Tomorrow.io weather code to OpenWeatherMap icon mapping
    weather_code_to_icon = {
        0: "http://openweathermap.org/img/wn/01d@2x.png",      # Clear day
        1000: "http://openweathermap.org/img/wn/01n@2x.png",   # Clear night
        1001: "http://openweathermap.org/img/wn/04d@2x.png",   # Cloudy
        1100: "http://openweathermap.org/img/wn/02d@2x.png",   # Mostly clear day
        1101: "http://openweathermap.org/img/wn/02n@2x.png",   # Mostly clear night
        1102: "http://openweathermap.org/img/wn/03d@2x.png",   # Partly cloudy
        2000: "http://openweathermap.org/img/wn/50d@2x.png",   # Fog
        2100: "http://openweathermap.org/img/wn/50n@2x.png",   # Light fog
        3000: "http://openweathermap.org/img/wn/02d@2x.png",   # Light wind
        4000: "http://openweathermap.org/img/wn/09d@2x.png",   # Drizzle
        4200: "http://openweathermap.org/img/wn/10d@2x.png",   # Light rain
        5000: "http://openweathermap.org/img/wn/13d@2x.png",   # Snow
        5001: "http://openweathermap.org/img/wn/13n@2x.png",   # Flurries
        5100: "http://openweathermap.org/img/wn/13d@2x.png",   # Light snow
        6000: "http://openweathermap.org/img/wn/09d@2x.png",   # Freezing drizzle
        7101: "http://openweathermap.org/img/wn/13d@2x.png",   # Heavy ice pellets
        8000: "http://openweathermap.org/img/wn/11d@2x.png",   # Thunderstorm
    }

    wc = int(weather_code)
    icon_url = weather_code_to_icon.get(wc, "http://openweathermap.org/img/wn/01d@2x.png")
    return icon_url

data = get_current_weather()

if data:
    current_weather = data['data']['values']
    temperature = current_weather["temperature"]
    humidity = current_weather["humidity"]
    wind_speed = current_weather["windSpeed"]
    precipitation = current_weather["precipitationProbability"]
    weather_code = current_weather["weatherCode"]

    icon = get_weather_icon(weather_code)

    # HTML formatted output
    html_output = f"""
    <div style='font-family: Arial; color: #333;'>
        <h2 style='color: #0059b3;'>Current Weather Conditions for {location}<img src='{get_weather_icon(weather_code)}'/></h2>
        <p><strong>Temperature:</strong> {temperature}°F</p>
        <p><strong>Humidity:</strong> {humidity}%</p>
        <p><strong>Wind Speed:</strong> {wind_speed} mph</p>
        <p><strong>Precipitation Intensity:</strong> {precipitation} inches/hour</p>
        <p><strong>Weather Code:</strong> {weather_code}</p>
    </div>
    """

    # Display the HTML in Streamlit
    st.markdown(html_output, unsafe_allow_html=True)
    #st.json(data)
else:
    st.warning("Unable to fetch weather data at the moment.")