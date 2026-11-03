
import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="marketing_elt_pipeline",
    description="End-to-end Marketing Analytics ELT Pipeline",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["marketing", "snowflake", "dbt", "elt"],
) as dag:

    # Task 1: Load CSV data into Snowflake RAW
    ingest_data = BashOperator(
        task_id="ingest_csv_to_snowflake",
        bash_command=(
            "/home/airflow/ingestion-venv/bin/python "
            "/opt/airflow/project/ingestion/load_to_snowflake.py"
        ),
        cwd="/opt/airflow/project",
    )

    # Task 2: Transform data using dbt
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "/home/airflow/dbt-venv/bin/dbt run "
            "--project-dir /opt/airflow/project/marketing_analytics_dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
        cwd="/opt/airflow/project",
    )

    # Task 3: Test data quality
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "/home/airflow/dbt-venv/bin/dbt test "
            "--project-dir /opt/airflow/project/marketing_analytics_dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
        cwd="/opt/airflow/project",
    )

    # Define execution order
    ingest_data >> dbt_run >> dbt_test
