import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {get, trimEnd, padStart} from 'lodash';
import {AirflowService} from '../airflow/airflow.service';
import {environment} from '../../environments/environment';

@Component({
  selector: 'app-demultiplex',
  templateUrl: './demultiplex.component.html',
  styleUrls: ['./demultiplex.component.css'],
  // providers: [AirflowSDK]
})
export class DemultiplexComponent implements OnInit {
  submitted = false;
  formResults = new DemultiplexComponentFormResult();
  error: string = null;
  response: any = null;
  runUrl: string = null;
  jiraTicket: JIRATicket = new JIRATicket();
  // Default is to use an existing ticket
  useExistingTicket: Boolean = true;

  constructor(private airflowService: AirflowService) {
  }

  ngOnInit() {
  }

  onSubmit() {
    this.submitted = true;
    this.response = null;
    this.error = null;

    if (!this.formResults.jiraTicket) {
      this.createJiraTicket();
    } else {
      this.triggerDag();
    }
  }

  triggerDag() {
    this.createRunId();
    this.airflowService.triggerDag('sequencer_automation', {
      conf: JSON.stringify({
        work_dir: trimEnd(this.formResults.workDir, '/'),
        scratch_dir: trimEnd(this.formResults.scratchDir, '/'),
        jira_ticket: this.formResults.jiraTicket,
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

  createJiraTicket() {
    this.airflowService.createJiraTicket(this.jiraTicket.summary, this.jiraTicket.description)
      .subscribe((results: { id, error, summary, description }) => {
        if (get(results, 'error')) {
          this.formResults.jiraTicketError = true;
        } else {
          console.log(JSON.stringify(results));
          this.formResults.jiraTicket = results.id;
          this.formResults.jiraTicketError = false;
          this.jiraTicket = new JIRATicket(this.formResults.jiraTicket, results.summary, results.description);
          this.triggerDag();
        }
      }, (error) => {
        console.log(error);
      });
  }

  checkRunId() {
    this.formResults.jiraTicketError = null;
    this.jiraTicket = new JIRATicket();
    this.airflowService.getJiraTicket(this.formResults.jiraTicket)
      .subscribe((results: { error, summary, description }) => {
        if (get(results, 'error')) {
          this.formResults.jiraTicketError = true;
        } else {
          this.formResults.jiraTicketError = false;
          this.jiraTicket = new JIRATicket(this.formResults.jiraTicket, results.summary, results.description);
        }
      }, (error) => {
        console.log(error);
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
      this.formResults.workDir = trimEnd(this.formResults.workDir, '/');
      runDir = this.formResults.workDir.split('/').pop();
      this.formResults.scratchDir = this.formResults.workDir.replace('/work', '/scratch');
    }
    this.formResults.runId = `${year}-${month}-${day}-${hour}:${minute}:${second}--JIRA-${this.formResults.jiraTicket}--WORK_DIR-${runDir}`;
  }

  getRunUrl() {
    const timeSubmittedRegexp = new RegExp(`.*@ (.*): ${this.formResults.runId}`);
    const executionDate = timeSubmittedRegexp.exec(this.response.message)[1];
    const url = [`${environment.airflowApiUrl}${environment.airflowPort}/admin/airflow/graph?`,
      `dag_id=sequencer_automation`,
      `&run_id=${this.formResults.runId}&executionDate${executionDate}`].join('');
    this.formResults.runUrl = encodeURI(url);
    this.formResults.jiraUrl = `https://cbi.abudhabi.nyu.edu/jira/browse/${this.formResults.jiraTicket}`;
  }

}

export class DemultiplexComponentFormResult {
  workDir: string = null;
  scratchDir: string = null;
  jiraTicket: string = null;
  jiraTicketError: Boolean = false;
  runId: string = null;
  runUrl: string = null;
  jiraUrl: string = null;
}

export class JIRATicket {
  description?: string = null;
  ticketId?: string = null;
  summary?: string = null;

  constructor(ticketId?, summary?, description?) {
    this.ticketId = ticketId;
    this.summary = summary;
    this.description = description;
  }
}

