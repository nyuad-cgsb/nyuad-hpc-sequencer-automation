import { AirflowModule } from './airflow.module';

describe('AirflowModule', () => {
  let airflowModule: AirflowModule;

  beforeEach(() => {
    airflowModule = new AirflowModule();
  });

  it('should create an instance', () => {
    expect(airflowModule).toBeTruthy();
  });
});
