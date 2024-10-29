import streamlit as st  # pip install streamlit
import pandas as pd # pip install pandas
from datetime import datetime
import requests

# You must run this in the terminal: streamlit run knowwear.py
# Or: set a break point and run the debugger in Python Streamlit(!) mode

st.title('KnowWear')

wb_api_key = st.secrets.WeatherBit_Key
city = "Ames, IA"
url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={city}&key={wb_api_key}&days=10"

response = requests.get(url)
data = response.json()

# Show the 10 day temperature forecast
forecast_data = {
    "Date": [
        datetime.strptime(day['datetime'], "%Y-%m-%d").strftime("%a, %m/%d")
        for day in data["data"]
    ],
    "Temperature (°F)": [(day['temp'] * 9/5) + 32 for day in data["data"]],
    "Min Temp (°F)": [(day['min_temp'] * 9/5) + 32 for day in data["data"]],
    "Max Temp (°F)": [(day['max_temp'] * 9/5) + 32 for day in data["data"]],
    "Precipitation (inches)": [day['precip'] for day in data["data"]],
    "Wind Speed (mph)": [day['wind_spd'] * 2.237 for day in data["data"]],  # Convert m/s to mph
    "Weather Description": [day['weather']['description'] for day in data["data"]]
}

# Create DataFrame
df_forecast = pd.DataFrame(forecast_data)

# Step 3: Display DataFrame and Visualize in Streamlit
st.title(f"10-Day Weather Forecast for {city}")
st.write("### Forecast Data")
st.dataframe(df_forecast)

# Show bar chart with temperature and precipitation
st.write("### Temperature and Precipitation Forecast")
chart_data = df_forecast[["Date", "Temperature (°F)"]]
chart_data.set_index("Date", inplace=True)
st.line_chart(chart_data)