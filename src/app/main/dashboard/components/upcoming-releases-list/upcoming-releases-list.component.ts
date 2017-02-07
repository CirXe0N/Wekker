import {Component, OnInit} from "@angular/core";
import {UpcomingReleaseDate, UpcomingRelease} from "./upcoming-releases-list.interface";
import * as moment from "moment";
import {WekkerAPIService} from "../../../../../services/wekker-api/wekker-api.service";
import {Router} from "@angular/router";

declare let _: any;

@Component({
  selector: 'upcoming-releases-list',
  templateUrl: './upcoming-releases-list.component.html',
  styleUrls: ['./upcoming-releases-list.component.sass']
})

export class UpcomingReleasesListComponent implements OnInit {
  private releaseDates: UpcomingReleaseDate[] = [];

  constructor(private wekker: WekkerAPIService, private router: Router) {}

  ngOnInit(): void {
    this.initReleaseDatesAgenda(7);
    this.doReleaseDatesRequest();
  }

  private initReleaseDatesAgenda(days: number): void {
    for(let index = 0; index < days; index++) {
      let date = moment().add(index, 'days');

      let upcomingReleaseItem: UpcomingReleaseDate = {
        date: date.format('dddd DD MMMM YYYY'),
        releases: []
      };

      this.releaseDates.push(upcomingReleaseItem)
    }
  }

  private doReleaseDatesRequest(): void {
    let today = moment().valueOf();

    this.wekker.doGetRequest('/dashboard/upcoming-releases/?date=' + today)
      .subscribe(res => {
        for(let upcomingRelease of res) {
          let date = moment(upcomingRelease.release_date).format('dddd DD MMMM YYYY');
          let releaseDate = _.find(this.releaseDates, {'date': date});
          if(releaseDate){
            releaseDate.releases.push(upcomingRelease)
          }
        }
      });
  }


  private nagivateToMediaDetails(media: any) {
    if(media.type == 'TV Show') {
      this.router.navigate(['/main/tv-shows/' + media.tv_show_id])
    }

    if(media.type == 'Movie') {
      this.router.navigate(['/main/movies/' + media.movie_id])
    }
  }
}
