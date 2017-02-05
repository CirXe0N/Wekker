import {Routes} from "@angular/router";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {DashboardComponent} from "./main/dashboard/dashboard.component";
import {MainComponent} from "./main/main.component";
import {MovieDetailsComponent} from "./main/movie-details/movie-details.component";
import {TVShowDetailsComponent} from "./main/tv-show-details/tv-show-details.component";
import {AuthenticationGuard} from "../guards/authentication.guard";
import {AccountVerificationComponent} from "./account-verification/account-verification.component";
import {AccountRecoveryComponent} from "./account-recovery/account-recovery.component";
import {UserProfileComponent} from "./main/user-profile/user-profile.component";

export const appRoutes: Routes = [
  {
    path: '', redirectTo: '/main', pathMatch: 'full'
  },
  {
    path: 'home', component: LandingPageComponent
  },
  {
    path: 'account-verification/:profile', component: AccountVerificationComponent
  },
  {
    path: 'account-recovery/:token', component: AccountRecoveryComponent
  },
  {
    path: 'main', component: MainComponent, canActivate: [AuthenticationGuard],
    children: [
      {
        path: '', component: DashboardComponent
      },
      {
        path: 'movies/:id', component: MovieDetailsComponent
      },
      {
        path: 'tv-shows/:id', component: TVShowDetailsComponent
      },
      {
        path: 'user-profile', component: UserProfileComponent
      }
   ]
  }
];
