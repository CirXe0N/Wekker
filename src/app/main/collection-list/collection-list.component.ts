import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {UtilitiesService} from "../../../services/utilities/utilities.service";
import {CollectionTVShow} from "../../../services/utilities/utilities.interface";
import {Router} from "@angular/router";

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

  constructor(private utilities: UtilitiesService, private router: Router) {}

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

  private nagivateToTvShowDetails(tv_show_id: string) {
    if(this.isToggled) {
      this.isToggledChange.emit(false);
    }
    this.router.navigate(['/main/tv-shows/' + tv_show_id])
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
