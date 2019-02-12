import argparse
import logging
import sys
from typing import Any
import os
import tempfile
import re

try:
    from .ssh_helpers import execute_ssh_command, initialize_ssh
except ImportError as e:
    from ssh_helpers import execute_ssh_command, initialize_ssh
except Exception as e:
    from ssh_helpers import execute_ssh_command, initialize_ssh

# create logger with 'spam_application'
logger = logging.getLogger('ensure_samplesheet_compute-15')
logger.setLevel(logging.DEBUG)


def check_sample_name(sample_name):
    """Check that the sample name only contains alphanumeric characters, underscores, and dashes
    Returns: true if sample name is valid
    false if sample name is invalid"""
    return bool(re.match('^[\w-]+$', sample_name))


def ensure_valid_sample_names(sample_file_contents):
    """:param: sample_file_contents : Array<str> from fh.readlines()
    :returns valid_sample_names: list of sample names that are valid and won't kill bcl2fastq
    :returns invalid_sample_names: list of sample names that do not pass validation step"""
    header_found = False
    sample_lines = []
    for line in sample_file_contents:
        if not header_found:
            if 'Sample_ID' in line:
                header_found = True
        else:
            sample_lines.append(line)
    invalid_sample_names = list(filter(lambda x: not check_sample_name, sample_lines))
    valid_sample_names = list(filter(lambda x: check_sample_name, sample_lines))
    return valid_sample_names, invalid_sample_names


def validate_sample_names(filename: str):
    """Sample names should ONLY contain alphanumeric characters, dashes, and underscores
    :param filename : filename on the LOCAL computer"""
    fh = open(filename, 'r')
    sample_file_contents = fh.readlines()
    sample_file_contents = list(map(lambda line: line.rstrip(), sample_file_contents))
    return ensure_valid_sample_names(sample_file_contents)


def validate_sample_names_from_work_dir(ssh_hook, work_dir):
    """

    :param ssh_hook: SSHHook from Airflow
    :param run_dir: Sequencing run_dir from dag_run conf context
    :return:
    :valid_sample_names: List of sample names that passed validation
    :invalid_sample_names: List of sample names that did NOT pass validation step
    """
    ssh_client = ssh_hook.get_conn()
    sftp_client = ssh_client.open_sftp()
    tfile_local_sample_sheet = tempfile.NamedTemporaryFile(delete=False)
    sftp_client.get(os.path.join(work_dir, 'SampleSheet.csv'), tfile_local_sample_sheet.name)
    valid_sample_names, invalid_sample_names = validate_sample_names(filename=tfile_local_sample_sheet.name)
    os.remove(tfile_local_sample_sheet.name)
    return valid_sample_names, invalid_sample_names


def get_run_name_from_run_dir(run_dir: str) -> str:
    """param run_dir: str Run Directory on /work
    Given the run_dir /work/gencore/nextseq/181125_NB551229_0029_AHYGHVBGX5
    os.path.basename: 181125_NB551229_0029_AHYGHVBGX5
    split: ['181125', 'NB551229', '0029', 'AHYGHVBGX5']
    pop: AHYGHVBGX5
    replace('A', '', 1): HYGHVBGX5
    return HYGHVBGX5
    """
    return os.path.basename(run_dir).split('_').pop().replace('A', '', 1)


def ensure_run_dir_exists(run_dir: str) -> list:
    """TODO: This should just be a task in the dag"""
    try:
        run_dir_contents = sftp.listdir(args.run_dir)
    except FileNotFoundError as e:
        print('Error occurred accessing run directory {}'.format(run_dir))
        print(e)
        raise FileNotFoundError
    except Exception as e:
        print('Unknown error occurred listing contents of run directory')
        print(e)
        raise Exception

    return run_dir_contents


def grep_for_csvs(csv_list: list, search_string: str) -> list:
    return [i for i, item in enumerate(csv_list) if re.search(search_string, item)]


def ensure_sample_sheet_exists(run_dir_contents: list) -> str:
    """:param run_dir_contents  - list of contents from the run directory
    If :
        there is a SampleSheet.csv just carry on
    Else:
        If there is more than 1 csv (besides the sample sheet) die
        If one, and only 1 csv file carry on with that csv file
    """
    logger.info('Begin: Checking for csv file')
    csv_file = ''
    if 'SampleSheet.csv' in run_dir_contents:
        csv_file = 'SampleSheet.csv'
        logger.info('SampleSheet Already present...')
    else:
        csv_indexes = grep_for_csvs(run_dir_contents, 'csv$')
        if not len(csv_indexes):
            logger.error('No CSVs were found! Aborting mission!')
            raise FileNotFoundError
        elif len(csv_indexes) > 1:
            logger.error('More than 1 csv was found! Aborting mission!')
            raise UserWarning
        elif len(csv_indexes) == 1:
            csv_file = run_dir_contents[csv_indexes[0]]
            logger.info('Found CSV: {}'.format(csv_file))

    logger.info('End: Checking for csv file')
    return csv_file


def ensure_valid_csv_file(sftp, run_dir, csv_file):
    """
    :param sftp sftpClient from paramiko
    :param run_dir : directory of run folder
    :param csv_file : csv file
    Each CSV file should have a [Header] declaration
    and should have the sample name
    """
    logger.info('Begin: Ensuring CSV file {} is valid'.format(csv_file))

    tfile = tempfile.NamedTemporaryFile(delete=False)
    sftp.get(os.path.join(run_dir, csv_file), tfile.name, callback=None)
    with open(tfile.name) as f:
        header_line = f.readline()

    sample = get_run_name_from_run_dir(run_dir)
    if sample in header_line:
        logger.info('{} in header'.format(sample))
        logger.info('[Header] in header')
        logger.info('Sample sheet looks valid')

    logger.info('End: Ensuring CSV file {} is valid'.format(csv_file))

    if 'SampleSheet.csv' not in csv_file:
        sftp.put(tfile.name, os.path.join(run_dir, 'SampleSheet.csv'))
        logger.info('Copied {} to SampleSheet.csv'.format(tfile.name))

    os.remove(tfile.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ensure SampleSheet.')
    parser.add_argument('--run-dir', type=str, required=True,
                        help='Run directory')

    args = parser.parse_args()
    args.run_dir = args.run_dir.strip()

    ssh, sftp = initialize_ssh('gencore', 'compute-15-1')

    logger.info('=============================================')
    logger.info('Beginning Sample Sheet Job')
    run_dir_contents = ensure_run_dir_exists(args.run_dir)
    csv_file = ensure_sample_sheet_exists(run_dir_contents)
    ensure_valid_csv_file(sftp, args.run_dir, csv_file)
    logger.info('Ending Sample Sheet Job')
    logger.info('=============================================')

    ssh.close()
