import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appResults]'
})
export class ResultsDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
