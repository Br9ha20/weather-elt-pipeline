# Modern Automated Weather ELT Pipeline

An end-to-end weather ELT pipeline that extracts live data from Open-Meteo,
loads it into Snowflake, transforms it with dbt, and orchestrates the workflow
with Apache Airflow in Docker containers.

## Tech Stack

- **Language:** Python 3.x and SQL
- **Orchestration:** Apache Airflow, Astro CLI, and Docker Desktop
- **Data warehouse:** Snowflake
- **Transformation:** dbt
- **Data source:** Open-Meteo REST API

## Pipeline Architecture

1. **Extract:** `include/extract.py` fetches hourly temperature and humidity
   data for Kathmandu from Open-Meteo and writes `raw_weather_data.csv`.
2. **Load:** `include/load.py` uploads the CSV to
   `MY_FIRST_PIPELINE.RAW.RAW_WEATHER` using the Snowflake Pandas connector.
3. **Transform:** dbt models in
   `include/weather_transformations/models/` convert temperatures to Fahrenheit
   and categorize humidity in `STG_WEATHER`.
4. **Orchestrate:** `dags/weather_pipeline_dag.py` runs the steps daily in
   Extract -> Load -> Transform order, with automatic retries.

## Repository Structure

```text
weather-elt-pipeline/
├── .gitignore
├── README.md
├── dags/
│   └── weather_pipeline_dag.py
├── include/
│   ├── extract.py
│   ├── load.py
│   └── weather_transformations/
│       ├── dbt_project.yml
│       ├── profiles.yml.example
│       └── models/
│           ├── schema.yml
│           └── stg_weather.sql
└── requirements.txt
```

The Astro `Dockerfile`, project tests, and local Astro configuration remain in
the repository because they are required to run the pipeline locally.

## Run Locally

### Prerequisites

- Docker Desktop
- Astro CLI
- A Snowflake account

Install the Astro CLI on Windows with:

```powershell
winget install -e --id Astronomer.Astro
```

### Configure Snowflake

Copy `include/weather_transformations/profiles.yml.example` to your dbt user
configuration directory as `~/.dbt/profiles.yml`. Set the following environment
variables in the terminal or in a local, untracked `.env` file:

```text
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=SYSADMIN
SNOWFLAKE_DATABASE=MY_FIRST_PIPELINE
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_SCHEMA=RAW
```

Never commit real passwords, tokens, private keys, `.env`, or
`profiles.yml`. The repository contains only `profiles.yml.example` with
environment-variable references.

### Start Airflow

From the repository root:

```powershell
astro dev start
```

Open the Airflow UI at <http://localhost:8080>.

To stop the local services:

```powershell
astro dev stop
```

### Run Tests

```powershell
pytest tests
```

## GitHub Safety Checklist

Before pushing:

```powershell
git status
git diff --check
git grep -n -I -E "password\s*=|token\s*=|secret\s*="
```

The final command should not report real credentials. If credentials were
previously committed, rotate them in Snowflake before publishing the repository.
