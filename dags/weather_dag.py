from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json
import pandas as pd
import boto3
from io import StringIO
from airflow.models import Variable

city_name='Houston'
api_key= Variable.get("weather_api_key")

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit

def weather_data_extract(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")

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
    
# ----------- Airflow ------

default_args ={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG('weather_dag', 
         default_args=default_args, 
         schedule_interval='@daily', 
         catchup=False) as dag:
    
        is_weather_api_ready = HttpSensor(
            task_id='is_weather_api_ready',
            http_conn_id='weather_api',
            endpoint=f'/data/2.5/weather?q={city_name}&appid={api_key}'
        )
        
        extract_weather_data = SimpleHttpOperator(
            task_id='extract_weather_data',
            http_conn_id='weather_api',
            endpoint=f'/data/2.5/weather?q={city_name}&appid={api_key}',
            method='GET',
            response_filter=lambda response: json.loads(response.text),
            log_response=True
        )
        
        transform_load_weather_data = PythonOperator(
            task_id="transform_load_weather_data",
            python_callable=weather_data_extract
        )
        
        
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data