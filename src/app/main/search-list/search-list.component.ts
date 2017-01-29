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
  private searchList: any[] = [];

  @Input() isOpen: boolean = false;
  @Input() isToggled: boolean = false;
  @Output() isToggledChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private wekker: WekkerAPIService, private dates: DatesService, private router: Router) {}

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

  private nagivateToTvShowDetails(tv_show_id: string) {
    if(this.isToggled) {
      this.isToggledChange.emit(false);
    }
    this.router.navigate(['/main/tv-shows/' + tv_show_id])
  }
}
