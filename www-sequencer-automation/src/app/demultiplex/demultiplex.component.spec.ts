import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {DemultiplexComponent} from './demultiplex.component';
import {FormsModule} from '@angular/forms';
import {UiSwitchModule} from 'ngx-ui-switch';
import {TypeaheadModule} from 'ngx-bootstrap';
import {HttpClient, HttpClientModule} from '@angular/common/http';

describe('DemultiplexComponent', () => {
  let component: DemultiplexComponent;
  let fixture: ComponentFixture<DemultiplexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DemultiplexComponent],
      imports: [FormsModule, UiSwitchModule.forRoot({}), TypeaheadModule.forRoot(),
        HttpClientModule,
      ],
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DemultiplexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should return url from results', () => {
    const results: { message } = {
      'message':
        ['Created <DagRun sequencer_automation @ 2018-12-02 06:31:51+00:00:',
          ' 2018-12-2-JIRA-ncb-333-WORK_DIR-180710_A00534_0022_AHFY3KDMXX,',
          ' externally triggered: True>'].join('')
    };
    const runId = '2018-12-2-JIRA-ncb-333-WORK_DIR-180710_A00534_0022_AHFY3KDMXX';
    const uri = ['http://localhost:8080/admin/airflow/graph?',
      'dag_id=sequencer_automation',
      '&run_id=2018-12-2-JIRA-ncb-333-WORK_DIR-180710_A00534_0022_AHFY3KDMXX',
      '&execution_date=2018-12-02+06%3A31%3A51%2B00%3A00'].join('');

    const timeSubmittedRegexp = new RegExp(`.*@ (.*): ${runId}`);
    const executionDate = timeSubmittedRegexp.exec(results.message)[1];
    const expectedUri = encodeURI(`http://localhost:8080/admin/airflow/graph?dag_id=sequencer_automation&run_id=${runId}&executionDate${executionDate}`);

    expect(executionDate).toEqual('2018-12-02 06:31:51+00:00');
  });
});
