import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {UtilitiesService} from "../../../services/utilities/utilities.service";
import {CollectionTVShow} from "../../../services/utilities/utilities.interface";
import {Router} from "@angular/router";
import {DatesService} from "../../../services/dates/dates.service";

@Component({
  selector: 'collection-list',
  templateUrl: './collection-list.component.html',
  styleUrls: ['./collection-list.component.sass']
})

export class CollectionListComponent implements OnInit {
  private isRequestingCollection: boolean = true;
  private selectedListType: string = 'TV Shows';
  private collectionList: CollectionTVShow[] | any[] = [];
  private tvShowList: CollectionTVShow[] =[];
  private movieList: any[] = [];

  @Input() isOpen: boolean = false;
  @Input() isToggled: boolean = false;
  @Output() isToggledChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private utilities: UtilitiesService, private dates: DatesService, private router: Router) {}

  ngOnInit(): void {
    this.doGetTvShowCollection();
    this.doGetMovieCollection();
  }

  private doGetTvShowCollection() {
    this.utilities.getTVShowCollection()
      .subscribe(res => {
        this.tvShowList = res;
        this.selectTvShowCollection();
        this.isRequestingCollection = false;
      });
  }

  private doGetMovieCollection() {
    this.utilities.getMovieCollection()
      .subscribe(res => {
        this.movieList = res;

        if(this.selectedListType == 'Movies') {
          this.selectMovieCollection();
        }
      });
  }

  private selectTvShowCollection() {
    this.selectedListType = 'TV Shows';
    this.collectionList =  this.tvShowList;
  }

  private selectMovieCollection() {
    this.selectedListType = 'Movies';
    this.collectionList =  this.movieList;
  }

  private nagivateToMediaDetails(media: any) {
    if(this.isToggled) {
      this.isToggledChange.emit(false);
    }

    if(this.selectedListType == 'TV Shows') {
      this.router.navigate(['/main/tv-shows/' + media.tv_show_id])
    }

    if(this.selectedListType == 'Movies') {
      this.router.navigate(['/main/movies/' + media.movie_id])
    }
  }

  private checkWatchProgress(tvShow: CollectionTVShow) {
    let lastSeenEpisode = tvShow.last_seen_episode;
    let lastReleasedEpisode = tvShow.last_released_episode;
    if(lastReleasedEpisode) {
      return JSON.stringify(lastSeenEpisode) == JSON.stringify(lastReleasedEpisode);
    }
    return false
  }
}
