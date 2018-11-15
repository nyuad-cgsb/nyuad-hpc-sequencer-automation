import paramiko
import argparse
from select import select
import logging
import sys

try:
    from .ssh_helpers import execute_ssh_command
except:
    from ssh_helpers import execute_ssh_command

# create logger with 'spam_application'
logger = logging.getLogger('run_bcl2fastq_compute-15')
logger.setLevel(logging.DEBUG)
# def execute(ssh_client, command, timeout=None):
#     try:
#         if not command:
#             raise Exception("no command specified so nothing to execute here.")
#
#         # Auto apply tty when its required in case of sudo
#         get_pty = False
#         if command.startswith('sudo'):
#             get_pty = True
#
#         # set timeout taken as params
#         logger.info('Executing command: {}'.format(command))
#
#         stdin, stdout, stderr = ssh_client.exec_command(command=command,
#                                                         get_pty=get_pty,
#                                                         timeout=timeout
#                                                         )
#         # get channels
#         channel = stdout.channel
#
#         # closing stdin
#         stdin.close()
#         channel.shutdown_write()
#
#         agg_stdout = b''
#         agg_stderr = b''
#
#         # capture any initial output in case channel is closed already
#         stdout_buffer_length = len(stdout.channel.in_buffer)
#
#         if stdout_buffer_length > 0:
#             agg_stdout += stdout.channel.recv(stdout_buffer_length)
#
#         # read from both stdout and stderr
#         while not channel.closed or \
#                 channel.recv_ready() or \
#                 channel.recv_stderr_ready():
#             readq, _, _ = select([channel], [], [], timeout)
#             for c in readq:
#                 if c.recv_ready():
#                     line = stdout.channel.recv(len(c.in_buffer))
#                     line = line
#                     agg_stdout += line
#                     logger.info(line.decode('utf-8').strip('\n'))
#                 if c.recv_stderr_ready():
#                     line = stderr.channel.recv_stderr(len(c.in_stderr_buffer))
#                     line = line
#                     agg_stderr += line
#                     logger.warning(line.decode('utf-8').strip('\n'))
#             if stdout.channel.exit_status_ready() \
#                     and not stderr.channel.recv_stderr_ready() \
#                     and not stdout.channel.recv_ready():
#                 stdout.channel.shutdown_read()
#                 stdout.channel.close()
#                 break
#
#         stdout.close()
#         stderr.close()
#
#         exit_status = stdout.channel.recv_exit_status()
#         if exit_status is 0:
#             # returning output if do_xcom_push is set
#             logger.info('Command exited with exitcode 0')
#
#         else:
#             error_msg = agg_stderr.decode('utf-8')
#             raise Exception("error running cmd: {0}, error: {1}".format(command, error_msg))
#
#     except Exception as e:
#         raise Exception("SSH operator error: {0}".format(str(e)))
#
#     return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run bcl2fastq.')
    parser.add_argument('--run-dir', type=str, required=True,
                        help='Working directory to run bcl2fastq')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('compute-15-1', username='gencore')

    command = 'cd {} && bcl2fastq -o Unaligned -p 28 --barcode-mismatches 1 -R {}'.format(args.run_dir, args.run_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
