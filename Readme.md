# open weather data extraction using Apache Airflow

## Project Overview
The Open Weather Data Pipeline (ETL) project is designed to extract, transform, and load weather data from the OpenWeather API into an AWS S3 bucket. This project leverages Apache Airflow for orchestrating the ETL process, using Python scripts for data extraction and transformation. The entire setup is deployed within Docker containers using Docker Compose

### Objectives:
- **Extract:** Fetch weather data from the OpenWeather API.
- **Transform:** Process and structure the data for storage.
- **Load:** Store the transformed data in an AWS S3 bucket.
- **Orchestrate:** Use Apache Airflow to schedule and manage the ETL process.
- **Deploy:** Use Docker and Docker Compose to containerize and deploy the Airflow instance.

<img src="Attachments\weather_data_ETL_airflow_architecture_diagram.drawio (1).png" width=700>

## Tools overview:

- **Apache Aireflow:** Used to define ETL tasks as Directed Acyclic Graphs (DAGs) and ensures that each task is executed in the correct order with proper dependency management.
- **Python:** Used transform the data using pandas library.
- **Docker & Dcoker Compose:** Used to containerize the Airflow setup and running multi-container Docker applications. With a simple YAML file, it allows us to configure the services (like Airflow, Postgres, etc.), networks, and volumes required for the project. It simplifies the orchestration of the containers, making it easier to manage and deploy the entire application stack.

## References:

- [How to build and automate a python ETL pipeline with airflow on AWS EC2 | Data Engineering Project](https://www.youtube.com/watch?v=uhQ54Dgp6To)
- [Extract current weather data from Open Weather Map API using python on AWS EC2](https://www.youtube.com/watch?v=0_caTDCZnd0)
- [Twitter Data Pipeline using Airflow for Beginners | Data Engineering Project](https://www.youtube.com/watch?v=q8q3OFFfY6c&t=1893s)
- [How to Upload files from local to AWS S3 using Python (Boto3) API | upload_file method |Handson Demo](https://www.youtube.com/watch?v=s9PVPijAw3I)
