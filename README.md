# NASA APOD ETL Pipeline with Airflow and PostgreSQL

This project builds a fully automated ETL (Extract, Transform, Load) pipeline to ingest NASA's Astronomy Picture of the Day (APOD) data using **Apache Airflow** and store it in a **PostgreSQL** database. The workflow is containerized using **Docker**, allowing for reproducible and scalable data ingestion.

---

## Project Overview

- Extracts daily image metadata from the [NASA APOD API](https://api.nasa.gov/)
- Transforms API responses into structured JSON format
- Loads transformed data into a PostgreSQL database
- Automates workflow using Airflow DAGs
- Runs locally inside Docker containers

---
## Tools & Technologies

- Apache Airflow
- PostgreSQL
- Docker & Docker Compose
- Python
- NASA APOD API
- PostgresHook, SimpleHttpOperator (Airflow)

---

## How It Works

1. **Extraction**  
   Uses `SimpleHttpOperator` to fetch data from the NASA APOD API.

2. **Transformation**  
   Converts the raw API response to a structured JSON format suitable for loading.

3. **Loading**  
   Inserts the transformed data into a PostgreSQL database using Airflow's `PostgresHook`.

4. **Automation**  
   The entire process is orchestrated through a scheduled Airflow DAG that runs daily.

---

## Running Locally with Docker

1. Clone the repo:

git clone https://github.com/Manidatta1/NASA-APOD-ETL-Pipeline-with-Airflow-and-Postgres.git
cd NASA-APOD-ETL-Pipeline-with-Airflow-and-Postgres

2. Start the Services

docker compose up

3. Access Airflow UI at: http://localhost:8080

---

## Author

ManiDatta
Master’s in Data Science @ University of Colorado Boulder

