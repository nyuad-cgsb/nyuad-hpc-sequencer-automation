import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AirflowConfig} from '../../sdk/airflow/airflow-config';

@Injectable({
  providedIn: 'root'
})
// header('Access-Control-Allow-Origin: *');
// header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
// header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');
export class AirflowService {
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      // 'Access-Control-Allow-Origin': 'http://localhost:8080',
      // 'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
      // 'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
    })
  };

  constructor(private http: HttpClient) {
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
    return this.http.post('http://localhost:8080/api/experimental/dags/sequencer_automation/dag_runs', params, this.httpOptions);
  }

  getTask(task_id: string): Observable<any> {
    return this.http.get('http://localhost:8080/api/experimental/dags/sequencer_automation/tasks/archive_run_dir_task');
  }
}
