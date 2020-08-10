import logging
import os
import subprocess

import mercantile
import argparse

xmin, ymin, xmax, ymax = 22.0856083513, 44.3614785833, 40.0807890155, 52.3350745713

DATA_DIR = '/var/import/'


def prerender(xmin, ymin, xmax, ymax, min_zoom, max_zoom):
    for z in range(min_zoom, max_zoom):
        min_t = mercantile.tile(xmin, ymin, z)
        max_t = mercantile.tile(xmax, ymax, z)

        cmd = f'render_list -m ajt -a -z {z} -Z {z} -n 10 ' \
              f'--min-x={min_t.x} --min-y={max_t.y} ' \
              f'--max-x={max_t.x} --max-y={min_t.y} ' \
              f'--tile-dir /var/run/renderd/mod_tile ' \
              f'-m osm'
        logging.info('Running `%s`', cmd)
        subprocess.run(cmd, shell=True, check=True)


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
    render = subparsers.add_parser('prerender')
    render.add_argument('--lat_min', default=44.3614785833, type=float)
    render.add_argument('--lng_min', default=22.0856083513, type=float)
    render.add_argument('--lat_max', default=52.3350745713, type=float)
    render.add_argument('--lng_max', default=40.0807890155, type=float)

    render.add_argument('--min-zoom', default=1, type=int)
    render.add_argument('--max-zoom', default=16, type=int)

    load = subparsers.add_parser('import')
    load.add_argument('-f', '--file', choices=[
        f for f in os.listdir(DATA_DIR)
        if f not in ('.gitkeep',)
    ], nargs='+', dest='files', required=True)

    args = parser.parse_args()

    if args.command == 'prerender':
        prerender(
            xmin=args.lng_min,
            ymin=args.lat_min,
            xmax=args.lng_max,
            ymax=args.lat_max,
            min_zoom=args.min_zoom,
            max_zoom=args.max_zoom
        )
    elif args.command == 'import':
        import_data_to_db(args.files)
    else:
        parser.print_help()
