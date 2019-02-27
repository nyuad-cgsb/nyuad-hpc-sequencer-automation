import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';

@Component({
  // selector: 'app-run-biosails-workflow-route',
  templateUrl: './run-biosails-workflow-route.component.html',
  styleUrls: ['./run-biosails-workflow-route.component.css']
})
export class RunBiosailsWorkflowRouteComponent implements OnInit {
  biosailsWorkflows = new BiosailsWorkflowsModule();

  constructor() {
  }

  ngOnInit() {
  }

}
