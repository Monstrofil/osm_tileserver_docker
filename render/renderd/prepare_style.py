import argparse
import sys

from ruamel.yaml import YAML


def update_template(path):
    yaml = YAML()  # default, if not specfied, is 'rt' (round-trip)
    data = yaml.load(open(path))

    data['_parts']['osm2pgsql']['host'] = '${PG_HOSTNAME}'
    data['_parts']['osm2pgsql']['dbname'] = '${PG_DBNAME}'
    data['_parts']['osm2pgsql']['user'] = '${PG_USERNAME}'
    data['_parts']['osm2pgsql']['password'] = '${PG_PASSWORD}'

    yaml.dump(data, open(path, 'w'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--style-file', required=True)

    args = parser.parse_args()
    update_template(args.style_file)
