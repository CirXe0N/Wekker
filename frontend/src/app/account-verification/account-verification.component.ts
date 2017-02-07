import {Component, OnInit, OnDestroy} from "@angular/core";
import {Router, ActivatedRoute} from "@angular/router";
import {WekkerAPIService} from "../../services/wekker-api/wekker-api.service";
import {Subscription} from "rxjs";

@Component({
  template: ''
})

export class AccountVerificationComponent implements OnInit, OnDestroy {
  private subscription: Subscription;

  constructor(private router: Router, private activatedRoute: ActivatedRoute, private wekker: WekkerAPIService) {}

  ngOnInit(): void {
    this.subscription = this.activatedRoute.params.subscribe(
      param => {
        this.wekker.doPutRequest('/account/authentication/', {profile_id: param['profile']}, true)
          .subscribe(res => {this.router.navigate(['/main'])})
      });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
