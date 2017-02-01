import {Component, OnInit} from "@angular/core";
import {WekkerAPIService} from "../../../services/wekker-api/wekker-api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {TVShow, Recommendation} from "./tv-show-details.interface";
import {DatesService} from "../../../services/dates/dates.service";
import {UtilitiesService} from "../../../services/utilities/utilities.service";
import {FormGroup, Validators, FormControl} from "@angular/forms";

@Component({
  templateUrl: './tv-show-details.component.html',
  styleUrls: ['./tv-show-details.component.sass']
})

export class TVShowDetailsComponent implements OnInit {
  private isLoading: boolean = true;
  private isRequestingCollectionItem: boolean = false;
  private isRecommendationToggled: boolean = false;
  private isRequestingRecommendation: boolean = false;
  private selectedPage: string = 'Episode Guide';
  private tvShow: TVShow;
  private form: FormGroup;

  constructor(private wekker: WekkerAPIService, private route: ActivatedRoute, private dates: DatesService,
              private utilities: UtilitiesService, private router: Router) {}

  ngOnInit() {
    this.form = new FormGroup({
      recipient: new FormControl('', [Validators.required, Validators.pattern('.+@.+[.]+.+')]),
    });

    this.route.params
      .map(params => params['id'])
      .subscribe(res => {
        this.isLoading = true;
        this.doTVShowDetailsRequest(res)});
  }

  private doTVShowDetailsRequest(tvShowId: string) {
    this.wekker.doGetRequest('/tv-shows/' + tvShowId + '/')
      .subscribe(
        res => {
          this.tvShow = res;
          this.isLoading = false;
        },
        err => this.router.navigate(['/main'])
      );
  }

  private doToggleCollectionItemRequest() {
    this.isRequestingCollectionItem = true;
    let request = {
      is_collection_item: !this.tvShow.is_collection_item
    };

    this.wekker.doPutRequest('/tv-shows/' + this.tvShow.tv_show_id + '/', request)
      .subscribe(res => {
        this.tvShow = res;
        this.utilities.getTVShowCollection();
        this.isRequestingCollectionItem = false;
      });
  }

  private doSendRecommendationRequest({value, valid}: {value: Recommendation, valid: boolean}) {
    this.isRequestingRecommendation = true;
    if(valid) {
      value['media_type'] = 'TV Show';
      value['tv_show_id'] =  this.tvShow.tv_show_id;

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

  private selectPage(page: string) {
    this.selectedPage = page;
  }
}
