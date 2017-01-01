import {Routes} from "@angular/router";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {DashboardComponent} from "./dashboard/dashboard.component";

export const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home', component: LandingPageComponent
  },
  {
    path: 'dashboard', component: DashboardComponent
  }
];
