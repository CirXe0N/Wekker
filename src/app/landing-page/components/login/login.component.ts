import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {LoginRequest} from "./login.interface";
import {Router} from "@angular/router";

@Component({
  selector: 'login',
  templateUrl: './login.component.html'
})

export class LoginComponent implements OnInit {
  private form: FormGroup;
  private isRequesting: boolean = false;

  constructor(private router: Router) {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
      password: new FormControl('', Validators.required),
    })
  }

  private doLoginRequest({value, valid}: {value: LoginRequest, valid: boolean}) {
    if(valid) {
      this.isRequesting = true;
      console.log(value);
      this.router.navigateByUrl('/dashboard')
    }
  }
}
