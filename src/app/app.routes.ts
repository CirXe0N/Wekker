import {Routes} from "@angular/router";
import {LandingPageComponent} from "./landing-page/landing-page.component";

export const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home', component: LandingPageComponent
  }
];
