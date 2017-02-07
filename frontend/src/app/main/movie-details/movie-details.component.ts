import {Component} from "@angular/core";
import {Movie, Recommendation} from "./movie-details.interface";
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {UtilitiesService} from "../../../services/utilities/utilities.service";
import {DatesService} from "../../../services/dates/dates.service";
import {FormGroup, FormControl, Validators} from "@angular/forms";

@Component({
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.sass']
})

export class MovieDetailsComponent {
  private isLoading: boolean = true;
  private isRequestingCollectionItem: boolean = false;
  private isRequestingWatchedItem: boolean = false;
  private isRecommendationToggled: boolean = false;
  private isRequestingRecommendation: boolean = false;
  private movie: Movie;
  private form: FormGroup;

  constructor(private wekker: WekkerAPIService, private route: ActivatedRoute, private dates: DatesService,
              private utilities: UtilitiesService, private router: Router) {}

  ngOnInit() {
    this.form = new FormGroup({
      recipient: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
    });

    this.route.params
      .map(params => params['id'])
      .subscribe(
        res => {
          this.isLoading = true;
          this.doMovieDetailsRequest(res)
        }
      );
  }

  private doMovieDetailsRequest(movieId: string) {
    this.wekker.doGetRequest('/movies/' + movieId + '/')
      .subscribe(
        res => {
          this.movie = res;
          this.isLoading = false;
        },
        err => this.router.navigate(['/main'])
      );
  }

  private doToggleCollectionItemRequest() {
    this.isRequestingCollectionItem = true;
    let request = {
      is_collection_item: !this.movie.is_collection_item
    };

    this.wekker.doPutRequest('/movies/' + this.movie.movie_id + '/', request)
      .subscribe(res => {
        this.movie = res;
        this.utilities.getMovieCollection();
        this.isRequestingCollectionItem = false;
      });
  }

  private doToggleWatchedRequest() {
    this.isRequestingWatchedItem = true;
    let request = {
      is_watched: !this.movie.is_watched
    };

    this.wekker.doPutRequest('/movies/' + this.movie.movie_id + '/', request)
      .subscribe(res => {
        this.movie.is_watched = res.is_watched;
        this.utilities.getMovieCollection();
        this.isRequestingWatchedItem = false;
      });
  }

  private doSendRecommendationRequest({value, valid}: {value: Recommendation, valid: boolean}) {
    this.isRequestingRecommendation = true;
    if(valid) {
      value['media_type'] = 'Movie';
      value['movie_id'] =  this.movie.movie_id;

      this.wekker.doPostRequest('/recommendation/', value)
        .subscribe(res => {
          this.toggleRecommendation();
          this.isRequestingRecommendation = false;
          this.form.reset();
        })
    }
  }

  private toggleRecommendation() {
    this.isRecommendationToggled = !this.isRecommendationToggled;
  }

}
