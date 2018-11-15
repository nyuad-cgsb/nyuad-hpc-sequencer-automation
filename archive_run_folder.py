import paramiko
import argparse
import logging
from .ssh_helpers import execute_ssh_command
import os
import sys

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

    tar_name = os.path.basename(args.run_dir)
    tar_name = tar_name + '.tar.gz'

    command = 'cd {} && rsync -av {}.tar.gz {}'.format(dirname, basename, archive_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
