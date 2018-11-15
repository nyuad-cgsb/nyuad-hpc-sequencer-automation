import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DemultiplexRouteComponent } from './demultiplex-route.component';

describe('DemultiplexRouteComponent', () => {
  let component: DemultiplexRouteComponent;
  let fixture: ComponentFixture<DemultiplexRouteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DemultiplexRouteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DemultiplexRouteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
