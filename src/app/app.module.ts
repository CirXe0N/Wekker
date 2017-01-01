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
import {DashboardComponent} from "./dashboard/dashboard.component";
import {CollectionListComponent} from "./dashboard/components/collection-list/collection-list.component";
import {CollectionListSearchPipe} from "./dashboard/components/collection-list/pipes/collection-list-search.pipe";

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    LoginComponent,
    SignUpComponent,
    ForgotPasswordComponent,
    DashboardComponent,
    CollectionListComponent,
    CollectionListSearchPipe
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
