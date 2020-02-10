import paramiko
import logging
from jinja2 import Environment, BaseLoader
import tempfile
import os
import time

from slurm_helpers import get_job_status, poll_slurm_job, parse_slurm_submission
from ssh_helpers import execute_ssh_command, initialize_ssh, execute_ssh_command_return_stdout_stderr

logger = logging.getLogger('submit_bcl2fastq')
logger.setLevel(logging.DEBUG)


def generate_demultiplex_slurm_job(dag_run):
    job_template = """#!/bin/bash
#SBATCH --output={{dag_run.conf["jira_ticket"]}}-demultiplex_%A.out
#SBATCH --error={{dag_run.conf["jira_ticket"]}}-demultiplex_%A.err
#SBATCH -J {{dag_run.conf["jira_ticket"]}}-demultiplex 
#SBATCH -p serial

#SBATCH --mem=118GB
#SBATCH --time=100:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --ntasks-per-node=1

cd {{dag_run.conf["demultiplex_current_work_dir"]}}
{{dag_run.conf["demultiplex_command"]}}
"""
    rtemplate = Environment(loader=BaseLoader).from_string(job_template)
    rendered_submit_demultiplex_command = rtemplate.render(dag_run=dag_run)
    return rendered_submit_demultiplex_command


def generate_submit_demultiplex_to_slurm_command(dag_run, script):
    job_template = """
cd {{dag_run.conf["demultiplex_current_work_dir"]}} && chmod 777 *sh && sbatch {{script}}
"""
    rtemplate = Environment(loader=BaseLoader).from_string(job_template)
    return rtemplate.render(dag_run=dag_run, script=script)


def submit_demultiplex_job_to_slurm(ssh, sftp, dag_run):
    try:
        slurm_script_str = generate_demultiplex_slurm_job(dag_run)
    except:
        raise ("Couldn't generate slurm job! Aborting mission!")

    with tempfile.NamedTemporaryFile('w+') as fp:
        print(slurm_script_str)
        try:
            fp.write(str(slurm_script_str))
        except:
            raise Exception("Unable to write slurm script to temp file!")
        fp.seek(0)
        script = os.path.join(dag_run.conf['demultiplex_current_work_dir'], 'demultiplex.sh')
        try:
            sftp.put(fp.name, script, callback=None)
        except:
            raise Exception("Unable to place temp script on dalma!")

    try:
        slurm_command = generate_submit_demultiplex_to_slurm_command(dag_run, script)
    except:
        raise Exception("Unable to generate slurm wrapper")
    output = execute_ssh_command_return_stdout_stderr(ssh,
                                                      slurm_command, logger)
    return output



def generate_demultiplex_command(dag_run):
    """
    Generate the demultiplex command
    This may or may not be a bad plan, presumably anyone could run anything
    :param kwargs:
    :return:
    """
    work_dir = dag_run.conf['work_dir']
    scratch_dir = dag_run.conf['scratch_dir']

    if 'demultiplex_command' in dag_run.conf:
        demultiplex_command = dag_run.conf['demultiplex_command']
        if 'rm ' in demultiplex_command:
            raise Exception('Unsafe command with rm found: {}'.format(demultiplex_command))
    else:
        demultiplex_command = 'mkdir -p {}/Unaligned && cd {} && bcl2fastq -o {}/Unaligned -p 28 --barcode-mismatches 1 -R {}'.format(
            scratch_dir, scratch_dir, scratch_dir, scratch_dir)
        dag_run.conf['demultiplex_command'] = demultiplex_command

    demultiplex_command = 'ssh gencore@compute-15-1 "{}"'.format(demultiplex_command)
    rtemplate = Environment(loader=BaseLoader).from_string(demultiplex_command)
    return rtemplate.render({'work_dir': work_dir})


def run_demultiplex_task(ds, **kwargs):
    """
    Run the command that demultiplexes the run dir
    :param ds:
    :param kwargs:
    :return:
    """
    ssh, sftp = initialize_ssh('gencore', 'dalma.abudhabi.nyu.edu')
    output = submit_demultiplex_job_to_slurm(ssh, sftp, kwargs['dag_run'])
    slurm_job_id = parse_slurm_submission(output)
    poll_slurm_job(ssh, slurm_job_id)

    ssh.close()
