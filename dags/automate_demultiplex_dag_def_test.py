import unittest
import tempfile
from jinja2 import Environment, BaseLoader
from test_helpers import DummyDAG

from automate_demultiplex_dag_def import rsync_work_to_scratch_command


class TestRunQCCommandIsCorrect(unittest.TestCase):
    def test_gencore_workdir(self):
        dag_run = DummyDAG()
        dag_run.conf = {'jira_ticket': 'NCB-464',
                        'qc_workflow': '/scratch/gencore/workflows/production/QC-QT-PE-nextseq.yml',
                        'scratch_dir': '/scratch/gencore/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST',
                        'work_dir': '/work/gencore/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST'}
        rtemplate = Environment(loader=BaseLoader).from_string(rsync_work_to_scratch_command)
        data = rtemplate.render(dag_run=dag_run)
        print(data)

    def test_gencoreseq_workdir(self):
        dag_run = DummyDAG()
        dag_run.conf = {'jira_ticket': 'NCB-464',
                        'qc_workflow': '/scratch/gencore/workflows/production/QC-QT-PE-nextseq.yml',
                        'scratch_dir': '/scratch/gencore/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST',
                        'work_dir': '/work/gencoreseq/nextseq/181126_NB551229_0030_AHYFTFBGX5-AIRFLOW-TEST'}
        rtemplate = Environment(loader=BaseLoader).from_string(rsync_work_to_scratch_command)
        data = rtemplate.render(dag_run=dag_run)
        print(data)


if __name__ == '__main__':
    unittest.main()
