from jinja2 import Environment, BaseLoader
import paramiko
from ssh_helpers import execute_ssh_command_return_stdout_stderr
import logging
from config import AIRFLOW_ADMIN_URL
from nyuad_cgsb_jira_client.jira_client import jira_client
from biosails_helpers import poll_biosails_submissions

logger = logging.getLogger('submit_qc_workflow')
logger.setLevel(logging.DEBUG)

run_qc_workflow_command = """
#!/usr/bin/env bash

{% if dag_run.conf["scratch_dir"] %}
echo "Scratch Dir: {{ dag_run.conf["scratch_dir"] }}"
cd {{ dag_run.conf["scratch_dir"] }}/Unaligned
{% else %}
echo "There is no scratch dir specified. Exiting"
exit 256
{% endif %}

{% if dag_run.conf["qc_workflow"] %}
echo "Rendering: {{ dag_run.conf["qc_workflow"] }}"
cp {{ dag_run.conf["qc_workflow"] }} ./ 
module load gencore/1
module load gencore_biosails
biox run -w {{ dag_run.conf["qc_workflow"] }} -o qc.sh
hpcrunner.pl submit_jobs --infile qc.sh --project {{dag_run.conf["jira_ticket"]}}-qc
{% else %}
echo "There is no QC Workflow specified. Exiting"
exit 0
{% endif %}
"""


def submit_qc_workflow_to_slurm(ds, **kwargs):
    """ If there is a QC Workflow
    render it using biox, and submit it to slurm with hpcrunner
    Then poll the job to check when its done
    """

    if not kwargs['dag_run'].conf['qc_workflow']:
        return
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('dalma.abudhabi.nyu.edu', username='gencore')
        rtemplate = Environment(loader=BaseLoader).from_string(run_qc_workflow_command)
        rendered_run_qc_workflow_command = rtemplate.render(dag_run=kwargs['dag_run'])
        agg_output = False
        error = False
        try:
            agg_output = execute_ssh_command_return_stdout_stderr(ssh, rendered_run_qc_workflow_command, logger)
        except Exception as e:
            error = e

        if agg_output:
            update_jira_ticket_success_slurm_submission_info(kwargs, agg_output)
            poll_biosails_submissions(ssh, agg_output)
        else:
            update_jira_ticket_success_slurm_submission_info(kwargs, [str(error)])
            raise Exception('No output from biosails submission found!')


def update_jira_ticket_success_slurm_submission_info(context, output):
    """
    If successful, update the JIRA ticket with the slurm submission info
    :return:
    """
    run_id = context['run_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    work_dir = context['dag_run'].conf['work_dir']
    comment = '{}*QC Workflow Submitted successfully*{}: {} [View Logs | {}&run_id={} ]' \
        .format('{color:green}', '{color}', context['task'], AIRFLOW_ADMIN_URL, run_id)
    comment += "{code}"
    comment += "\n".join(output)
    comment += "{code}"
    comment += '*View Progress*: [View Progress | {}&run_id={} ] on {}'.format(AIRFLOW_ADMIN_URL, run_id, work_dir)
    jira_client.add_comment(jira_ticket, comment)
    return


def update_jira_ticket_failure_slurm_submission_info(context, output):
    """
    If successful, update the JIRA ticket with the slurm submission info
    :return:
    """
    run_id = context['run_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    work_dir = context['dag_run'].conf['work_dir']
    comment = '{}*QC Workflow Submission Task Failed*{}: {} [View Logs | {}&run_id={} ]' \
        .format('{color:red}', '{color}', context['task'], AIRFLOW_ADMIN_URL, run_id)
    comment += "{code}"
    comment += "\n".join(output)
    comment += "{code}"
    comment += '*View Full Log*: [View Progress | {}&run_id={} ] on {}'.format(AIRFLOW_ADMIN_URL, run_id, work_dir)
    jira_client.add_comment(jira_ticket, comment)
    return
