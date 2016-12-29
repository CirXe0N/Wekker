import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {ForgotPasswordRequest} from "./forgot-password.interface";

@Component({
  selector: 'forgot-password',
  templateUrl: './forgot-password.component.html'
})

export class ForgotPasswordComponent implements OnInit {
  private form: FormGroup;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', Validators.required)
    })
  }

  private doForgotPasswordRequest({value, valid}: {value: ForgotPasswordRequest, valid: boolean}) {
    if(valid) {
      console.log(value);
    }
  }
}
