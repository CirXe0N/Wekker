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
  private user: User;
  private isOpenCollectionSidebar: boolean = true;
  private isOpenSearchSidebar: boolean = false;

  private isToggledCollectionSidebar: boolean = false;
  private isToggledSearchSidebar: boolean = false;


  private isActiveProfileMenu: boolean = false;
  private isVerificationEmailSent: boolean = false;

  constructor(private router: Router, private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnInit(): void {
    this.getUser();
  }

  private getUser(): void {
    this.utilities.getUser()
      .subscribe(res => this.user = res);
  }

  private toggleCollectionSidebar(): void {
    this.isToggledCollectionSidebar = !this.isToggledCollectionSidebar;

    if(this.isToggledCollectionSidebar) {
      this.isToggledSearchSidebar = false;
    }
  }

  private toggleSearchSidebar(): void {
    this.isToggledSearchSidebar = !this.isToggledSearchSidebar;
    if(this.isToggledSearchSidebar) {
      this.isToggledCollectionSidebar = false;
    }
  }

  private openCollectionSidebar(): void {
    this.isOpenCollectionSidebar = true;
    this.isOpenSearchSidebar = false;
  }

  private openSearchSidebar(): void {
    this.isOpenCollectionSidebar = false;
    this.isOpenSearchSidebar = true;
  }

  private toggleProfileMenu(): void {
    this.isActiveProfileMenu = !this.isActiveProfileMenu;
  }

  private resendVerificationEmail(): void {
    this.wekker.doGetRequest('/account/authentication/')
      .subscribe(() => {});

    this.isVerificationEmailSent = true;
  }

  private navigateToUserProfile(): void {
    this.toggleProfileMenu();
    this.router.navigate(['/main/user-profile/']);
  }

  private navigateToMain(): void {
    this.router.navigate(['/main/']);
  }
}
