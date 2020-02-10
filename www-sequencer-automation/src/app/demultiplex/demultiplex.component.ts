import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {get, snakeCase, trimEnd, clone, padStart} from 'lodash';
import {AirflowService} from '../airflow/airflow.service';
import {environment} from '../../environments/environment';
import {NgxSpinnerService} from 'ngx-spinner';

@Component({
  selector: 'app-demultiplex',
  templateUrl: './demultiplex.component.html',
  styleUrls: ['./demultiplex.component.css'],
})
export class DemultiplexComponent implements OnInit {
  submitted = false;
  formResults = new DemultiplexComponentFormResult();
  error: string = null;
  response: any = null;
  runUrl: string = null;
  jiraTicket: JIRATicket = new JIRATicket();
  biosails: BiosailsWorkflowsModule;
  // Default is to use an existing ticket
  useExistingTicket: Boolean = true;

  constructor(private airflowService: AirflowService, private spinner: NgxSpinnerService) {
    this.biosails = new BiosailsWorkflowsModule(airflowService);
  }

  ngOnInit() {
  }

  isFormValid() {
    if (!this.formResults.workDir) {
      return false;
    } else if (!this.formResults.jiraTicket) {
      return false;
    } else {
      return true;
    }
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
    const conf = {};
    Object.keys(this.formResults).map((key) => {
      const newKey = snakeCase(key);
      conf[newKey] = this.formResults[key];
    });
    conf['qc_workflow'] = this.biosails.selectedQCWorkflow;
    console.log(conf);
    this.airflowService.triggerDag('sequencer_automation', {
      conf: JSON.stringify(conf),
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
    this.airflowService
      .createJiraTicket(this.jiraTicket.summary, this.jiraTicket.description)
      .subscribe((results: { id, error, summary, description }) => {
        if (get(results, 'error')) {
          this.formResults.jiraTicketError = true;
        } else {
          console.log(JSON.stringify(results));
          this.formResults.jiraTicket = results.id;
          this.formResults.jiraTicketError = false;
          this.jiraTicket = new JIRATicket(this.formResults.jiraTicket, results.summary, results.description);
          console.log(this.jiraTicket);
          this.isFormValid();
          this.createRunId();
        }
      }, (error) => {
        console.log(error);
      });
  }

  getJiraTicket() {
    this.formResults.jiraTicketError = null;
    this.jiraTicket = new JIRATicket();
    this.airflowService
      .getJiraTicket(this.formResults.jiraTicket)
      .subscribe((results: { error, summary, description, id }) => {
        if (get(results, 'error')) {
          this.formResults.jiraTicketError = true;
        } else {
          this.formResults.jiraTicketError = false;
          this.jiraTicket = new JIRATicket(results.id, results.summary, results.description);
          this.isFormValid();
          this.createRunId();
        }
      }, (error) => {
        console.log(error);
      });
  }

  checkDoesSampleFileExist() {
    this.spinner.show();
    this.airflowService
      .doesFileExist(this.formResults.sampleSheet)
      .subscribe((results: { results, context }) => {
        console.log('checkDoesFileExist: results');
        console.log(results);
        this.formResults.doesSampleSheetExist = get(results, ['file_exists']);
        this.spinner.hide();
      }, (error) => {
        console.log('checkDoesFileExist: error');
        console.log(error);
        this.spinner.hide();
      });
  }

  checkDoesDirExist() {
    this.formResults.workDir = trimEnd(this.formResults.workDir, '/');
    this.spinner.show();
    this.airflowService
      .doesDirExist(this.formResults.workDir)
      .subscribe((results: { results, context }) => {
        console.log('checkDoesDirExist: results');
        console.log(results);
        this.formResults.isWorkDirValid = results.results.dir_exists;
        this.spinner.hide();
        this.createRunId();
      }, (error) => {
        console.log('checkDoesDirExist: error');
        console.log(error);
        this.spinner.hide();
      });
  }

  createRunId() {
    // this.checkDoesDirExist();
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

    // And is workdir valid?
    if (this.formResults.workDir) {
      runDir = this.formResults.workDir.split('/').pop();
      this.generateDemultiPlexDirs();
    }
    if (this.formResults.projectName) {
      this.formResults.runId = [
        `${year}-${month}-${day}-${hour}:${minute}:${second}`,
        `--JIRA-${this.formResults.jiraTicket}`,
        `--PROJECT-${this.formResults.projectName}`,
        `---WORK_DIR-${runDir}`
      ].join('');
    } else {
      this.formResults.runId = [
        `${year}-${month}-${day}-${hour}:${minute}:${second}`,
        `--JIRA-${this.formResults.jiraTicket}`,
        `---WORK_DIR-${runDir}`
      ].join('');
    }
    this.isFormValid();
  }

  generateDemultiPlexDirs() {
    this.formResults.workDir = trimEnd(this.formResults.workDir, '/');
    // TODO This should someday be replaced with profiles
    this.formResults.scratchDir = clone(this.formResults.workDir);
    this.formResults.scratchDir = this.formResults.scratchDir.replace('/work', '/scratch');
    this.formResults.scratchDir = this.formResults.scratchDir.replace('gencoreseq', 'gencore');
    this.formResults.demultiplexCurrentWorkDir = clone(this.formResults.scratchDir);
    this.formResults.demultiplexRunDir = clone(this.formResults.scratchDir);
    this.formResults.sampleSheet = clone(this.formResults.demultiplexCurrentWorkDir) + '/SampleSheet.csv';
    this.generateDemultiPlexCommand('');
  }

  generateDemultiPlexCommand(join) {
    // Example
    // bcl2fastq -R ../190714_M01086_0061_000000000-C2D2W/ --sample-sheet SampleSheet.csv --barcode-mismatches 1 -p 12 -o Unaligned
    this.formResults.demultiplexCommand = [
      'cd ', this.formResults.demultiplexCurrentWorkDir,
      ' && ',
      ' bcl2fastq -R ', this.formResults.demultiplexRunDir,
      ' --sample-sheet ', this.formResults.sampleSheet,
      ' --barcode-mismatches ', '1 ',
      ' -p ', '24 ',
      ' -o ', 'Unaligned ',
    ].join(join);
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
  isWorkDirValid: Boolean = false;

  scratchDir: string = null;
  jiraTicket: string = null;
  jiraTicketError: Boolean = false;
  runId: string = null;
  runUrl: string = null;
  jiraUrl: string = null;

  // The current work dir is where we cd to before running the demultiplex
  demultiplexCurrentWorkDir: string = null;
  // Run dir is the -R
  demultiplexRunDir: string = null;
  // demultiplex command is autogenerated
  demultiplexCommand: string = null;

  // Optional project name
  projectName: string = null;

  // Sample sheet is the --sample-sheet
  sampleSheet: string = null;
  doesSampleSheetExist: Boolean = false;
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

