from airflow import DAG
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.sftp_operator import SFTPOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import os
from pprint import pprint
from nyuad_cgsb_jira_client.jira_client import jira_client

try:
    from .ensure_samplesheet import validate_sample_names_from_work_dir
except Exception as e:
    from ensure_samplesheet import validate_sample_names_from_work_dir

AIRFLOW_ADMIN_URL = '{}{}/admin/airflow/graph?dag_id=sequencer_automation'.format(os.environ.get('AIRFLOW_URL'),
                                                                                  os.environ.get('AIRFLOW_PORT'))

"""Sequence Automation Tasks

Description: This is a workflow that goes from demultiplexing runs on /work, rsyncing them to /scratch, 
    tars the raw run along with the demultiplexed fastqs, runs an md5sum check, and archives the whole lot of it 
    
Example Conf Parameters:
        'work_dir': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
        'scratch_dir': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq'

copy_ssh_helpers_script_task
    description: Copies the ssh_helpers.py script to the run folder (so there is always a current record in case it changes) 
    host: dalma.abudhabi.nyu.edu
    operator: SFTPOperator
    dependencies: none 
    
Demultiplex Tasks

copy_ensure_samplesheet_task
    description: Copies the ensure_samplesheet.py script to the run folder (so there is always a current record in case it changes) 
    host: dalma.abudhabi.nyu.edu
    operator: SFTPOperator
    dependencies: copy_ssh_helpers_script_task 
    
ensure_samplesheet_task
    description: Copies the run_bcl2fastq.py script to the run folder (so there is always a current record in case it changes) 
    host: dalma.abudhabi.nyu.edu
    operator: SSHOperator
    dependencies: copy_ensure_samplesheet_task 

copy_demultiplex_script_task
    description: Copies the run_bcl2fastq.py script to the run folder (so there is always a current record in case it changes) 
    host: dalma.abudhabi.nyu.edu
    operator: SFTPOperator
    dependencies: copy_ssh_helpers_script_task 

demultiplex_task
    description: Runs the previously copied run_bcl2fastq script (from the run folder) and runs it. This uses bcl2fastq to demultiplex the run
        outputs - Unaligned/Stats and Unaligned/Reports  
        TODO Generate a report that indicates whether or not sample fails
    host: compute-15
    operator: SSHOperator
    dependencies: copy_demultiplex_script_task
    
rsync_work_task
    description: Rsyncs the demultiplexed reads from $WORK to $SCRATCH
    host: dalma.abudhabi.nyu.edu
    operator: SSHOperator
    dependencies: demultiplex_task
    
copy_tar_run_script_task
    description: Copies the tar_run_folder.py script to the run folder
    host: dalma.abudhabi.nyu.edu
    operator: SFTP
    dependencies: rsync_work_task
    
tar_run_folder_task
    description: Tars the run folder and runs an md5sum check
    host: compute-15-1
    operator: SSHOperator
    dependencies: copy_tar_run_script_task

copy_archive_run_script_task
    description: Copies the archive_run_folder to the run dir
    host: dalma.abudhabi.nyu.edu 
    operator: SFTPOperator
    dependencies: tar_run_folder_task

archive_run_folder_task
    description: Archives the tarred run
    host: archive3 
    operator: SSHOperator
    TODO: Figure out md5sum checks - I can run the md5sum, but then how to run it from archive?
    dependencies: copy_archive_run_script_task

SSH Hook Info

The SSH Hook must be declared in the Airflow UI

Most of it is self explanatory, but for an automatic ssh connection you must set the following in the 'extra' field of the UI 
extra: {"key_file": "/Users/jillian/.ssh/id_rsa", "no_host_key_check": true}
"""

this_env = os.environ.copy()

this_dir = os.path.dirname(os.path.realpath(__file__))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def update_jira_ticket_start_progress(context):
    """ Context looks like this:
    {'END_DATE': '2018-12-09',
     'conf': <module 'airflow.configuration' from '/Users/jillian/software/airflow/lib/python3.6/site-packages/airflow/configuration.py'>,
     'dag': <DAG: sequencer_automation>,
     'dag_run': <DagRun sequencer_automation @ 2018-12-09 09:24:04+00:00: 2018-12-9-12:24:04--JIRA-NCS-167--WORK_DIR-181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST, externally triggered: True>,
     'ds': '2018-12-09',
     'ds_nodash': '20181209',
     'end_date': '2018-12-09',
     'execution_date': <Pendulum [2018-12-09T09:24:04+00:00]>,
     'inlets': [],
     'latest_date': '2018-12-09',
     'macros': <module 'airflow.macros' from '/Users/jillian/software/airflow/lib/python3.6/site-packages/airflow/macros/__init__.py'>,
     'next_ds': None,
     'next_execution_date': None,
     'outlets': [],
     'params': {},
     'prev_ds': None,
     'prev_execution_date': None,
     'run_id': '2018-12-9-12:24:04--JIRA-NCS-167--WORK_DIR-181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST',
     'tables': None,
     'task': <Task(SFTPOperator): sftp_put_ssh_helpers_script>,
     'task_instance': <TaskInstance: sequencer_automation.sftp_put_ssh_helpers_script 2018-12-09T09:24:04+00:00 [success]>,
     'task_instance_key_str': 'sequencer_automation__sftp_put_ssh_helpers_script__20181209',
     'test_mode': False,
     'ti': <TaskInstance: sequencer_automation.sftp_put_ssh_helpers_script 2018-12-09T09:24:04+00:00 [success]>,
     'tomorrow_ds': '2018-12-10',
     'tomorrow_ds_nodash': '20181210',
     'ts': '2018-12-09T09:24:04+00:00',
     'ts_nodash': '20181209T092404+0000',
     'var': {'json': None, 'value': None},
     'yesterday_ds': '2018-12-08',
     'yesterday_ds_nodash': '20181208'
    }"""
    run_id = context['run_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    work_dir = context['dag_run'].conf['work_dir']
    comment = '*Run Started*: [View Progress | {}&run_id={} ] on {}'.format(AIRFLOW_ADMIN_URL, run_id, work_dir)
    jira_client.add_comment(jira_ticket, comment)
    return


def update_jira_ticket_success(context):
    pprint(context)
    pprint(context['dag_run'].conf)
    run_id = context['run_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    comment = '{}*Task Complete*{}: {} [View Progress | {}&run_id={} ]' \
        .format('{color:green}', '{color}', context['task'], AIRFLOW_ADMIN_URL, run_id)
    jira_client.add_comment(jira_ticket, comment)
    return


def update_jira_ticket_failure(context):
    """ Update the JIRA ticket with failure status
    TODO - Get the URL of the failed log"""
    pprint(context)
    pprint(context['dag_run'].conf)
    run_id = context['run_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    comment = '{}*Task Failed*{}: {} [View Logs | {}&run_id={} ]' \
        .format('{color:red}', '{color}', context['task'], AIRFLOW_ADMIN_URL, run_id)
    jira_client.add_comment(jira_ticket, comment)
    return


def update_jira_ticket_invalid_sample_names(context, invalid_sample_names, valid_sample_names):
    jira_ticket = context['dag_run'].conf['jira_ticket']
    if not len(valid_sample_names):
        comment = '{}*No valid samples were found*{}' \
            .format('{color:red}', '{color}')
        jira_client.add_comment(jira_ticket, comment)
    if len(invalid_sample_names):
        comment = '{}*The following sample names are invalid:*{}\n{}' \
            .format('{color:red}', '{color}', '\n'.join(invalid_sample_names))
        jira_client.add_comment(jira_ticket, comment)

    if not len(valid_sample_names) or len(invalid_sample_names):
        raise Exception
    else:
        return


def ensure_valid_sample_names_from_sample_sheet(ds, **kwargs):
    """
    Sample names can only contain alphanumeric characters, _, and -.
    If they contain other characters bcl2fastq will DIE
    :return:
    """
    work_dir = kwargs['dag_run'].conf['work_dir']
    valid_sample_names, invalid_sample_names = validate_sample_names_from_work_dir(ssh_hook=ssh_hook, work_dir=work_dir)
    if len(valid_sample_names):
        print('Found Valid Sample Names:\n{}'.format('\n'.join(valid_sample_names)))
    else:
        print('No valid sample names were found!')
    if len(invalid_sample_names):
        print('Found InValid Sample Names:\n{}'.format('\n'.join(invalid_sample_names)))
    else:
        print('No invalid sample names were found.')

    update_jira_ticket_invalid_sample_names(kwargs, invalid_sample_names=invalid_sample_names,
                                            valid_sample_names=valid_sample_names)
    return


dag = DAG('sequencer_automation', default_args=default_args, schedule_interval=None)
ssh_hook = SSHHook(ssh_conn_id='gencore@dalma.abudhabi.nyu.edu')
ssh_hook.no_host_key_check = True

copy_ssh_helpers_script_task = SFTPOperator(
    task_id='sftp_put_ssh_helpers_script',
    local_filepath=os.path.join(this_dir,
                                'ssh_helpers.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/ssh_helpers.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
    on_success_callback=update_jira_ticket_start_progress,
    on_failure_callback=update_jira_ticket_failure,
)

copy_ensure_samplesheet_task = SFTPOperator(
    task_id='sftp_put_ensure_samplesheet_script',
    local_filepath=os.path.join(this_dir,
                                'ensure_samplesheet.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/ensure_samplesheet.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
    on_failure_callback=update_jira_ticket_failure,
)
ensure_samplesheet_command = """
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ dag_run.conf["work_dir"] }}"
        python3 ensure_samplesheet.py --run-dir {{ dag_run.conf["work_dir"] }}
"""

ensure_samplesheet_task = SSHOperator(
    task_id='ensure_samplesheet',
    command=ensure_samplesheet_command,
    ssh_hook=ssh_hook,
    retries=1,
    do_xcom_push=True,
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag
)

validate_sample_names_task = PythonOperator(
    task_id='validate_sample_names',
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag,
    python_callable=ensure_valid_sample_names_from_sample_sheet,
    provide_context=True,
)

copy_demultiplex_script_task = SFTPOperator(
    task_id='sftp_put_demultiplex_script',
    local_filepath=os.path.join(this_dir,
                                'run_bcl2fastq.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/run_bcl2fastq.py',
    operation='put',
    ssh_hook=ssh_hook,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag,
)

demultiplex_command = """
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ dag_run.conf["work_dir"] }}"
        python3 run_bcl2fastq.py --run-dir {{ dag_run.conf["work_dir"] }}
"""

demultiplex_task = SSHOperator(
    task_id='demultiplex',
    command=demultiplex_command,
    ssh_hook=ssh_hook,
    retries=1,
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    do_xcom_push=True,
    dag=dag
)


# Normally I would do this with the SFTP Operator
# but I cannot figure out hwo to sftp a directory through the paramiko / airflow interface


def update_jira_ticket_demultiplex_report_url(context):
    work_dir = context['dag_run'].conf['work_dir']
    url = work_dir.replace("/work/gencore/", "")
    url = 'https://{}{}/{}/Unaligned/Reports/html/index.html'.format(os.environ.get('AIRFLOW_URL'),
                                                                     os.environ.get('NGINX_PORT'), url,
                                                                     'Unaligned/Reports/html/index.html')
    jira_ticket = context['dag_run'].conf['jira_ticket']
    comment = '*Demultiplex Reports*: {} [Reports | {}'.format(url)
    jira_client.add_comment(jira_ticket, comment)
    return


rsync_demultiplex_reports_dirs_command = """
    mkdir -p /home/airflow/html/{{ dag_run.conf["work_dir"].replace("/work/gencore", "") }}/Unaligned
    rsync -avz gencore@dalma.abudhabi.nyu.edu:{{ dag_run.conf["work_dir"] }}/Unaligned/Reports \
     /home/airflow/html/{{ dag_run.conf["work_dir"].replace("/work/gencore", "") }}/Unaligned/
"""
rsync_demultiplex_reports_dirs = BashOperator(
    task_id='create_demultiplex_reports_dirs',
    dag=dag,
    retries=4,
    bash_command=rsync_demultiplex_reports_dirs_command,
    on_success_callback=update_jira_ticket_demultiplex_report_url,
    on_failure_callback=update_jira_ticket_failure,
)

rsync_work_command = """
        echo "{{ ds }}"
        {{ dag_run.conf["work_dir"] if dag_run else "exit 256" }}
        mkdir -p {{ dag_run.conf["scratch_dir"] }}
        rsync -av "{{ dag_run.conf["work_dir"] }}/Unaligned" "{{ dag_run.conf["scratch_dir"] }}/"
"""
rsync_work_task = SSHOperator(
    task_id='rsync_work_scratch',
    ssh_hook=ssh_hook,
    command=rsync_work_command,
    retries=5,
    retry_delay=10,
    do_xcom_push=True,
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag
)

copy_tar_run_script_task = SFTPOperator(
    task_id='sftp_put_tar_run_script',
    local_filepath=os.path.join(this_dir,
                                'tar_run_folder.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/tar_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag,
)

tar_run_folder_command = """
        echo "{{ ds }}"
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ dag_run.conf["work_dir"] }}"
        python3 tar_run_folder.py --run-dir {{ dag_run.conf["work_dir"] }}
"""
tar_run_folder_task = SSHOperator(
    task_id='tar_run_folder_task',
    ssh_hook=ssh_hook,
    command=tar_run_folder_command,
    retries=5,
    retry_delay=10,
    do_xcom_push=True,
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag
)

copy_archive_run_script_task = SFTPOperator(
    task_id='sftp_put_archive_run_script',
    local_filepath=os.path.join(this_dir,
                                'archive_run_folder.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/archive_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag,
)

archive_run_folder_command = """
        echo "{{ ds }}"
        module load gencore gencore_anaconda/3-4.0.0
        cd "{{ dag_run.conf["work_dir"] }}"
        python3 archive_run_folder.py --run-dir {{ dag_run.conf["work_dir"] }}
"""
archive_run_folder_task = SSHOperator(
    task_id='archive_run_dir_task',
    ssh_hook=ssh_hook,
    command=archive_run_folder_command,
    retries=5,
    retry_delay=100,
    do_xcom_push=True,
    on_success_callback=update_jira_ticket_success,
    on_failure_callback=update_jira_ticket_failure,
    dag=dag
)

copy_ensure_samplesheet_task.set_upstream(copy_ssh_helpers_script_task)
ensure_samplesheet_task.set_upstream(copy_ensure_samplesheet_task)
validate_sample_names_task.set_upstream(ensure_samplesheet_task)
copy_demultiplex_script_task.set_upstream(validate_sample_names_task)
demultiplex_task.set_upstream(copy_demultiplex_script_task)
rsync_demultiplex_reports_dirs.set_upstream(demultiplex_task)
rsync_work_task.set_upstream(demultiplex_task)
copy_tar_run_script_task.set_upstream(rsync_work_task)
tar_run_folder_task.set_upstream(copy_tar_run_script_task)
copy_archive_run_script_task.set_upstream(demultiplex_task)
archive_run_folder_task.set_upstream(copy_archive_run_script_task)
