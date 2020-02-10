import paramiko
import argparse
import logging
import os
import sys
from ssh_helpers import execute_ssh_command

"""
This script sshs from dalma.abudhabi.nyu.edu (login) to archive3, and runs the rsync command
Previously this script ran after tarring, but this has been deprecated
:param run_dir :str 

Example:
    run_dir = '/scratch/gencoreseq/novaseq/180710_A00534_0022_AHFY3KDMXX'
    archive_dir = '/archive/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
    run_dir_basedir = '/scratch/gencore/novaseq/'
    scratch_tar_dir = '/scratch/gencoreseq/novaseq/'
    archive_tar_dir = '/archive/gencore/novaseq'
    command: 
        cd /scratch/gencore/novaseq && \
        rsync -av 180710_A00534_0022_AHFY3KDMXX /archive/gencore/novaseq/raw/
"""

logger = logging.getLogger('archive_tar_archive-3')
logger.setLevel(logging.DEBUG)


def generate_archive_scratch_dir_command(scratch_dir):
    dirname = os.path.dirname(scratch_dir)

    archive_dir = scratch_dir.replace('scratch', 'archive')
    archive_dir = os.path.dirname(archive_dir)
    archive_dir = os.path.join(archive_dir, 'raw')

    # tar_name = os.path.basename(scratch_dir) + '.tar'
    tar_name = os.path.basename(scratch_dir)

    # TODO Really should have profiles that say where to ssh to
    return 'ssh gencore@archive3 "rsync -av --checksum {}/{} {}/"'.format(dirname, tar_name, archive_dir)


def archive_scratch_dir_folder(ds, **kwargs):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('archive3', username='gencore')
    ssh.connect('dalma.abudhabi.nyu.edu', username='gencore')

    scratch_dir = kwargs['dag_run'].conf['scratch_dir']
    scratch_dir = scratch_dir.rstrip('/')

    command = generate_archive_scratch_dir_command(scratch_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        return
    else:
        raise Exception


# If running through the SSHOperator run like this
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tar run folder')
    parser.add_argument('--scratch-dir', type=str, required=True,
                        help='Directory on /scratch to archive')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()

    # Archive3 is a restricted machine
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('archive3', username='gencore')

    command = generate_archive_scratch_dir_command(args.scratch_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
