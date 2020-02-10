import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {AirflowService} from '../airflow/airflow.service';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: []
})
export class BiosailsWorkflowsModule {
  public selectedWorkflow: string = null;
  public selectedQCWorkflow: string = null;
  public availableWorkflows: string[] = [];
  public availableQCWorkflows: string[] = [];
  public errors: string[] = [];

  constructor(private airflowService: AirflowService) {
    this.getProdQcWorflows();
  }

  getProdQcWorflows() {
    this.airflowService
      .getQcWorkflows()
      .subscribe((results: { qc_workflows, context }) => {
        console.log(results);
        this.availableQCWorkflows = results.qc_workflows;
        this.availableQCWorkflows.unshift(null);
      }, (error) => {
        this.errors.push(error);
      });
  }

}
