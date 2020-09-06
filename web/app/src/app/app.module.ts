import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {NgxMapboxGLModule} from "ngx-mapbox-gl";
import {NgPipesModule} from "ngx-pipes";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgPipesModule,
    NgxMapboxGLModule.withConfig({
      accessToken: 'pk.eyJ1IjoibW9uc3Ryb2ZpbCIsImEiOiJjazVjbHc0ZWoxczNpM2xsamlsb2Vla3U3In0.D_AounEf87Va3Zq6Z8tTsg'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
