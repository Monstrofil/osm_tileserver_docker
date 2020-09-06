#!/usr/bin/env python3
import logging
import os
import shutil
import subprocess

import argparse

DATA_DIR = '/import/'
DIFFDIR = '/diffdir/'


def import_data_to_db(filename):
    shutil.rmtree(DIFFDIR, ignore_errors=True)

    cmd = [
        './imposm', 'import', '-appendcache',
        '-diff',
        '-diffdir', DIFFDIR,
        '-cachedir', DIFFDIR,
        '-connection',
        f"postgis://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}",
        '-write', '-mapping', '/config/mapping.yml',
        '-read', os.path.join(DATA_DIR, filename),
        '-deployproduction'
    ]
    subprocess.call(cmd, env={**os.environ})


def update_db():
    cmd = [
        './imposm', 'run',
        '-diffdir', DIFFDIR,
        '-cachedir', DIFFDIR,
        '-connection',
        f"postgis://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}",
        '-mapping', '/config/mapping.yml',
    ]
    subprocess.call(cmd, env={**os.environ})


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    load = subparsers.add_parser('import')
    load.add_argument('-f', '--file', choices=[
        f for f in os.listdir(DATA_DIR)
        if f not in ('.gitkeep',)
    ], dest='files', required=True)

    update = subparsers.add_parser('update')

    args = parser.parse_args()

    if args.command == 'import':
        import_data_to_db(args.files)
    elif args.command == 'update':
        update_db()
    else:
        parser.print_help()
