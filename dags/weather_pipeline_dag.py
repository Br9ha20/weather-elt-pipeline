from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_elt_pipeline',
    default_args=default_args,
    description='Daily Weather ELT Pipeline using Open-Meteo, Snowflake, and dbt',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['weather', 'elt', 'snowflake'],
) as dag:

    # Task 1: Run Python Extract Script
    extract_task = BashOperator(
        task_id='extract_data',
        bash_command='python /usr/local/airflow/include/extract.py',
    )

    # Task 2: Run Python Load Script to Snowflake
    load_task = BashOperator(
        task_id='load_to_snowflake',
        bash_command='python /usr/local/airflow/include/load.py',
    )

    # Task 3: Run dbt Transformations
    transform_task = BashOperator(
        task_id='dbt_transform',
        bash_command='cd /usr/local/airflow/include/weather_transformations && dbt run',
    )

    # Set Pipeline Dependency Order: Extract -> Load -> Transform
    extract_task >> load_task >> transform_task