import {Component, OnInit} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {AirflowService} from '../airflow/airflow.service';

@Component({
  // selector: 'app-run-biosails-workflow-route',
  templateUrl: './run-biosails-workflow-route.component.html',
  styleUrls: ['./run-biosails-workflow-route.component.css']
})
export class RunBiosailsWorkflowRouteComponent implements OnInit {
  biosailsWorkflows: BiosailsWorkflowsModule;

  constructor(private airflowService: AirflowService) {
    this.biosailsWorkflows = new BiosailsWorkflowsModule(airflowService);
  }

  ngOnInit() {
  }

}
