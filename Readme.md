## Quickstart

1. Download .pbf dump of region you want to render (e.g. using https://download.geofabrik.de/).
   Let's take `luxembourg-latest.osm.pbf` as and example.
2. Place downloaded `luxembourg-latest.osm.pbf` file into `data` folder.
3. Run `./manage.sh import luxembourg-latest.osm.pbf` in order to start postgis and import osm data into.
4. Run `./manage.sh run` to start webserver (works on 8082 port by default). 
   Generated tiles are available by `http://localhost:8082/osm/{z}/{x}/{y}.png`


## Recommended hardware
TODO:


