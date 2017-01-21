import {Component, OnInit} from "@angular/core";
import {Router} from "@angular/router";
import {UtilitiesService} from "../../services/utilities/utilities.service";
import {WekkerAPIService} from "../../services/wekker-api/wekker-api.service";
import {User} from "../../services/utilities/utilities.interface";

@Component({
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})

export class MainComponent implements OnInit {
  private isActiveCollectionSidebar: boolean= false;
  private isActiveProfileMenu: boolean = false;
  private isVerificationEmailSent: boolean = false;
  private user: User;

  constructor(private router: Router, private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnInit(): void {
    this.doGetUserDataRequest();
  }

  private toggleCollectionSidebar(): void {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }

  private toggleProfileMenu(): void {
    this.isActiveProfileMenu = !this.isActiveProfileMenu;
  }

  private resendVerificationEmail(): void {
    this.wekker.doGetRequest('/account/authentication/')
      .subscribe(() => {});

    this.isVerificationEmailSent = true;
  }

  private doGetUserDataRequest(): void {
    this.wekker.doGetRequest('/users/')
      .subscribe(
        res => {
          this.user = res;
          this.utilities.setUser(res);
        },
        err => this.logout()
      )
  }

  private logout(): void {
    localStorage.removeItem('WekkerAccessToken');
    this.router.navigate(['/home']);
  }
}
