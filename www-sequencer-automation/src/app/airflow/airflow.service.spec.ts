import { TestBed } from '@angular/core/testing';

import { AirflowService } from './airflow.service';

describe('AirflowService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: AirflowService = TestBed.get(AirflowService);
    expect(service).toBeTruthy();
  });
});
