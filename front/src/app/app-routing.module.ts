import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddCodeComponent } from './add-code/add-code.component';
import { TesterComponent } from './tester/tester.component';

const routes: Routes = [
  { path: "add", component: AddCodeComponent},
  { path: "", component: TesterComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
