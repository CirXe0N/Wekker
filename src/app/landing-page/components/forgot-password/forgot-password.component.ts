import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {ForgotPasswordRequest} from "./forgot-password.interface";

@Component({
  selector: 'forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.sass']
})

export class ForgotPasswordComponent implements OnInit {
  private form: FormGroup;
  private isSuccessfulRequest: boolean = false;
  private isRequesting: boolean = false;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')])
    })
  }

  private doForgotPasswordRequest({value, valid}: {value: ForgotPasswordRequest, valid: boolean}) {
    this.isRequesting = true;
    if(valid) {
      console.log(value);

      // Successful Request
      this.isSuccessfulRequest = true;
    }
  }
}
