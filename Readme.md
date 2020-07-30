## Quickstart

0. If you don't want to build images from source, run `docker-compose pull` before any futher steps.
1. Download .pbf dump of region you want to render (e.g. using https://download.geofabrik.de/).
   Let's take `luxembourg-latest.osm.pbf` as and example.
2. Place downloaded `luxembourg-latest.osm.pbf` file into `data` folder.
3. Run `./manage.sh import luxembourg-latest.osm.pbf` in order to start postgis and import osm data into.
4. Run `./manage.sh run` to start webserver (works on 8082 port by default). 
   Generated tiles are available by `http://localhost:8082/osm/{z}/{x}/{y}.png`


### Prerendering tiles
You can prerender given area using following command:
```text
/manage.sh render prerender --help
usage: manage.py prerender [-h] [--lat_min LAT_MIN] [--lng_min LNG_MIN]
                           [--lat_max LAT_MAX] [--lng_max LNG_MAX]
                           [--min-zoom MIN_ZOOM] [--max-zoom MAX_ZOOM]

optional arguments:
  -h, --help           show this help message and exit
  --lat_min LAT_MIN
  --lng_min LNG_MIN
  --lat_max LAT_MAX
  --lng_max LNG_MAX
  --min-zoom MIN_ZOOM
  --max-zoom MAX_ZOOM
```

In order to find boundary you can use [bboxfinder](http://bboxfinder.com/).

## Recommended hardware
TODO:


