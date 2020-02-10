import argparse
import logging
import sys
from typing import Any
import os
import tempfile
import re

from ssh_helpers import execute_ssh_command, initialize_ssh

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


def validate_sample_names_from_scratch_dir(ssh_hook, csv_file):
    """
    :param ssh_hook: SSHHook from Airflow
    :param csv_file: Absolute path to csv SampleSheet
    :return:
    :valid_sample_names: List of sample names that passed validation
    :invalid_sample_names: List of sample names that did NOT pass validation step
    """
    ssh_client = ssh_hook.get_conn()
    sftp_client = ssh_client.open_sftp()
    tfile_local_sample_sheet = tempfile.NamedTemporaryFile(delete=False)
    # TODO sampledir will be passed in as a variable from the front end
    sftp_client.get(csv_file, tfile_local_sample_sheet.name)
    valid_sample_names, invalid_sample_names = validate_sample_names(filename=tfile_local_sample_sheet.name)
    os.remove(tfile_local_sample_sheet.name)
    return valid_sample_names, invalid_sample_names


def get_run_name_from_run_dir(run_dir: str) -> str:
    """param run_dir: str Run Directory on /scratch
    Given the run_dir /scratch/gencore/nextseq/181125_NB551229_0029_AHYGHVBGX5
    os.path.basename: 181125_NB551229_0029_AHYGHVBGX5
    split: ['181125', 'NB551229', '0029', 'AHYGHVBGX5']
    pop: AHYGHVBGX5
    replace('A', '', 1): HYGHVBGX5
    return HYGHVBGX5
    """
    return os.path.basename(run_dir).split('_').pop().replace('A', '', 1)


def ensure_run_dir_exists(sftp, run_dir: str) -> list:
    """TODO: This should just be a task in the dag"""
    try:
        run_dir_contents = sftp.listdir(run_dir)
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


def ensure_sample_sheet_exists_in_scratch_dir(sftp, csv_file: str) -> str:
    """:param run_dir_contents  - list of contents from the run directory
    If :
        there is a SampleSheet.csv just carry on
    Else:
        If there is more than 1 csv (besides the sample sheet) die
        If one, and only 1 csv file carry on with that csv file
    """
    logger.info('Begin: Checking for csv file')
    run_dir_contents = sftp.listdir(os.path.dirname(csv_file))
    if os.path.basename(csv_file) in run_dir_contents:
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


def ensure_valid_csv_file(sftp, scratch_dir, csv_file):
    """
    :param sftp sftpClient from paramiko
    :param scratch_dir : directory of run folder on /scratch
    :param csv_file : csv file
    Each CSV file should have a [Header] declaration
    and should have the sample name
    """
    logger.info('Begin: Ensuring CSV file {} is valid'.format(csv_file))

    tfile = tempfile.NamedTemporaryFile(delete=False)
    # Copy the sample sheet over locally and check it
    sftp.get(csv_file, tfile.name, callback=None)
    with open(tfile.name) as f:
        header_line = f.readline()

    sample = get_run_name_from_run_dir(scratch_dir)
    if sample in header_line:
        logger.info('{} in header'.format(sample))
        logger.info('[Header] in header')
        logger.info('Sample sheet looks valid')

    logger.info('End: Ensuring CSV file {} is valid'.format(csv_file))

    # Remove the local samplesheet once we're done
    os.remove(tfile.name)


def ensure_sample_sheet_exists_and_is_valid_csv(ds, **kwargs):
    scratch_dir = kwargs['dag_run'].conf['scratch_dir']
    sample_sheet = kwargs['dag_run'].conf['sample_sheet']
    logger.info('Begin: Sample sheet check for {}'.format(scratch_dir))
    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')

    logger.info('=============================================')
    logger.info('Beginning Sample Sheet Job')

    # This is already taken care of on the front end
    # But we should run a check to make sure,
    # incase of running directly through the REST API
    run_dir_contents = ensure_run_dir_exists(sftp, scratch_dir)
    csv_file = ensure_sample_sheet_exists_in_scratch_dir(sftp, sample_sheet)
    ensure_valid_csv_file(sftp, scratch_dir, csv_file)

    logger.info('Ending Sample Sheet Job')
    logger.info('=============================================')

