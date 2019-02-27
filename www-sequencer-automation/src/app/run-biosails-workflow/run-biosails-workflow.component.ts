import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';

@Component({
  selector: 'app-run-biosails-workflow',
  templateUrl: './run-biosails-workflow.component.html',
  styleUrls: ['./run-biosails-workflow.component.css']
})
export class RunBiosailsWorkflowComponent implements OnInit {
  public biosailsWorkflows = new BiosailsWorkflowsModule();

  constructor() {
  }

  ngOnInit() {
  }

}
