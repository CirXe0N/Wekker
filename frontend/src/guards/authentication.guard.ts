import {Injectable} from '@angular/core';
import {CanActivate} from '@angular/router';
import {UtilitiesService} from "../services/utilities/utilities.service";

@Injectable()
export class AuthenticationGuard implements CanActivate {

  constructor(private utilities: UtilitiesService) {}

  canActivate() {
    return this.utilities.isLoggedIn();
  }
}
