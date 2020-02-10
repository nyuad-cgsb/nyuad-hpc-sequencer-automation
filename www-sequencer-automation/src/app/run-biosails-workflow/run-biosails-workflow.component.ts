import {Component, OnInit, Input} from '@angular/core';
import {BiosailsWorkflowsModule} from '../biosails-workflows/biosails-workflows.module';
import {AirflowService} from '../airflow/airflow.service';

@Component({
  selector: 'app-run-biosails-workflow',
  templateUrl: './run-biosails-workflow.component.html',
  styleUrls: ['./run-biosails-workflow.component.css']
})
export class RunBiosailsWorkflowComponent implements OnInit {
  @Input() biosailsWorkflows: BiosailsWorkflowsModule;

  constructor(private airflowService: AirflowService) {
    // this.biosailsWorkflows = new BiosailsWorkflowsModule(airflowService);
  }

  ngOnInit() {
  }

}
