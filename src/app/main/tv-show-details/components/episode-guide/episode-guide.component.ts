import {Component, Input, OnChanges} from "@angular/core";
import {Season} from "../../tv-show-details.interface";
import {DatesService} from "../../../../../services/dates/dates.service";

@Component({
  selector: 'episode-guide',
  templateUrl: './episode-guide.component.html',
  styleUrls: ['./episode-guide.component.sass']
})

export class EpisodeGuideComponent implements OnChanges {
  private selectedSeasonNumber: number = 1;
  private selectedSeason: Season;

  @Input() seasons: Season[];

  constructor(private dates: DatesService) {}

  ngOnChanges(): void {
    if(this.seasons && this.seasons.length > 0) {
      for(let season of this.seasons) {
        season.is_watched = this.checkWatchedStatus(season);
      }

      this.selectSeason(this.seasons[0]);
    }
  }

  private selectSeason(season: Season): void {
    this.selectedSeason = season;
    this.selectedSeasonNumber = season.season_number;
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
