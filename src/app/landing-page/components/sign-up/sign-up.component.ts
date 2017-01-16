import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {SignUpRequest} from "./sign-up.interface";

@Component({
  selector: 'sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.sass']
})

export class SignUpComponent implements OnInit {
  private form: FormGroup;
  private isRequesting: boolean = false;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
      password: new FormControl('', [Validators.required, Validators.minLength(5)]),
    });
  }

  private doSignUpRequest({value, valid}: {value: SignUpRequest, valid: boolean}) {
    this.isRequesting = true;

    if(valid) {
      console.log(value);
    }
  }
}
