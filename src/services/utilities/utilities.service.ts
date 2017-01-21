import {Injectable} from '@angular/core';
import {User} from "./utilities.interface";
import {ReplaySubject, Observable} from "rxjs";
import {Router} from "@angular/router";
import {WekkerAPIService} from "../wekker-api/wekker-api.service";

@Injectable()
export class UtilitiesService {
  private user: ReplaySubject<User> = new ReplaySubject<User>();

  constructor(private router: Router, private wekker: WekkerAPIService) {}

  public setUser(user: User): void {
    this.user.next(user);
  }

  public getUser(): Observable<User> {
    return this.user.asObservable().map(user => user);
  }

  public isLoggedIn(): boolean {
    if (localStorage.getItem('WekkerAccessToken')) {
      return true;
    }

    this.router.navigate(['/home']);
  }
}
