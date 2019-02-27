import { BiosailsWorkflowsModule } from './biosails-workflows.module';

describe('BiosailsWorkflowsModule', () => {
  let biosailsWorkflowsModule: BiosailsWorkflowsModule;

  beforeEach(() => {
    biosailsWorkflowsModule = new BiosailsWorkflowsModule();
  });

  it('should create an instance', () => {
    expect(biosailsWorkflowsModule).toBeTruthy();
  });
});
