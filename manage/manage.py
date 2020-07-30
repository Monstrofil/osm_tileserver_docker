#!/usr/bin/env python3
import argparse
import os
import subprocess

DATA_DIR = '/var/import/'


def import_data_to_db(files):

    for filename in files:
        cmd = [
            'osm2pgsql',
            '-d', os.environ['POSTGRES_DB'],
            '-U', os.environ['POSTGRES_USER'],
            '-H', os.environ['POSTGRES_HOST'],
            '-W',
            '--create', '--slim', '-G', '--hstore',
            '--tag-transform-script', '/openstreetmap-carto/openstreetmap-carto.lua',
            '-S', '/openstreetmap-carto/openstreetmap-carto.style',
            '--number-processes', str(os.cpu_count()),
            os.path.join(DATA_DIR, filename)
        ]
        subprocess.call(
            cmd, env={**os.environ, 'PGPASSWORD': os.environ['POSTGRES_PASSWORD']},
            stdin=subprocess.DEVNULL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    imp = subparsers.add_parser('import')
    imp.add_argument('-f', '--file', choices=[
        f for f in os.listdir(DATA_DIR)
        if f not in ('.gitkeep', )
    ], nargs='+', dest='files')

    args = parser.parse_args()

    if args.command == 'import':
        import_data_to_db(args.files)
    else:
        parser.print_help()
