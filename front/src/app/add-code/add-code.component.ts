import { Component, OnInit } from '@angular/core';
import { TestService } from '../test.service';

@Component({
  selector: 'app-add-code',
  templateUrl: './add-code.component.html',
  styleUrls: ['./add-code.component.css']
})
export class AddCodeComponent implements OnInit {


  constructor(
    private test_service: TestService
  ) { }

  ngOnInit() {
  }

  disableText(nodes) {
    nodes.forEach( elem => {
      elem.placeholder = "File has beens selected";
      elem.value = "";
      elem.disabled = true;
    })
  }

  submitCode(elem: any, input: Object) {
    
    if (typeof input["file"] !== "undefined" &&
        !/^.+.py$/.test(input["file"].name) &&
        !/^.*.zip$/.test(input["file"].name)
        ) {
      alert("The file you submitted is not a Python or zip file.");
      return;

    } else if (typeof input["file"] === "undefined" &&
              input["code"] === ""
      ) {
      alert("THere is no code being submitted.");
      return;

    } else {
      elem.textContent = "Processing...";
      elem.disabled = true;
      this.test_service.addCode(input).subscribe( data => {
        console.log(data);
        if (data !== undefined && data['success']) {
          alert("Code was added succesfully. Thank you!");
        } else {
          alert("There was an issue adding code to the database. Try again.");
        }

        elem.textContent = "Submit";
        elem.disabled = false;
      })
    }
  }
}
