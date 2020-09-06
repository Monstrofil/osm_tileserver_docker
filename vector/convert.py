import yaml
import toml

mvt_providers = {}
layers = []

with open('openmaptiles.yaml') as f:
    data = yaml.load(f)

for layer in data['Layer']:
    layer_source = layer['Datasource']
    source_name = layer_source['dbname']
    if source_name not in mvt_providers:
        mvt_providers[source_name] = dict(
            name='openmaptiles',
            type="postgis",
            host=layer_source['host'],
            port=layer_source['port'],
            database=layer_source['dbname'],
            user=layer_source['user'],
            password=layer_source['password'],
            srid=3857 if layer_source['srid'] == 900913 else layer_source['srid'],
        )

    layers.append(dict(
        name=layer['id'],
        geometry_fieldname='geometry',
        geometry_type="linestring",
        id_fieldname="id_field",
        sql='SELECT * FROM ' + layer_source['table'].replace(
            layer_source['geometry_field'],
            f'ST_AsMVTGeom({layer_source["geometry_field"]}, !BBOX!) AS geometry, 1 AS id_field'
        )
    ))
    print(layer['id'])

assert len(mvt_providers) == 1
print(toml.dumps({
    'mvt_providers': {
        # **list(mvt_providers.values())[0],
        'layers': layers
    },
    'maps': [{
        'name': 'openmaptiles',
        'layers': [dict(
            provider_layer=f"mvt_openmaptiles.{layer['name']}",
            min_zoom=data['minzoom'],
            max_zoom=data['maxzoom']
        ) for layer in layers]
    }]
}))

