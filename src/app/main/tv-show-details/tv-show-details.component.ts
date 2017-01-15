import {Component} from "@angular/core";

@Component({
  templateUrl: './tv-show-details.component.html'
})

export class TVShowDetailsComponent {
  private selectedPage: string = 'Episode Guide';

  private selectPage(page: string) {
    this.selectedPage = page;
  }
}
