import json
import os
from slurm_helpers import poll_slurm_job

"""
When submitting with hpcrunner we get a job output that looks like this:

[2019/07/21 23:15:02] Job Summary 
[2019/07/21 23:15:02] 
.---------------------------------------------------------------------.
| Job Name                | Scheduler ID | Task Indices | Total Tasks |
+-------------------------+--------------+--------------+-------------+
| concat_reads            |      1316487 | 1-18         |          18 |
| raw_fastqc              |      1316498 | 19-36        |          18 |
| trimmomatic             |      1316499 | 37-45        |           9 |
| trimmomatic_fastqc      |      1316500 | 46-63        |          18 |
| trimmomatic_gzip        |      1316501 | 64-99        |          36 |
| multiqc                 |      1316502 | 100-100      |           1 |
| remove_trimmomatic_logs |      1316503 | 101-109      |           9 |
'-------------------------+--------------+--------------+-------------'
 
[2019/07/21 23:15:02] Your jobs have been submitted. 
[2019/07/21 23:15:02] Experimental! For status updates please run: 
[2019/07/21 23:15:02] hpcrunner.pl stats 
[2019/07/21 23:15:02] To get status updates for only this submission please run: 
[2019/07/21 23:15:02] hpcrunner.pl stats --data_dir /scratch/gencore/miseq/190714_M01086_0061_000000000-C2D2W/Unaligned/hpc-runner/2019-07-21T23-14-26/ncs-233-qc/logs/000_hpcrunner_logs/stats 

In the stats dir is a submission.json file, which has all the submission data
We want to read in this file, and return the slurm job ids
"""


def check_for_hpcrunner_stats(line):
    if 'hpcrunner.pl stats --data_dir' in line:
        return True
    else:
        return False


def get_hpcrunner_data_dir(output):
    output = ''.join(output)
    output = output.split("\n")
    data_dir_line = list(filter(lambda x: check_for_hpcrunner_stats(x), output))
    stats_line = data_dir_line.pop()
    # Directory is the last part of the line
    stats_dir = stats_line.split().pop()
    return stats_dir


def get_submission_ids(output):
    """
    Read in the submission.json and get a list of job_ids
    :param output:
    :return:
    """
    stats_dir = get_hpcrunner_data_dir(output)
    f = open(os.path.join(stats_dir, 'submission.json'))
    data = json.loads(f.read())
    submission_data = []
    for job in data['jobs']:
        job_name = job['job']
        submission_ids = list(map(lambda x: x['scheduler_id'], job['schedule']))
        for submission_id in submission_ids:
            job_data = {}
            job_data['job_name'] = job_name
            job_data['submission_id'] = submission_id
            submission_data.append(job_data)

    return submission_data


def poll_biosails_submissions(ssh, output):
    """
    Poll the biosails job submissions
    :param ssh:
    :param output:
    :return:
    """
    # TODO Set this up in a queue, so it can run in the background every hour or so
    # And update the JIRA ticket
    submission_data = get_submission_ids(output)
    for data in submission_data:
        submission_id = data['submission_id']
        job_status = poll_slurm_job(ssh, submission_id)
        data['job_status'] = job_status

    return submission_data