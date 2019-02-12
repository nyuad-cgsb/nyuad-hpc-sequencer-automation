import {Inject, Injectable, ModuleWithProviders, Optional} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AirflowServiceConfig} from './airflow.token';
import {AirflowModuleConfigOptions, AirflowModuleConfigOptionsDefaults} from './airflow.config';

@Injectable({
  providedIn: 'root'
})

export class AirflowService {
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    })
  };

  public config: AirflowModuleConfigOptions;

  constructor(@Inject(AirflowServiceConfig) @Optional() config: AirflowModuleConfigOptions,
              private http: HttpClient) {
    this.config = new AirflowModuleConfigOptionsDefaults(config);
    console.log(`CONFIG: ${JSON.stringify(config)}`);
    console.log(`CONFIG: ${JSON.stringify(this.config)}`);
  }

  /**
   *
   * @param dag_id Airflow dag_id
   * @param params airflow configuration parameters
   * Example Triggering a dag running at localhost:8080 with dag_id `sequencer_automation`:
   * curl -X POST \
   http://localhost:8080/api/experimental/dags/sequencer_automation/dag_runs \
   -H 'Cache-Control: no-cache' \
   -H 'Content-Type: application/json' \
   -d '{"conf":"{\"hello\":\"world\"}"}'
   */
  triggerDag(dag_id: string, params: { conf, run_id }): Observable<any> {
    return this.http.post(`${this.config.host}${this.config.port}${this.config.apiEndPoint}/dags/${dag_id}/dag_runs`,
      params, this.httpOptions);
  }

  getTask(dag_id: string, task_id: string): Observable<any> {
    return this.http.post(`${this.config.host}${this.config.port}${this.config.apiEndPoint}/dags/${dag_id}/tasks/${task_id}`,
      {}, this.httpOptions);
  }

  createJiraTicket(summary: string, description: string): Observable<any> {
    return this.http.post(`${this.config.host}${this.config.port}/jira/create_jira_ticket`,
      {summary: summary, description: description}, this.httpOptions);
  }

  getJiraTicket(ticket_id: string): Observable<any> {
    return this.http.post(`${this.config.host}${this.config.port}/jira/get_jira_ticket`,
      {ticketId: ticket_id}, this.httpOptions);
  }

}
