import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {NgxMapboxGLModule} from "ngx-mapbox-gl";
import {NgPipesModule} from "ngx-pipes";
import { ToplistComponent } from './toplist/toplist.component';
import {HttpClientModule} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent,
    ToplistComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgPipesModule,
    HttpClientModule,
    NgxMapboxGLModule.withConfig({
      accessToken: 'pk.eyJ1IjoibW9uc3Ryb2ZpbCIsImEiOiJjazVjbHc0ZWoxczNpM2xsamlsb2Vla3U3In0.D_AounEf87Va3Zq6Z8tTsg'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
