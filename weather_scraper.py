import requests
import time
import matplotlib.pyplot as plt
import datetime

# Define your OpenWeatherMap API Key and the city for which you want the weather data
API_KEY = 'YOUR_API_KEY'
CITY = 'Nashville'
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

# Function to fetch weather data
def fetch_weather_data():
    try:
        response = requests.get(URL)
        data = response.json()
        if data['cod'] == 200:
            main_data = data['main']
            temperature = main_data['temp']
            humidity = main_data['humidity']
            return temperature, humidity
        else:
            print("Error in fetching data.")
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Lists to store the temperature and humidity data
temperature_data = []
humidity_data = []
timestamps = []

# Collect weather data every 10 minutes for 2 hours (12 readings)
for _ in range(12):
    temperature, humidity = fetch_weather_data()
    if temperature is not None and humidity is not None:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamps.append(current_time)
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        print(f"Time: {current_time}, Temp: {temperature}°C, Humidity: {humidity}%")
    time.sleep(600)  # Wait for 10 minutes before fetching the next data point

# Plot temperature and humidity over time
fig, ax1 = plt.subplots()

ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature (°C)', color='tab:red')
ax1.plot(timestamps, temperature_data, color='tab:red', label='Temperature')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax2 = ax1.twinx()
ax2.set_ylabel('Humidity (%)', color='tab:blue')
ax2.plot(timestamps, humidity_data, color='tab:blue', label='Humidity')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# Rotate time labels for better visibility
plt.xticks(rotation=45, ha='right')

# Title and show plot
plt.title(f"Weather Data for {CITY}")
fig.tight_layout()
plt.show()
