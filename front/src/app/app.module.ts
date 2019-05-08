import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TesterComponent } from './tester/tester.component';
import { HttpClientModule } from "@angular/common/http";
import { ResultsDirective } from './results.directive';
import { ResultsComponent } from './results/results.component';
import { AddCodeComponent } from './add-code/add-code.component';

@NgModule({
  declarations: [
    AppComponent,
    TesterComponent,
    ResultsDirective,
    ResultsComponent,
    AddCodeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
