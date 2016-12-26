import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {LoginRequest} from "./login.interface";

@Component({
  selector: 'login',
  templateUrl: './login.component.html'
})

export class LoginComponent implements OnInit {
  private form: FormGroup;

  constructor() {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    })
  }

  private doLoginRequest({value, valid}: {value: LoginRequest, valid: boolean}) {
    if(valid) {
      console.log(value);
    }
  }
}
