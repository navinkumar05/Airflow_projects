from datetime import datetime
import pandas as pd
# import json
import requests
import boto3
import os
from io import StringIO
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'E://POC//Airflow_docker_setup//.env'))

city_name='Houston'
api_key=os.getenv('api_key')

full_url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit

def weather_data_extract(full_url):
    data=requests.get(full_url).json()

    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels Like (F)": feels_like_farenheit,
                        "Minimun Temp (F)":min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }
    
    # Generate a timestamp for the output directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    df_data = pd.DataFrame([transformed_data])
    # df_data.to_csv(f"weather_{city}_{timestamp}.csv", index=False)
    
    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    df_data.to_csv(csv_buffer, index=False)

    # AWS S3 bucket details
    bucket_name = 'snowflake-db-prac'
    file_name = f"weather_{city}_{timestamp}.csv"

    # Initialize a session using boto3
    s3 = boto3.client('s3')

    # Upload the CSV to S3
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())

if __name__ == '__main__':
    weather_data_extract(full_url)