import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {SignUpRequest} from "./sign-up.interface";
import {WekkerAPIService} from "../../../../services/wekker-api/wekker-api.service";
import {Router} from "@angular/router";
import {UtilitiesService} from "../../../../services/utilities/utilities.service";

@Component({
  selector: 'sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.sass']
})

export class SignUpComponent implements OnInit {
  private form: FormGroup;
  private requestError: any[] = [];
  private isRequesting: boolean = false;

  constructor(private router: Router, private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnInit() {
    this.form = new FormGroup({
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
      password: new FormControl('', [Validators.required, Validators.minLength(5)]),
    });
  }

  private doSignUpRequest({value, valid}: {value: SignUpRequest, valid: boolean}) {
    if(valid) {
      this.isRequesting = true;
      this.wekker.doPostRequest('/users/', value, true)
        .subscribe(
          res => {
            this.utilities.setUser(res);
            localStorage.setItem('WekkerAccessToken', res.access_token);
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
    this.requestError = [];
  }
}
