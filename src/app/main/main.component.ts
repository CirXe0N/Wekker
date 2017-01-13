import {Component, OnInit} from "@angular/core";

@Component({
  templateUrl: './main.component.html'
})

export class MainComponent implements OnInit {
  private isActiveCollectionSidebar = false;

  ngOnInit() {}

  private toggleCollectionSidebar() {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }
}
