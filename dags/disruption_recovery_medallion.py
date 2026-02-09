from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.bronze_ingest import build_bronze
from scripts.silver_instability import build_silver
from scripts.gold_decision_view import build_gold


with DAG(
    dag_id="disruption_recovery_medallion",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["disruption", "medallion"],
) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_ingest",
        python_callable=build_bronze,
    )

    silver_task = PythonOperator(
        task_id="silver_instability",
        python_callable=build_silver,
    )

    gold_task = PythonOperator(
        task_id="gold_decision_view",
        python_callable=build_gold,
    )

    bronze_task >> silver_task >> gold_task
