import paramiko
import logging

from ssh_helpers import execute_ssh_command

logger = logging.getLogger('run_bcl2fastq_compute-15')
logger.setLevel(logging.DEBUG)


def run_demultiplex_task(ds, **kwargs):
    work_dir = kwargs['dag_run'].conf['work_dir']
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('dalma.abudhabi.nyu.edu', username='gencore')

    # TODO Make number of threads a variable
    command = 'ssh gencore@compute-15-1 cd {} && bcl2fastq -o Unaligned -p 28 --barcode-mismatches 1 -R {}'.format(work_dir, work_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        return
    else:
        raise Exception

