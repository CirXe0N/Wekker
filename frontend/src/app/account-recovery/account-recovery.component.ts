import {Component, OnInit, OnDestroy} from "@angular/core";
import {Router, ActivatedRoute} from "@angular/router";
import {WekkerAPIService} from "../../services/wekker-api/wekker-api.service";
import {Subscription} from "rxjs";
import {AccountRecovery} from "./account-recovery.interface";
import {FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, FormBuilder} from "@angular/forms";

@Component({
  templateUrl: './account-recovery.component.html',
  styleUrls: ['./account-recovery.component.sass']
})

export class AccountRecoveryComponent implements OnInit, OnDestroy {
  private form: FormGroup;
  private subscription: Subscription;
  private request: AccountRecovery;
  private isRequesting: boolean = false;
  private displayRequestError: string;
  private displayMatchingPasswordError: boolean;

  constructor(private router: Router, private activatedRoute: ActivatedRoute,
              private wekker: WekkerAPIService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.request = {
      token: '',
      password: ''
    };

    this.subscription = this.activatedRoute.params
      .subscribe(param => this.request.token = param['token']);

    this.form = this.fb.group({
      password: ['', Validators.required],
      repeat_password: ['', Validators.required],
    }, {validator: this.areEqualPasswords});
  }

  private doChangePasswordRequest({valid}: {valid: boolean}) {
    if (valid) {
      this.isRequesting = true;
      this.wekker.doPutRequest('/account/recovery/', this.request, true)
        .subscribe(
          res => this.router.navigate(['/main']),
          err => {
            this.displayRequestError = err;
            this.isRequesting = false;
          }
        )
    } else {
      if('areNotEqualPasswords' in this.form.errors) { this.displayMatchingPasswordError = true}
    }
  }

  private resetValidation(): void {
    this.displayRequestError = null;
    this.displayMatchingPasswordError = null;
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  private areEqualPasswords(group: FormGroup) {
    let password = group.get('password').value;
    let repeatPassword = group.get('repeat_password').value;
    if(password == repeatPassword) {
      return null
    }

    return {
      areNotEqualPasswords : true
    };
  }
}
