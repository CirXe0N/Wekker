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
import {CollectionListComponent} from "./main/dashboard/components/collection-list/collection-list.component";
import {CollectionListSearchPipe} from "./main/dashboard/components/collection-list/pipes/collection-list-search.pipe";
import {UpcomingReleasesListComponent} from "./main/dashboard/components/upcoming-releases-list/upcoming-releases-list.component";
import {StatisticCardComponent} from "./main/dashboard/components/statistic-card/statistic-card.component";
import {WatchListComponent} from "./main/dashboard/components/watch-list/watch-list.component";
import {IdeaBoxComponent} from "./main/dashboard/components/idea-box/idea-box.component";
import {MainComponent} from "./main/main.component";
import {TVShowDetailsComponent} from "./main/tv-show-details/tv-show-details.component";
import {MovieDetailsComponent} from "./main/movie-details/movie-details-component";

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
    CollectionListSearchPipe,
    UpcomingReleasesListComponent,
    StatisticCardComponent,
    WatchListComponent,
    IdeaBoxComponent,
    MovieDetailsComponent,
    TVShowDetailsComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    ReactiveFormsModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule {}
