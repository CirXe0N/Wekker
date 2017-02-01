import {Component, OnInit} from "@angular/core";
import {WekkerAPIService} from "../../../../../services/wekker-api/wekker-api.service";
import {UtilitiesService} from "../../../../../services/utilities/utilities.service";

@Component({
  selector: 'watch-list',
  templateUrl: './watch-list.component.html',
  styleUrls: ['./watch-list.component.sass']
})

export class WatchListComponent implements OnInit {
  private watchList: any[] = [];

  constructor(private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnInit(): void {
    this.doGetWatchListRequest();
  }

  private doGetWatchListRequest(): void {
    this.wekker.doGetRequest('/dashboard/watch-list/')
      .subscribe(res => this.watchList = res);
  }

  private doUpdateWatchedEpisodeRequest(episode: any) {
    episode.isRequestingWatched = true;
    let request = {
      is_watched: !episode.is_watched
    };

    this.wekker.doPutRequest('/tv-show-episodes/' + episode.episode_id + '/', request)
      .subscribe(res => {
        this.doGetWatchListRequest();
        this.utilities.getTVShowCollection();
        this.utilities.getDasboardStatistics();
        episode.isRequestingWatched = false;
      });
  }
}
