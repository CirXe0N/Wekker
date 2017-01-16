import {Component, OnInit} from "@angular/core";

@Component({
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})

export class MainComponent implements OnInit {
  private isActiveCollectionSidebar = false;

  ngOnInit() {}

  private toggleCollectionSidebar() {
    this.isActiveCollectionSidebar = !this.isActiveCollectionSidebar;
  }
}
