import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';

@Component({
  selector: 'app-demultiplex',
  templateUrl: './demultiplex.component.html',
  styleUrls: ['./demultiplex.component.css']
})
export class DemultiplexComponent implements OnInit {
  submitted = false;
  formResults = new DemultiplexComponentFormResult();
  biosailsWorkflows = new BiosailsWorkflowsModule();

  constructor() {
  }

  ngOnInit() {
  }

  onSubmit() {
    this.submitted = true;
  }

  checkWorkDir() {
    console.log('in check workdir');
  }

  createRunId() {
    let runDir = '';
    const d = new Date();
    const month = '' + (d.getMonth() + 1);
    const day = '' + d.getDate();
    const year = d.getFullYear();
    if (this.formResults.workDir) {
      runDir = this.formResults.workDir.split('/').pop();
    }
    this.formResults.runId = `${year}-${month}-${day} ${this.formResults.jiraTicket} ${runDir}`;
  }

}

export class DemultiplexComponentFormResult {
  workDir: string = null;
  jiraTicket: string = null;
  runQcWorkflow: Boolean;
  runWorkflow: Boolean;
  qcWorkflow: string = null;
  workflow: string = null;
  runId: string = null;
}
