import { Component, OnInit } from '@angular/core';
import {ToplistService} from "./toplist.service";
import {Observable, Subject} from "rxjs";

class ByStatusInfo {
  working: number;
  proposed: number;
  construction: number;
  total: number;
}

class LengthInfo {
  cycleway: ByStatusInfo;
  cyclelane: ByStatusInfo;
  cyclefootway: ByStatusInfo;
  total: number;
}

class Record {
  name: string;

  length: LengthInfo;
}


@Component({
  selector: 'app-toplist',
  templateUrl: './toplist.component.html',
  styleUrls: ['./toplist.component.scss']
})
export class ToplistComponent implements OnInit {

  public topList: Record[];
  public order = 'length.total';
  public direction = -1;

  constructor(private provider: ToplistService) { }

  ngOnInit(): void {
    this.provider.getTopList().subscribe((data: Record[]) => {
      this.topList = data;
    });
  }

  setOrder(value) {
    if (this.order == value) {
      this.direction *= -1;
    }
    else {
      this.direction = -1;
      this.order = value;
    }
  }

}
