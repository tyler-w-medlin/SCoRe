import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Responser } from './responser';
import { Observable, of } from "rxjs";
import { catchError } from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})

export class TestService {

  private url: string = "http://localhost:5000/";
  constructor(
    private http: HttpClient
  ) { }

  getTests(search: string) {
    const url: string = this.url + "search";
    return this.http.post<Responser>(url, {"search" : search}).pipe(
      catchError(this.handleError<Responser>("getTests"))
    );
  }

  addCode(input: Object) {
    const url: string = this.url + "addCode";

    if (typeof input['file'] !== "undefined") {
      return this.http.post<Responser>(url, input['file']).pipe(
        catchError(this.handleSearchError<Responser>("addCode"))
      );
    } else {
      return this.http.post<Responser>(url, input).pipe(
        catchError(this.handleSearchError<Responser>("addCode"))
      );
    }
  }

  private handleSearchError<T> (operation = "operation", result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      return of(result as T);
    }
  }

  private handleError<T>(operation = "operation", result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      alert("Something went wrong when sending the data.");
      return of(result as T);
    }
  }
}
