import paramiko
import argparse
import logging
from .ssh_helpers import execute_ssh_command
import os
import sys

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tar run folder')
    parser.add_argument('--run-dir', type=str, required=True,
                        help='Working directory to run bcl2fastq')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('compute-15-1', username='gencore')

    dirname = os.path.dirname(args.run_dir)
    run_dir_base_dir = os.path.dirname(dirname)
    basename = os.path.basename(args.run_dir)

    tar_name = os.path.basename(args.run_dir)
    tar_name = tar_name + '.tar'

    work_abs_tar_path = os.path.dirname(args.run_dir) + tar_name

    command = """cd {} && tar -cvf {} {} && md5sum {} > {}.md5sum""".format(dirname, tar_name, args.run_dir, tar_name, basename)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
