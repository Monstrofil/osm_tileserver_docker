import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ToplistService {

  constructor(private http: HttpClient) { }

  getTopList() {
    return this.http.get('https://uacycling.info/cycleways/');
  }
}
