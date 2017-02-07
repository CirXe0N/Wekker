import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {LoginRequest} from "./login.interface";
import {Router} from "@angular/router";
import {WekkerAPIService} from "../../../../services/wekker-api/wekker-api.service";
import {UtilitiesService} from "../../../../services/utilities/utilities.service";

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})

export class LoginComponent implements OnInit {
  private form: FormGroup;
  private isRequesting: boolean = false;
  private requestError;

  constructor(private router: Router, private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
      password: new FormControl('', Validators.required),
    })
  }

  private doLoginRequest({value, valid}: {value: LoginRequest, valid: boolean}) {
    if(valid) {
      this.isRequesting = true;
      this.wekker.doPostRequest('/account/authentication/', value, true)
        .subscribe(
          res => {
            localStorage.setItem('WekkerAccessToken', res.access_token);
            this.utilities.getUser();
            this.router.navigate(['/main'])
          },
          err => {
            this.requestError = err;
            this.isRequesting = false;
          }
        );
    }
  }

  private resetRequestError() {
    this.requestError = null;
  }
}
