import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RunBiosailsWorkflowRouteComponent } from './run-biosails-workflow-route.component';

describe('RunBiosailsWorkflowRouteComponent', () => {
  let component: RunBiosailsWorkflowRouteComponent;
  let fixture: ComponentFixture<RunBiosailsWorkflowRouteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RunBiosailsWorkflowRouteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RunBiosailsWorkflowRouteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
