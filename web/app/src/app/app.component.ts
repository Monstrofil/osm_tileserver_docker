import { Component } from '@angular/core';
import { Map } from 'mapbox-gl';
import {StorageMap} from '@ngx-pwa/local-storage';
import {first, take} from 'rxjs/operators';
import {forkJoin, merge} from 'rxjs';

class LegendItem {
  color: any;
  title: string;
  dasharray: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'web';
  map: Map;

  layers = [
    'cyclelane-pedestrian-working'
  ];

  zoom = [10];
  center = [35.0409, 48.4755];

  legend: LegendItem[] = [];

  constructor(private storage: StorageMap) {
    forkJoin([
        this.storage.get('zoom').pipe(
        take(1)
      ),
        this.storage.get('location').pipe(
        take(1)
      )
    ]).subscribe((values) => {
      if (values[0]) {
        this.zoom = [values[0] as number];
      }
      if (values[1]) {
        this.center = values[1] as number[];
      }
    });
  }

  onMoveEnd(event) {
    this.storage.set('location', event.target.getCenter()).subscribe(() => {});
  }

  onZoomEnd(event) {
    this.storage.set('zoom', event.target.getZoom()).subscribe(() => {});
    console.log('zoom', event.target.getZoom());
  }

  onMapLoad(map) {
    map.getStyle().layers.forEach(layer => {
      if (!(layer.metadata && layer.metadata['maputnik:comment'])) {
        return;
      }
      this.legend.push({
        color: layer.paint['line-color'],
        title: layer.metadata['maputnik:comment'],
        dasharray: layer.paint['line-dasharray']
      });
    });
    this.legend.sort((a, b) => {
      return (a.title < b.title) ? -1 : 1;
    });

    // this.storage.get('zoom').pipe(take(1)).subscribe((value) => {
    //   if (!value) { return; }
    //   console.log(this.zoom, value);
    //   map.setZoom(value);
    // });
    // this.storage.get('location').pipe(take(1)).subscribe((value) => {
    //   if (!value) { return; }
    //   map.setCenter(value);
    // });
  }
}
