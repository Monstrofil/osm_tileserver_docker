import { Component } from '@angular/core';
import { Map } from 'mapbox-gl';

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

  legend: LegendItem[] = [];

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

    console.log(this.legend)
  }
}
