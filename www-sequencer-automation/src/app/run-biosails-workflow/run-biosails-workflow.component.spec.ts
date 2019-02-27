import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RunBiosailsWorkflowComponent } from './run-biosails-workflow.component';

describe('RunBiosailsWorkflowComponent', () => {
  let component: RunBiosailsWorkflowComponent;
  let fixture: ComponentFixture<RunBiosailsWorkflowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RunBiosailsWorkflowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RunBiosailsWorkflowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
