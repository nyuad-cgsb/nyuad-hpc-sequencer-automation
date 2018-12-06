from airflow import DAG
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.sftp_operator import SFTPOperator
import os

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
)

copy_ensure_samplesheet_task = SFTPOperator(
    task_id='sftp_put_ensure_samplesheet_script',
    local_filepath=os.path.join(this_dir,
                                'ensure_samplesheet.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/ensure_samplesheet.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
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
    dag=dag)

copy_demultiplex_script_task = SFTPOperator(
    task_id='sftp_put_demultiplex_script',
    local_filepath=os.path.join(this_dir,
                                'run_bcl2fastq.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/run_bcl2fastq.py',
    operation='put',
    ssh_hook=ssh_hook,
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
    # cpus=28,
    do_xcom_push=True,
    dag=dag)

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
    dag=dag
)

copy_tar_run_script_task = SFTPOperator(
    task_id='sftp_put_tar_run_script',
    local_filepath=os.path.join(this_dir,
                                'tar_run_folder.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/tar_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
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
    dag=dag
)

copy_archive_run_script_task = SFTPOperator(
    task_id='sftp_put_archive_run_script',
    local_filepath=os.path.join(this_dir,
                                'archive_run_folder.py'),
    remote_filepath='{{ dag_run.conf["work_dir"] }}/archive_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
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
    dag=dag
)

copy_ensure_samplesheet_task.set_upstream(copy_ssh_helpers_script_task)
ensure_samplesheet_task.set_upstream(copy_ensure_samplesheet_task)
copy_demultiplex_script_task.set_upstream(ensure_samplesheet_task)
demultiplex_task.set_upstream(copy_demultiplex_script_task)
rsync_work_task.set_upstream(demultiplex_task)
copy_tar_run_script_task.set_upstream(rsync_work_task)
tar_run_folder_task.set_upstream(copy_tar_run_script_task)
copy_archive_run_script_task.set_upstream(demultiplex_task)
archive_run_folder_task.set_upstream(copy_archive_run_script_task)
