import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

schedule_job = datetime(2018, 4, 5, 14, 0, 0, 0)


def build_dag_args(schedule_job, email_on_failure=True, email_on_retry=True,
                   retries=2, retry_delay_in_minutes=2):
    return {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': schedule_job,
        'email': ['airflow'],
        'email_on_failure': email_on_failure,
        'email_on_retry': email_on_retry,
        'retries': retries,
        'retry_delay': timedelta(minutes=retry_delay_in_minutes),
    }

dag = DAG('airflow-travis-test',
          default_args=build_dag_args(schedule_job=schedule_job),
          description='travis-test',
          schedule_interval='* * * * *',
          dagrun_timeout=timedelta(hours=1))

def print_context(ds, **kwargs):
    print('Whatever you return gets printed in the logs')

first = PythonOperator(
    task_id='first',
    provide_context=True,
    python_callable=print_context,
    dag=dag)


second = PythonOperator(
    task_id='second',
    provide_context=True,
    python_callable=print_context,
    dag=dag)


third = PythonOperator(
    task_id='third',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

first >> second
second >> third