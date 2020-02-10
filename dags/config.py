import os
AIRFLOW_ADMIN_URL = '{}{}/admin/airflow/graph?dag_id=sequencer_automation'.format(os.environ.get('AIRFLOW_URL'),
                                                                                  os.environ.get('AIRFLOW_PORT'))
