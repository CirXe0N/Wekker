import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import {RouterModule} from "@angular/router";
import {appRoutes} from "./app.routes";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {LoginComponent} from "./landing-page/components/login/login.component";
import {SignUpComponent} from "./landing-page/components/sign-up/sign-up.component";
import {ForgotPasswordComponent} from "./landing-page/components/forgot-password/forgot-password.component";
import {DashboardComponent} from "./main/dashboard/dashboard.component";
import {CollectionListComponent} from "./main/collection-list/collection-list.component";
import {UpcomingReleasesListComponent} from "./main/dashboard/components/upcoming-releases-list/upcoming-releases-list.component";
import {StatisticCardComponent} from "./main/dashboard/components/statistic-card/statistic-card.component";
import {WatchListComponent} from "./main/dashboard/components/watch-list/watch-list.component";
import {IdeaBoxComponent} from "./main/dashboard/components/idea-box/idea-box.component";
import {MainComponent} from "./main/main.component";
import {TVShowDetailsComponent} from "./main/tv-show-details/tv-show-details.component";
import {MovieDetailsComponent} from "./main/movie-details/movie-details.component";
import {EpisodeGuideComponent} from "./main/tv-show-details/components/episode-guide/episode-guide.component";
import {CrewListComponent} from "./main/crew-list/crew-list.component";
import {SettingsService} from "../services/settings/settings.service";
import {WekkerAPIService} from "../services/wekker-api/wekker-api.service";
import {UtilitiesService} from "../services/utilities/utilities.service";
import {AuthenticationGuard} from "../guards/authentication.guard";
import {AccountVerificationComponent} from "./account-verification/account-verification.component";
import {AccountRecoveryComponent} from "./account-recovery/account-recovery.component";
import {SearchListComponent} from "./main/search-list/search-list.component";
import {DatesService} from "../services/dates/dates.service";

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    LoginComponent,
    SignUpComponent,
    ForgotPasswordComponent,
    MainComponent,
    DashboardComponent,
    CollectionListComponent,
    SearchListComponent,
    UpcomingReleasesListComponent,
    StatisticCardComponent,
    WatchListComponent,
    IdeaBoxComponent,
    MovieDetailsComponent,
    TVShowDetailsComponent,
    EpisodeGuideComponent,
    CrewListComponent,
    AccountVerificationComponent,
    AccountRecoveryComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    ReactiveFormsModule,
    FormsModule,
    HttpModule
  ],
  providers: [
    SettingsService,
    UtilitiesService,
    WekkerAPIService,
    DatesService,
    AuthenticationGuard
  ],
  bootstrap: [AppComponent]
})

export class AppModule {}
