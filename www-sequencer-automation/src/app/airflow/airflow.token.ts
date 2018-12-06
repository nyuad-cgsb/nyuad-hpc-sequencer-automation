import {InjectionToken} from '@angular/core';
import {AirflowModuleConfigOptions} from './airflow.config';

export const AirflowServiceConfig = new InjectionToken<AirflowModuleConfigOptions>('AirflowModuleConfigOptions');
