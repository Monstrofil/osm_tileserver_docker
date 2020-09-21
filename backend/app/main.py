import json
import os
from itertools import groupby
from operator import itemgetter

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)

config = {
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    'SQLALCHEMY_DATABASE_URI': f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
                               f"@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"
}

app.config.from_mapping(config)
db = SQLAlchemy(app)
db.init_app(app)
cache = Cache(app)


@cache.cached(timeout=3600)
@app.route("/cycleways/")
def cycleways():
    r = db.engine.execute("""
        SELECT 
           bounded.name AS name, 
           COALESCE(bounded.status, 'working'),
           bounded.type, 
           COALESCE(Sum(ST_Length(bounded.geometry)), 0) AS length 
          FROM (
            SELECT
                osm_administrative.osm_id AS osm_id,
                osm_administrative.name AS name,
                'cycleway' AS type,
                ST_Intersection(osm_cycleways.geometry, osm_administrative.geometry) AS geometry,
                CASE
                   WHEN osm_cycleways.highway NOT IN ('construction', 'proposed') THEN 'working'
                   ELSE osm_cycleways.highway
                END AS status
            FROM osm_administrative
                LEFT JOIN osm_cycleways
                ON osm_cycleways.geometry && ST_Envelope(osm_administrative.geometry)

            UNION ALL

            SELECT
                osm_administrative.osm_id AS osm_id,
                osm_administrative.name AS name,
                'cyclefootway' AS type,
                ST_Intersection(osm_cycleways_foot_shared.geometry, osm_administrative.geometry) AS geometry,
                CASE
                   WHEN osm_cycleways_foot_shared.highway NOT IN ('construction', 'proposed') THEN 'working'
                   ELSE osm_cycleways_foot_shared.highway
                END AS status
            FROM osm_administrative
                LEFT JOIN osm_cycleways_foot_shared
                ON osm_cycleways_foot_shared.geometry && ST_Envelope(osm_administrative.geometry)

            UNION ALL

            SELECT
                osm_administrative.osm_id AS osm_id,
                osm_administrative.name AS name,
                'cyclelane' AS type,
                ST_Intersection(osm_cycleway_lanes.geometry, osm_administrative.geometry) AS geometry,
                CASE
                   WHEN osm_cycleway_lanes.highway NOT IN ('construction', 'proposed') THEN 'working'
                   ELSE osm_cycleway_lanes.highway
                END AS status
            FROM osm_administrative
                LEFT JOIN osm_cycleway_lanes
                ON osm_cycleway_lanes.geometry && ST_Envelope(osm_administrative.geometry)
        ) AS bounded
        WHERE bounded.osm_id IN (
            -1952636,
            -448930,
            -2692156,
            -421866,
            -1952636,
            -3678531,
            -3154746,
            -2171253,
            -1413957,
            -2175078,
            -3030976,
            -3030295,
            -2175078,
            -1418322,
            -1413934,
            -1017311,
            -1418311,
            -1641691,
            -2825507,
            -361818,
            -1792913,
            -3058686,
            -2362670,
            -2692232,
            -2032280,
            -3058686,
            -2825228
        ) AND bounded.osm_id IS NOT NULL
        GROUP BY bounded.osm_id, bounded.name, bounded.type, bounded.status
        ORDER BY bounded.name
    """)

    results = [tuple(result) for result in r]
    info = {}
    for k, g in groupby(results, itemgetter(0)):
        for v in g:
            if k not in info:
                info[k] = {
                    'name': v[0],
                    'length': {
                        'cycleway': {
                            'working': 0,
                            'proposed': 0,
                            'construction': 0,
                            'total': 0
                        },
                        'cyclefootway': {
                            'working': 0,
                            'proposed': 0,
                            'construction': 0,
                            'total': 0
                        },
                        'cyclelane': {
                            'working': 0,
                            'proposed': 0,
                            'construction': 0,
                            'total': 0
                        },
                        'total': 0
                    }
                }
            info[k]['length'][v[2]][v[1]] += v[3]
            info[k]['length'][v[2]]['total'] += v[3]
            info[k]['length']['total'] += v[3]

    return Response(json.dumps(list(info.values())), content_type='application/json')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)


