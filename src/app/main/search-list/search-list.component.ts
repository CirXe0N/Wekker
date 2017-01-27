import {Component, OnInit} from '@angular/core';
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {DatesService} from "../../../services/dates/dates.service";

@Component({
  selector: 'search-list',
  templateUrl: './search-list.component.html',
  styleUrls: ['./search-list.component.sass']
})

export class SearchListComponent implements OnInit {
  private searchList: any[] = [];

  constructor(private wekker: WekkerAPIService, private dates: DatesService) {}

  ngOnInit() {}

  private doSearchRequest(query: string) {
    this.wekker.doGetRequest('/tv-shows/?query=' + query)
      .debounceTime(5000)
      .subscribe(
        res => {
          this.searchList = res;
          console.log(res)
        }
      )
  }
}
