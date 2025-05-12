from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
import json


## Define the DAG
with DAG(
    dag_id = 'nasa_postgres',
    start_date = datetime(2024,4,25),
    schedule = "@daily",
    catchup= False
) as dag:
    
    ## step 1: Create the table if it doesn't exists
    @task
    def create_table():
        # initialize the postgress hook to interact with the postgresSQL
        postgres_hook = PostgresHook(postgres_conn_id = "my_postgres_connection")

        # SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(50),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        )
        """
        ## Execute the table creation query
        postgres_hook.run(create_table_query)



    ## step 2: extract the NASA API data(APOD data)
    extract_apod = HttpOperator(
        task_id = "extract_epod", # id of this particular task
        http_conn_id ="nasa_api", # connection ID which will be defined in airflow for NASA API
        endpoint= 'planetary/apod', # NASA API endpoint for APOD
        method = "GET",
        data = {"api_key":"{{conn.nasa_api.extra_dejson.api_key}}"},
        response_filter = lambda response:response.json() # converts the response from the http request to the json format.

        #You (or admin) manually create a Connection in Airflow.

        #Go to Airflow UI → Admin → Connections → Add Connection.

        #Create a connection with:

        #Conn ID: nasa_api

        #Conn Type: HTTP

        #Host: https://api.nasa.gov/
        
        # the api key will be specifiecd in the airflow, connection settings as json box in the extra field

        # when the airflow runs the DAG it looks for:
         # connection with ID nasa_api
         # Reads the extra field inside it (extra_dejson means deserialize JSON).
         # Finds the value associated with "api_key".

        # At runtime, Airflow replaces "{{conn.nasa_api.extra_dejson.api_key}}" with your actual API key.

        # Final HTTP request goes with the real API key.

    )


    ## step 3: Transform the data 
    @task
    def transform_data(response):
        apod_data={
            'title': response.get('title',''),
            'explanation': response.get('explanation',''),
            'url': response.get('url',''),
            'date': response.get('date',''),
            'media_type': response.get('media_type','')
        }
        return apod_data



    ## step 4: Load the data into Postgres SQL
    @task
    def load_data(apod_data):
        ## initalizing the postgreshook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        
        # SQL insert query

        insert_query= """
        INSERT INTO apod_data(title, explanation, url, date, media_type)
        VALUES (%s,%s,%s,%s,%s);
        """
        # Executing the SQL query
        postgres_hook.run(insert_query,parameters=(
           apod_data['title'],
           apod_data['explanation'],
           apod_data['url'],
           apod_data['date'],
           apod_data['media_type'],
        ))


    ## step 6: define the task dependencies
    create_table() >> extract_apod
    transformed_data = transform_data(extract_apod.output)
    load_data(transformed_data)



#  To view the postgres database, open the DBeaver