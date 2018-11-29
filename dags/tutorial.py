"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/incubator-airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
from pprint import pprint

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('my_tutorial', default_args=default_args, schedule_interval=None)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='echo {{ dag_run.conf.hello }}',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)


def print_context(ds, **kwargs):
    pprint(kwargs)
    pprint(kwargs['dag_run'].conf)
    print(ds)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

t1.set_upstream(run_this)
t2.set_upstream(t1)
t3.set_upstream(t1)

if __name__ == "__main__":
    """
        curl -X POST \
        http://localhost:8080/api/experimental/dags/my_tutorial/dag_runs \
        -H 'Cache-Control: no-cache' \
        -H 'Content-Type: application/json' \
        -d '{"conf":"{\"hello\":\"world\"}"}'
    This curl call works
    The conf value MUST be a json string
        data = {'conf': json.dumps({
            'hello': 'DOES THIS WORK'
        })}
        res = requests.post('http://localhost:8080/api/experimental/dags/my_tutorial/dag_runs', json=data)
    """
    data_dict = {'conf': json.dumps({
        'hello': 'DOES THIS WORK'
    })}

    res = requests.post('http://localhost:8080/api/experimental/dags/my_tutorial/dag_runs', json=data_dict)
    print(res.content)
