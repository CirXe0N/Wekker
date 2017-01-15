import {Component} from "@angular/core";

@Component({
  selector: 'episode-guide',
  templateUrl: './episode-guide.component.html',
  styleUrls: ['./episode-guide.component.sass']
})

export class EpisodeGuideComponent {
  private selectedSeason: number = 1;

  private selectSeason(episode: number) {
    this.selectedSeason = episode;
  }
}
