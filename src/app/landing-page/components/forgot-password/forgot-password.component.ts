import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators} from "@angular/forms";
import {ForgotPasswordRequest} from "./forgot-password.interface";
import {WekkerAPIService} from "../../../../services/wekker-api/wekker-api.service";

@Component({
  selector: 'forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.sass']
})

export class ForgotPasswordComponent implements OnInit {
  private form: FormGroup;
  private isSuccessfulRequest: boolean = false;
  private isRequesting: boolean = false;

  constructor(private wekker: WekkerAPIService) {}

  ngOnInit() {
    this.form = new FormGroup({
      email_address: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')])
    })
  }

  private doForgotPasswordRequest({value, valid}: {value: ForgotPasswordRequest, valid: boolean}) {
    this.isSuccessfulRequest = false;

    if(valid) {
      this.isRequesting = true;
      this.wekker.doPostRequest('/account/recovery/', value, true)
        .subscribe(
          res => {
            this.isSuccessfulRequest = true;
            this.isRequesting = false;
          }
        );
    }
  }
}
