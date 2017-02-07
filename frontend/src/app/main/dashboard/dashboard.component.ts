import {Component, OnInit} from "@angular/core";
import {UtilitiesService} from "../../../services/utilities/utilities.service";

@Component({
  templateUrl: './dashboard.component.html'
})

export class DashboardComponent implements OnInit {
  private isActiveCollectionSidebar = false;
  private dashboardStatistics: any;

  constructor(private utilities: UtilitiesService) {}

  ngOnInit() {
    this.getDashboardStatistics();
  }

  private toggleCollectionSidebar(): void {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }

  private getDashboardStatistics(): void {
    this.utilities.getDasboardStatistics()
      .subscribe(res => {
        this.dashboardStatistics = res;
      })
  }
 }
