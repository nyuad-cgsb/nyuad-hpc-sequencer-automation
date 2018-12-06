import paramiko
import argparse
import logging
import sys

try:
    from .ssh_helpers import execute_ssh_command
except:
    from ssh_helpers import execute_ssh_command

# create logger with 'spam_application'
logger = logging.getLogger('run_bcl2fastq_compute-15')
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run bcl2fastq.')
    parser.add_argument('--run-dir', type=str, required=True,
                        help='Working directory to run bcl2fastq')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('compute-15-1', username='gencore')

    # TODO Make number of threads a variable
    command = 'cd {} && bcl2fastq -o Unaligned -p 28 --barcode-mismatches 1 -R {}'.format(args.run_dir, args.run_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
