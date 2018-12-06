import paramiko
import argparse
import logging
import os
import sys
try:
    from .ssh_helpers import execute_ssh_command
except:
    from ssh_helpers import execute_ssh_command

"""
This script sshs from dalma.abudhabi.nyu.edu (login) to archive3, and runs the rsync command
:param run_dir :str 

Example:
    run_dir = '/work/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
    archive_dir = '/archive/gencore/novaseq/180710_A00534_0022_AHFY3KDMXX'
    run_dir_basedir = '/work/gencore/novaseq/'
    tar_name = '180710_A00534_0022_AHFY3KDMXX.tar.gz'
    work_tar_dir = '/work/gencore/novaseq/'
    archive_tar_dir = '/archive/gencore/novaseq'
    command: 
        cd /work/gencore/novaseq && \
        rsync -av 180710_A00534_0022_AHFY3KDMXX.tar /archive/gencore/novaseq/raw/
"""

logger = logging.getLogger('archive_tar_archive-3')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tar run folder')
    parser.add_argument('--run-dir', type=str, required=True,
                        help='Working directory to run bcl2fastq')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('archive3', username='gencore')

    dirname = os.path.dirname(args.run_dir)
    run_dir_base_dir = os.path.dirname(dirname)
    basename = os.path.basename(args.run_dir)

    archive_dir = args.run_dir.replace('work', 'archive')
    archive_dir = os.path.dirname(archive_dir)
    archive_dir = os.path.join(archive_dir, 'raw')

    tar_name = os.path.basename(args.run_dir)
    tar_name = tar_name + '.tar'

    ## Archive3 is a restricted machine
    command = 'rsync -av --checksum {}/{} {}/'.format(dirname, tar_name, archive_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
