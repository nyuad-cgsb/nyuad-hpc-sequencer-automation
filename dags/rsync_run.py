import sys
import paramiko
from airflow import DAG
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.sftp_operator import SFTPOperator
import os

"""Sequence Automation Tasks

Description: This is a workflow that goes from demultiplexing runs on /work, rsyncing them to /scratch, 
    tars the raw run along with the demultiplexed fastqs, runs an md5sum check, and archives the whole lot of it 

copy_ssh_helpers_script_task
    operator: SFTPOperator
    description: Copies the ssh_helpers.py script to the run folder (so there is always a current record in case it changes) 
    dependencies: none 
    
Demultiplex Tasks

copy_demultiplex_script_task
    operator: SFTPOperator
    description: Copies the run_bcl2fastq.py script to the run folder (so there is always a current record in case it changes) 
    dependencies: copy_ssh_helpers_script_task 

demultiplex_task
    operator: SSHOperator
    description: Runs the previously copied run_bcl2fastq script (from the run folder) and runs it. This uses bcl2fastq to demultiplex the run
    dependencies: copy_demultiplex_script_task
    
rsync_work_task
    operator: SSHOperator
    description: Rsyncs the demultiplexed reads from $WORK to $SCRATCH
    dependencies: demultiplex_task
    
copy_tar_run_script_task
    operator: SFTP
    description: Copies the tar_run_folder.py script to the run folder
    dependencies: rsync_work_task
    
tar_run_folder_task
    operator: SSHOperator
    descriptions: Tars the run folder and runs an md5sum check
    dependencies: copy_tar_run_script_task

copy_archive_run_script_task
    operator: SFTPOperator
    description: Copies the archive_run_folder to the run dir
    dependencies: tar_run_folder_task

archive_run_folder_task
    operator: SSHOperator
    description: Archives the tarred run
    TODO: Figure out md5sum checks - I can run the md5sum, but then how to run it from archive?
    dependencies: copy_archive_run_script_task
"""

this_env = os.environ.copy()

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
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    local_filepath=os.path.join('/Users/jillian/Dropbox/projects/infrastructure/nyuad-hpc-sequencer-automation', 'ssh_helpers.py'),
    remote_filepath='{{params.sequence_run_work}}/ssh_helpers.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
)

copy_demultiplex_script_task = SFTPOperator(
    task_id='sftp_put_demultiplex_script',
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    local_filepath=os.path.join('/Users/jillian/Dropbox/projects/infrastructure/nyuad-hpc-sequencer-automation', 'run_bcl2fastq.py'),
    remote_filepath='{{params.sequence_run_work}}/run_bcl2fastq.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
)

demultiplex_command = """
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ params.sequence_run_work }}"
        python3 run_bcl2fastq.py --run-dir {{params.sequence_run_work}}
"""

demultiplex_task = SSHOperator(
    task_id='demultiplex',
    command=demultiplex_command,
    ssh_hook=ssh_hook,
    retries=1,
    do_xcom_push=True,
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    dag=dag)

rsync_work_command = """
        echo "{{ ds }}"
        mkdir -p {{params.sequence_run_scratch}}/Unaligned
        rsync -av "{{ params.sequence_run_work }}/Unaligned" "{{params.sequence_run_scratch}}"
"""
rsync_work_task = SSHOperator(
    task_id='rsync_work_scratch',
    ssh_hook=ssh_hook,
    command=rsync_work_command,
    retries=5,
    retry_delay=10,
    do_xcom_push=True,
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    dag=dag
)

copy_tar_run_script_task = SFTPOperator(
    task_id='sftp_put_tar_run_script',
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    local_filepath=os.path.join('/Users/jillian/Dropbox/projects/infrastructure/nyuad-hpc-sequencer-automation', 'tar_run_folder.py'),
    remote_filepath='{{params.sequence_run_work}}/tar_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
)

tar_run_folder_command = """
        echo "{{ ds }}"
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ params.sequence_run_work }}"
        python3 tar_run_folder.py --run-dir {{params.sequence_run_work}}
"""
tar_run_folder_task = SSHOperator(
    task_id='tar_run_folder_task',
    ssh_hook=ssh_hook,
    command=tar_run_folder_command,
    retries=5,
    retry_delay=10,
    do_xcom_push=True,
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    dag=dag
)

copy_archive_run_script_task = SFTPOperator(
    task_id='sftp_put_archive_run_script',
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    local_filepath=os.path.join('/Users/jillian/Dropbox/projects/infrastructure/nyuad-hpc-sequencer-automation', 'archive_run_folder.py'),
    remote_filepath='{{params.sequence_run_work}}/archive_run_folder.py',
    operation='put',
    ssh_hook=ssh_hook,
    dag=dag,
)

archive_run_folder_command = """
        echo "{{ ds }}"
        module load gencore gencore_anaconda/3-4.0.0
        export PATH=/scratch/gencore/bcl2fastq-v2.20.0.422/bin/:$PATH
        cd "{{ params.sequence_run_work }}"
        python3 archive_run_folder.py --run-dir {{params.sequence_run_work}}
"""
archive_run_folder_task = SSHOperator(
    task_id='archive_run_dir_task',
    ssh_hook=ssh_hook,
    command=archive_run_folder_command,
    retries=5,
    retry_delay=10,
    do_xcom_push=True,
    params={
        'sequence_run_work': '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'sequence_run_scratch': '/scratch/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX',
        'bcl2fastq': '/scratch/gencore/bcl2fastq-v2.20.0.422/bin/bcl2fastq',
    },
    dag=dag
)

copy_demultiplex_script_task.set_upstream(copy_ssh_helpers_script_task)
demultiplex_task.set_upstream(copy_demultiplex_script_task)
rsync_work_task.set_upstream(demultiplex_task)
copy_tar_run_script_task.set_upstream(rsync_work_task)
tar_run_folder_task.set_upstream(copy_tar_run_script_task)
copy_archive_run_script_task.set_upstream(tar_run_folder_task)
archive_run_folder_task.set_upstream(copy_archive_run_script_task)
