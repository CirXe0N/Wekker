import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {LoginRequest} from "./login.interface";

@Component({
  selector: 'login',
  templateUrl: './login.component.html'
})

export class LoginComponent implements OnInit {
  private form: FormGroup;
  private isRequesting: boolean = false;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    })
  }

  private doLoginRequest({value, valid}: {value: LoginRequest, valid: boolean}) {
    this.isRequesting = true;

    if(valid) {
      console.log(value);
    }
  }
}
