from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# DAG definition
with DAG(
    dag_id='ventas360_pipeline',
    description='Orchestrates the ETL pipeline for Ventas360 using dbt and Snowflake',
    default_args=default_args,
    schedule_interval='@daily',  # Runs daily
    start_date=days_ago(1),
    catchup=False
) as dag:

    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='echo "Simulating data extraction and loading into Snowflake..."'
    )

    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command="""
        cd /path/to/dbt/project &&
        dbt run --profiles-dir . --target prod
        """
    )

    test_dbt_models = BashOperator(
        task_id='test_dbt_models',
        bash_command="""
        cd /path/to/dbt/project &&
        dbt test --profiles-dir . --target prod
        """
    )

    success_task = BashOperator(
        task_id='pipeline_success',
        bash_command='echo "Ventas360 pipeline completed successfully!"'
    )


    extract_data >> run_dbt_models >> test_dbt_models >> success_task
