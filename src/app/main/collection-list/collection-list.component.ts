import {Component, OnInit} from '@angular/core';
import {tvShow, movie} from "./collection-list.interface";
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";

@Component({
  selector: 'collection-list',
  templateUrl: './collection-list.component.html',
  styleUrls: ['./collection-list.component.sass']
})

export class CollectionListComponent implements OnInit {
  private selectedListType: string = 'TV Shows';
  private collectionList: tvShow[] | movie[] = [];
  private tvShowList: tvShow[] =[];
  private movieList: movie[] = [];

  constructor(private wekker: WekkerAPIService) {}

  ngOnInit() {
    this.doGetTvShowCollection();
    this.doGetMovieCollection();
    this.selectTvShowCollection();
  }

  private selectTvShowCollection() {
    this.selectedListType = 'TV Shows';
    this.collectionList =  this.tvShowList;
  }

  private selectMovieCollection() {
    this.selectedListType = 'Movies';
    this.collectionList =  this.movieList;
  }

  private doSearchRequest(query: string) {
    this.wekker.doGetRequest('/tv-shows/?query=' + query)
      .debounceTime(5000)
      .subscribe(
        res => {
          console.log(res)
        }
    )
  }

  private doGetTvShowCollection() {
    this.tvShowList = [
      {
        title: 'Friends',
        poster_url: 'http://stuffpoint.com/friends/image/124272-friends-friends-poster.jpg',
        status: 'Ended',
        last_seen_episode: 's02e17',
        last_released_episode: 's02e18',
        is_up_to_date:  false,
        has_new_episode: true,
        amount_comments: 0,
        type: 'TV Show'
      },
      {
        title: 'How I Met Your Mother',
        poster_url: 'https://daisyishdays.files.wordpress.com/2014/02/how-i-met-your-mother-poster-bca998.jpg',
        status: 'In between seasons',
        last_seen_episode: 's02e17',
        last_released_episode: 's02e18',
        is_up_to_date:  false,
        has_new_episode: true,
        amount_comments: 2,
        type: 'TV Show'
      },
      {
        title: 'Lost',
        poster_url: 'http://www.cineparadise.com/wp-content/uploads/2014/05/final-season-lost-poster.jpg',
        status: 'Canceled',
        last_seen_episode: 's02e18',
        last_released_episode: 's02e18',
        is_up_to_date:  true,
        has_new_episode: false,
        amount_comments: 0,
        type: 'TV Show'
      }];
  }

  private doGetMovieCollection() {
    this.movieList = [
      {
        title: 'The Matrix',
        poster_url: 'https://www.movieposter.com/posters/archive/main/9/A70-4902',
        status: 'Released',
        release_date: '10/10/2016',
        is_watched: true,
        amount_comments: 99,
        type: 'Movie'
      },
      {
        title: 'Logan',
        poster_url: 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTUwNjU5NjgxOF5BMl5BanBnXkFtZTgwMDM5NjY5MDI@._V1_UX140_CR0,0,140,209_AL_.jpg',
        status: 'Not Released Yet',
        release_date: '10/10/2017',
        is_watched: false,
        amount_comments: 0,
        type: 'Movie'
      }
    ]
  }
}
