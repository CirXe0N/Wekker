import {Component, OnInit} from "@angular/core";
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {ActivatedRoute} from "@angular/router";
import {TVShow} from "./tv-show-details.interface";
import {SettingsService} from "../../../services/settings/settings.service";
import {DatesService} from "../../../services/dates/dates.service";

@Component({
  templateUrl: './tv-show-details.component.html',
  styleUrls: ['./tv-show-details.component.sass']
})

export class TVShowDetailsComponent implements OnInit {
  private selectedPage: string = 'Episode Guide';
  private tvShow: TVShow;

  constructor(private wekker: WekkerAPIService, private route: ActivatedRoute, private settings: SettingsService,
              private dates: DatesService) {}

  ngOnInit() {
    this.route.params
      .map(params => params['id'])
      .subscribe(res => this.doTVShowDetailsRequest(res));
  }

  private doTVShowDetailsRequest(tvShowId: string) {
    this.wekker.doGetRequest('/tv-shows/' + tvShowId + '/')
      .subscribe(res => this.tvShow = res);
  }

  private selectPage(page: string) {
    this.selectedPage = page;
  }
}
