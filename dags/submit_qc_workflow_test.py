import unittest
from jinja2 import Environment, BaseLoader

from test_helpers import DummyDAG

run_qc_workflow_task_command = """
        {{ echo "Work Dir: dag_run.conf["work_dir"]" if dag_run.conf["work_dir"] else "echo "No work dir specified"; exit 256" }}
        {{ echo "Scratch Dir: dag_run.conf["scratch_dir"]" if dag_run.conf["scratch_dir"] else "echo "No scratch dir specified"; exit 256" }}
        {{ echo "Running QC Workflow: dag_run.conf["qc_workflow"]" if dag_run.conf["qc_workflow"] else "echo "No qc workflow specified"; exit 0" }}
        cd {{ dag_run.conf["scratch_dir"] }}/Unaligned
"""

is_there_qc = """
#!/usr/bin/env bash

{% if dag_run.conf["scratch_dir"] %}
echo "Scratch Dir: {{ dag_run.conf["scratch_dir"] }}"
cd {{ dag_run.conf["scratch_dir"] }}/Unaligned
{% else %}
echo "There is no scratch dir specified. Exiting"
exit 256
{% endif %}

{% if dag_run.conf["qc_workflow"] %}
echo "Processing: {{ dag_run.conf["qc_workflow"] }}"
cp {{ dag_run.conf["qc_workflow"] }} ./ 
module load gencore gencore_dev
biox workflow -w {{ dag_run.conf["qc_workflow"] }} -o qc.sh
hpcrunner.pl submit_jobs --infile qc.sh --project {{dag_run.conf["jira_ticket"]}}-qc
{% else %}
echo "There is no QC Workflow specified. Exiting"
exit 0
{% endif %}
"""


class TestRunQCCommandIsCorrect(unittest.TestCase):
    def test(self):
        dag_run = DummyDAG()
        dag_run.conf = {'jira_ticket': 'NCB-464',
                        'qc_workflow': '/scratch/gencore/workflows/production/QC-QT-PE-nextseq.yml',
                        'scratch_dir': '/scratch/gencore/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST',
                        'work_dir': '/work/gencore/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST'}
        rtemplate = Environment(loader=BaseLoader).from_string(is_there_qc)
        data = rtemplate.render(dag_run=dag_run)
        print(data)

