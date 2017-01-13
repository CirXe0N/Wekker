import {Routes} from "@angular/router";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {DashboardComponent} from "./main/dashboard/dashboard.component";
import {MainComponent} from "./main/main.component";
import {MovieDetailsComponent} from "./main/movie-details/movie-details-component";
import {TVShowDetailsComponent} from "./main/tv-show-details/tv-show-details.component";

export const appRoutes: Routes = [
  {
    path: '', redirectTo: '/home', pathMatch: 'full'
  },
  {
    path: 'home', component: LandingPageComponent
  },
  {
    path: 'main', component: MainComponent,
    children: [
      {
        path: '', component: DashboardComponent
      },
      {
        path: 'movies/:id', component: MovieDetailsComponent
      },
      {
        path: 'tv-shows/:id', component: TVShowDetailsComponent
      }
   ]
  }
];
