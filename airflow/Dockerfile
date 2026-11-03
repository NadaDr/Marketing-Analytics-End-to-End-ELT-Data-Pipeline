
FROM apache/airflow:3.3.2

USER airflow

# Environment 1: Python ingestion
RUN python -m venv /home/airflow/ingestion-venv && \
    /home/airflow/ingestion-venv/bin/pip install --no-cache-dir \
    "pandas==2.3.3" \
    "python-dotenv" \
    "snowflake-connector-python[pandas]"

# Environment 2: dbt transformations
RUN python -m venv /home/airflow/dbt-venv && \
    /home/airflow/dbt-venv/bin/pip install --no-cache-dir \
    "dbt-core==1.12.6" \
    "dbt-snowflake==1.12.4"
