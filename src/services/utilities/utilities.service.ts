import {Injectable} from '@angular/core';
import {User, CollectionTVShow, CollectionMovie, DashboardStatistics} from "./utilities.interface";
import {Observable, Subject} from "rxjs";
import {Router} from "@angular/router";
import {WekkerAPIService} from "../wekker-api/wekker-api.service";

@Injectable()
export class UtilitiesService {
  private user: Subject<User> = new Subject<User>();
  private tvShowCollection: Subject<CollectionTVShow[]> = new Subject<CollectionTVShow[]>();
  private movieCollection: Subject<CollectionMovie[]> = new Subject<CollectionMovie[]>();
  private dashboardStatistics: Subject<DashboardStatistics> = new Subject<DashboardStatistics>();

  constructor(private router: Router, private wekker: WekkerAPIService) {}

  public getUser(): Observable<User> {
    this.wekker.doGetRequest('/users/')
      .subscribe(
        res => this.user.next(res),
        err => this.logout()
      );

    return this.user.asObservable().map(res => res);
  }

  public getTVShowCollection(): Observable<CollectionTVShow[]> {
    this.wekker.doGetRequest('/collections/tv-shows/')
      .subscribe(res => this.tvShowCollection.next(res));

    return this.tvShowCollection.asObservable().map(res => res);
  }

  public getMovieCollection(): Observable<CollectionMovie[]> {
    this.wekker.doGetRequest('/collections/movies/')
      .subscribe(res => this.movieCollection.next(res));

    return this.movieCollection.asObservable().map(res => res);
  }

  public getDasboardStatistics(): Observable<DashboardStatistics> {
    this.wekker.doGetRequest('/dashboard/statistics/')
      .subscribe(res => this.dashboardStatistics.next(res));

    return this.dashboardStatistics.asObservable().map(res => res);
  }

  public isLoggedIn(): boolean {
    if (localStorage.getItem('WekkerAccessToken')) {
      return true;
    }
    this.router.navigate(['/home']);
  }

  private logout(): void {
    localStorage.removeItem('WekkerAccessToken');
    this.router.navigate(['/home']);
  }

  public addZeroToSingleDigit(value: number): string {
    return value > 9 ? "" + value: "0" + value;
  }
}
