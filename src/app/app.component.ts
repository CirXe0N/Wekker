import { Component } from '@angular/core';
import {Router, NavigationEnd} from "@angular/router";
import {environment} from "../environments/environment";

declare let ga: Function;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})

export class AppComponent {
  constructor(public router: Router) {
    if (environment.production) {
      this.enableGoogleAnalytics();
    }
  }

  private enableGoogleAnalytics(): void {
    ga('create', 'UA-91383599-1', 'auto');

    this.router.events.subscribe(
      event => {
        if (event instanceof NavigationEnd && ga) {
          ga('set', 'page', event.urlAfterRedirects);
          ga('send', 'pageview');
        }
      }
    )
  }
}


