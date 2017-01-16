import {Component} from "@angular/core";

@Component({
  templateUrl: './tv-show-details.component.html',
  styleUrls: ['./tv-show-details.component.sass']
})

export class TVShowDetailsComponent {
  private selectedPage: string = 'Episode Guide';

  private selectPage(page: string) {
    this.selectedPage = page;
  }
}
