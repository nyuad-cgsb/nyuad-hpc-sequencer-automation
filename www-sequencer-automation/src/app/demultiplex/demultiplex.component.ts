import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {padStart} from 'lodash';
import {AirflowService} from '../airflow/airflow.service';

@Component({
  selector: 'app-demultiplex',
  templateUrl: './demultiplex.component.html',
  styleUrls: ['./demultiplex.component.css'],
  // providers: [AirflowSDK]
})
export class DemultiplexComponent implements OnInit {
  submitted = false;
  formResults = new DemultiplexComponentFormResult();
  biosailsWorkflows = new BiosailsWorkflowsModule();
  error: string = null;
  response: any = null;
  runUrl: string = null;

  constructor(private airflowService: AirflowService) {
  }

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
        this.getRunUrl();
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
    let hour = d.getHours();
    hour = padStart(hour, 2, '0');
    let minute = d.getMinutes();
    minute = padStart(minute, 2, '0');
    let second = d.getSeconds();
    second = padStart(second, 2, '0');

    if (this.formResults.workDir) {
      runDir = this.formResults.workDir.split('/').pop();
      this.formResults.scratchDir = this.formResults.workDir.replace('/work', '/scratch');
    }
    this.formResults.runId = `${year}-${month}-${day}-${hour}:${minute}:${second}--JIRA-${this.formResults.jiraTicket}--WORK_DIR-${runDir}`;
  }

  getRunUrl() {
    const timeSubmittedRegexp = new RegExp(`.*@ (.*): ${this.formResults.runId}`);
    const executionDate = timeSubmittedRegexp.exec(this.response.message)[1];
    const url = `http://localhost:8080/admin/airflow/graph?dag_id=sequencer_automation&run_id=${this.formResults.runId}&executionDate${executionDate}`;
    this.formResults.runUrl = encodeURI(url);
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
  runUrl: string = null;
}
