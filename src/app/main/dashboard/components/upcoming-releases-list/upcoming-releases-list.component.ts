import {Component, OnInit} from "@angular/core";
import {UpcomingReleaseDate} from "./upcoming-releases-list.interface";
import * as moment from "moment";

@Component({
  selector: 'upcoming-releases-list',
  templateUrl: './upcoming-releases-list.component.html',
  styleUrls: ['./upcoming-releases-list.component.sass']
})

export class UpcomingReleasesListComponent implements OnInit {
  private releaseDates: UpcomingReleaseDate[] = [];

  ngOnInit() {
    this.doReleaseDatesRequest();
  }

  private doReleaseDatesRequest(): void {
    let today = moment().toISOString();
    this.releaseDates = [
      {
        date: 'SUNDAY 08 JANUARY 2017',
        releases: []
      },
      {
        date: 'MONDAY 09 JANUARY 2017',
        releases: []
      },
      {
        date: 'TUESDAY 10 JANUARY 2017',
        releases: []
      },
      {
        date: 'WEDNESDAY 11 JANUARY 2017',
        releases: []
      },
      {
        date: 'THURSDAY 12 JANUARY 2017',
        releases: []
      },
      {
        date: 'FRIDAY 13 JANUARY 2017',
        releases: []
      },
      {
        date: 'SATURDAY 14 JANUARY 2017',
        releases: []
      }
    ];
  }
}
