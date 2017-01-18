import {Component, OnInit} from "@angular/core";
import {Router} from "@angular/router";

@Component({
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})

export class MainComponent {
  private isActiveCollectionSidebar: boolean= false;
  private isActiveProfileMenu: boolean = false;

  constructor(private router: Router) {}

  private toggleCollectionSidebar() {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }

  private toggleProfileMenu() {
    this.isActiveProfileMenu = !this.isActiveProfileMenu;
  }

  private logout() {
    localStorage.removeItem('WekkerAccessToken');
    this.router.navigate(['/home']);
  }
}
