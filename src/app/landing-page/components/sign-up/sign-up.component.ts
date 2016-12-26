import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {SignUpRequest} from "./sign-up.interface";

@Component({
  selector: 'sign-up',
  templateUrl: './sign-up.component.html'
})

export class SignUpComponent implements OnInit {
  private form: FormGroup;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      email_address: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    })
  }

  private doSignUpRequest({value, valid}: {value: SignUpRequest, valid: boolean}) {
    if(valid) {
      console.log(value);
    }
  }
}
