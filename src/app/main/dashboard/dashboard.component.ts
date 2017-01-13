import {Component, OnInit} from "@angular/core";

@Component({
  templateUrl: './dashboard.component.html'
})

export class DashboardComponent implements OnInit {
  private isActiveCollectionSidebar = false;

  ngOnInit() {}

  private toggleCollectionSidebar() {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }
}
