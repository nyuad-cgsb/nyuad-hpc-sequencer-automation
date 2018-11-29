import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {AirflowService} from '../airflow/airflow.service';

@Component({
  selector: 'app-demultiplex',
  templateUrl: './demultiplex.component.html',
  styleUrls: ['./demultiplex.component.css'],
  providers: [AirflowService]
})
export class DemultiplexComponent implements OnInit {
  submitted = false;
  formResults = new DemultiplexComponentFormResult();
  biosailsWorkflows = new BiosailsWorkflowsModule();
  error: string = null;
  response: any = null;

  constructor(private airflowService: AirflowService) {
  }

  // constructor() {
  // }

  ngOnInit() {
  }

  onSubmit() {
    this.submitted = true;
    this.response = null;
    this.error = null;

    this.createRunId();
    this.airflowService.triggerDag('sequencer_automation', {
      conf: JSON.stringify({
        work_dir: this.formResults.workDir,
        scratch_dir: this.formResults.scratchDir,
      }),
      run_id: this.formResults.runId,
    })
      .subscribe((results) => {
        this.response = results;
      }, (error) => {
        this.error = error;
      });
  }

  createRunId() {
    let runDir = '';
    const d = new Date();
    const month = '' + (d.getMonth() + 1);
    const day = '' + d.getDate();
    const year = d.getFullYear();
    if (this.formResults.workDir) {
      runDir = this.formResults.workDir.split('/').pop();
      this.formResults.scratchDir = this.formResults.workDir.replace('/work', '/scratch');
    }
    this.formResults.runId = `${year}-${month}-${day}-JIRA-${this.formResults.jiraTicket}-WORK_DIR-${runDir}`;

  }

}

export class DemultiplexComponentFormResult {
  workDir: string = null;
  scratchDir: string = null;
  jiraTicket: string = null;
  runQcWorkflow: Boolean;
  runWorkflow: Boolean;
  qcWorkflow: string = null;
  workflow: string = null;
  runId: string = null;
}
