import {BrowserModule} from '@angular/platform-browser';
import {RouterModule, Routes} from '@angular/router';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';

/**
 * Components
 */
import {AppComponent} from './app.component';
import {DemultiplexComponent} from './demultiplex/demultiplex.component';
import {DemultiplexRouteComponent} from './demultiplex-route/demultiplex-route.component';
import {RunBiosailsWorkflowComponent} from './run-biosails-workflow/run-biosails-workflow.component';
import {RunBiosailsWorkflowRouteComponent} from './run-biosails-workflow-route/run-biosails-workflow-route.component';

/**
 * UI Helpers
 */
import {TypeaheadModule} from 'ngx-bootstrap/typeahead';
import {UiSwitchModule} from 'ngx-ui-switch';
import {NotFoundComponent} from './pages/not-found/not-found.component';
import {AirflowService} from './airflow/airflow.service';
import {HttpClient, HttpClientModule, HttpHandler} from '@angular/common/http';

/**
 * Routes
 */
const appRoutes: Routes = [
  {path: 'run-biosails-workflow', component: RunBiosailsWorkflowRouteComponent},
  {path: 'demultiplex', component: DemultiplexRouteComponent},
  // {path: '404', component: NotFoundComponent},
  // {path: '**', redirectTo: '/404'}
];

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
    HttpClientModule,
    FormsModule,
    BrowserModule,
    UiSwitchModule.forRoot({}),
    RouterModule.forRoot(
      appRoutes,
      {enableTracing: true} // <-- debugging purposes only
    ),
    TypeaheadModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}