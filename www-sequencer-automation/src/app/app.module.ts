import {BrowserModule} from '@angular/platform-browser';
import {RouterModule, Routes} from '@angular/router';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';

/**
 * Components
 */
import {AppComponent} from './app.component';
import {DemultiplexComponent} from './demultiplex/demultiplex.component';
import {DemultiplexRouteComponent} from './demultiplex-route/demultiplex-route.component';
import {RunBiosailsWorkflowComponent} from './run-biosails-workflow/run-biosails-workflow.component';
import {RunBiosailsWorkflowRouteComponent} from './run-biosails-workflow-route/run-biosails-workflow-route.component';

/**
 * Modules
 */
import {AirflowModule} from './airflow/airflow.module';
import {environment} from '../environments/environment';

/**
 * UI Helpers
 */
import {TypeaheadModule} from 'ngx-bootstrap/typeahead';
import {UiSwitchModule} from 'ngx-ui-switch';
import {NotFoundComponent} from './pages/not-found/not-found.component';


/**
 * Routes
 */
const appRoutes: Routes = [
  {path: 'run-biosails-workflow', component: RunBiosailsWorkflowRouteComponent},
  {path: 'demultiplex', component: DemultiplexRouteComponent},
  // {path: '404', component: NotFoundComponent},
  // {path: '**', redirectTo: '/404'}
];

// @ts-ignore
const airflowApiUrl = environment.airflowApiUrl;
console.log(`AirflowUrl: ${airflowApiUrl}`);
console.log(JSON.stringify(environment));

@NgModule({
  declarations: [
    AppComponent,
    DemultiplexComponent,
    DemultiplexRouteComponent,
    RunBiosailsWorkflowComponent,
    RunBiosailsWorkflowRouteComponent,
    NotFoundComponent
  ],
  imports: [
    FormsModule,
    HttpClientModule,
    BrowserModule,
    AirflowModule.forRoot({apiEndPoint: '/api/experimental', host: environment.airflowApiUrl, port: environment.airflowPort}),
    UiSwitchModule.forRoot({}),
    RouterModule.forRoot(
      appRoutes,
      // {enableTracing: true} // <-- debugging purposes only
    ),
    TypeaheadModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
