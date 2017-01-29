import {Component, Input, OnChanges, SimpleChanges} from "@angular/core";
import {Season, Episode} from "../../tv-show-details.interface";
import {DatesService} from "../../../../../services/dates/dates.service";
import {WekkerAPIService} from "../../../../../services/wekker-api/wekker-api.service";
import {UtilitiesService} from "../../../../../services/utilities/utilities.service";

@Component({
  selector: 'episode-guide',
  templateUrl: './episode-guide.component.html',
  styleUrls: ['./episode-guide.component.sass']
})

export class EpisodeGuideComponent implements OnChanges {
  private selectedSeasonNumber: number = 1;
  private selectedSeason: Season;

  @Input() seasons: Season[];

  constructor(private dates: DatesService, private wekker: WekkerAPIService, private utilities: UtilitiesService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if(changes['seasons'].currentValue) {
      for (let season of this.seasons) {
        season.is_watched = this.checkWatchedStatus(season);
      }

      this.selectSeason(this.seasons[0]);
    }
  }

  private selectSeason(season: Season): void {
    this.selectedSeason = season;
    this.selectedSeasonNumber = season.season_number;
  }

  private doUpdateWatchedEpisodeRequest(episode: Episode) {
    let request = {
      is_watched: !episode.is_watched
    };

    this.wekker.doPutRequest('/tv-show-episodes/' + episode.episode_id + '/', request)
      .subscribe(res => {
        episode.is_watched = res.is_watched;
        this.utilities.getTVShowCollection();
      });
  }

  private checkWatchedStatus(season: Season): boolean {
    for(let episode of season.episodes) {
      if (!episode.is_watched) {
        return false;
      }
    }
    return true;
  }
}
