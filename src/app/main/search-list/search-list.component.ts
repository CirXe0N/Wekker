import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {DatesService} from "../../../services/dates/dates.service";
import {Router} from "@angular/router";

@Component({
  selector: 'search-list',
  templateUrl: './search-list.component.html',
  styleUrls: ['./search-list.component.sass']
})

export class SearchListComponent implements OnInit {
  private isRequestingSearch: boolean =  false;
  private searchList: any[] = [];

  @Input() isOpen: boolean = false;
  @Input() isToggled: boolean = false;
  @Output() isToggledChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private wekker: WekkerAPIService, private dates: DatesService, private router: Router) {}

  ngOnInit() {}

  private doSearchRequest(query: string) {
    this.isRequestingSearch = true;
    this.wekker.doGetRequest('/search/?query=' + query)
      .subscribe(
        res => {
          console.log(res);
          this.searchList = res;
          setTimeout(()=>this.isRequestingSearch = false, 2000);
        }
      )
  }

  private nagivateToMediaDetails(media: any) {
    if(this.isToggled) {
      this.isToggledChange.emit(false);
    }

    if(media.type == 'TV Show') {
      this.router.navigate(['/main/tv-shows/' + media.tv_show_id])
    }

    if(media.type == 'Movie') {
      this.router.navigate(['/main/movies/' + media.movie_id])
    }
  }
}
