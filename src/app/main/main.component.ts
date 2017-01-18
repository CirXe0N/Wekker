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

  private toggleCollectionSidebar(): void {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }

  private toggleProfileMenu(): void {
    this.isActiveProfileMenu = !this.isActiveProfileMenu;
  }

  private logout(): void {
    localStorage.removeItem('WekkerAccessToken');
    this.router.navigate(['/home']);
  }
}
