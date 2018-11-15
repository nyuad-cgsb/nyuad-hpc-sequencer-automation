import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DemultiplexComponent } from './demultiplex.component';

describe('DemultiplexComponent', () => {
  let component: DemultiplexComponent;
  let fixture: ComponentFixture<DemultiplexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DemultiplexComponent ]
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
});
