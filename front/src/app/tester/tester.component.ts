import { Component, OnInit, SystemJsNgModuleLoader, ViewChildren, QueryList } from '@angular/core';
import { TestService } from '../test.service';
;


@Component({
  selector: 'app-tester',
  templateUrl: './tester.component.html',
  styleUrls: ['./tester.component.css']
})
export class TesterComponent implements OnInit {

  results: Array<Object> = [];
  keywordResults: Array<Object> = [];
  sort: String = "relevancy";

  constructor(
    private test_service: TestService
  ) { }

  ngOnInit() {
  }

  switchSort(value) {
    this.sort = value;
    console.log(this.keywordResults);
  }

  quicksort(array: Array<Object>, left: any, right: any) {
    if (left < right) {
      let pivotIndex = this.partition(array, left, right);

      this.quicksort(array, left, pivotIndex - 1);
      this.quicksort(array, pivotIndex + 1, right);
    }
    
  }

  partition(array: Array<Object>, left: any, right: any) {
    let i = left - 1;
    let pivot = array[right];
    for (let j = left; j < right - 1; j++) {
      if (array[j]["value"] >= pivot["value"]) {
        i++;
        let temp = array[i];
        array[i] = array[j];
        array[j] = temp;
      }
    }
    let temp = array[i + 1];
    array[i + 1] = array[right];
    array[right] = temp;
    
    return (i + 1);
    
  }

  private getSearch(search: string) {
    if (search === "") {
      return;
    }

    let words: Array<String> = search.split(" ");
    
    this.test_service.getTests(search).subscribe( data => {
      
      if (this.results.length > 0) {
        this.results.length = 0;
      }

      if (this.keywordResults.length > 0) {
        this.keywordResults.length = 0;
      }
      
      for (let prop in data) {
        if (data.hasOwnProperty(prop)) {
          this.results.push(data[prop]);
          let matched = 0;

          words.forEach(elem => {
            if (data[prop].keywords.includes(elem)) {
              matched++;
            }
          });
          
          this.keywordResults.push({
            value: matched,
            res: data[prop]
          })
        }
      }

      this.quicksort(this.keywordResults, 0, this.keywordResults.length - 1);

    })
  }

  getResults(search: string) {
    this.getSearch(search);
  }
}
