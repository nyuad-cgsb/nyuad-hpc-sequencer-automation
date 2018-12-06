import {InjectionToken, ModuleWithProviders, NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {AirflowService} from './airflow.service';

// These need to be in separate files, or else there is a circular dependency issue
import {AirflowModuleConfigOptions} from './airflow.config';
import {AirflowServiceConfig} from './airflow.token';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: []
})
export class AirflowModule {
  static forRoot(config: AirflowModuleConfigOptions | null | undefined | {}): ModuleWithProviders {
    return {
      ngModule: AirflowModule,
      providers: [AirflowService, {
        provide: AirflowServiceConfig,
        useValue: config || {},
      }],
    };
  }
}
