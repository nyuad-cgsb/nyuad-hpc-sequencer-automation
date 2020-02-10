import paramiko
import logging
import os
from ssh_helpers import execute_ssh_command

"""
This script tars the run-dir and runs an md5checksum

Example: 
    run_dir = '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
    archive_dir = '/archive/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
    run_dir_basedir = '/work/gencore/novaseq/'
    tar_name = '180710_A00534_0022_AHFY3KDMXX.tar.gz'
    work_tar_dir = '/work/gencore/novaseq/'
    archive_tar_dir = '/archive/gencore/novaseq'
    command = 
    cd /work/gencore/novaseq && 
        tar -cvf 180710_A00534_0022_AHFY3KDMXX.tar /work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX && \
        md5sum 180710_A00534_0022_AHFY3KDMXX.tar > 180710_A00534_0022_AHFY3KDMXX.md5sum'
"""

logger = logging.getLogger('run_create_tar_compute-15')
logger.setLevel(logging.DEBUG)


def generate_tar_command(work_dir):
    """
    Generate the command for tarring up the run folder
    IF the dir ends in '/', os.path.basename returns ''
    So remove a trailing '/'
    :param work_dir:
    :return:
    """
    work_dir = work_dir.rstrip('/')
    dirname = os.path.dirname(work_dir)
    basename = os.path.basename(work_dir)
    tar_name = os.path.basename(work_dir) + '.tar'

    command = """cd {} && tar -cvf {} {} && md5sum {} > {}.md5sum""".format(dirname, tar_name, work_dir, tar_name, basename)
    return command


def tar_work_run_folder(ds, **kwargs):
    work_dir = kwargs['dag_run'].conf['work_dir']
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('dalma.abudhabi.nyu.edu', username='gencore')

    command = generate_tar_command(work_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        return
    else:
        raise Exception


