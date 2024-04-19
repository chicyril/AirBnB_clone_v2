#!/usr/bin/python3
"""Fabric (v1.14) script that distributes an archive to web-servers."""

from os.path import isfile, basename, splitext
from fabric.api import run, put, env

env.hosts = ['52.86.157.4', '100.25.14.58']


def do_deploy(archive_path):
    """Deploy an archive to web-servers."""

    if not isfile(archive_path):
        return False

    archive = basename(archive_path)
    dir_name = splitext(archive)[0]
    remote_location = f'/data/web_static/releases/{dir_name}'

    statements = [
        f'{archive_path};/tmp/',
        f'mkdir -p {remote_location}',
        f'tar -xzf /tmp/{archive} -C {remote_location} --strip-components=1',
        f'rm -rf /tmp/{archive} /data/web_static/current',
        f'ln -sf {remote_location}/ /data/web_static/current'
    ]

    for statement in statements:
        if statement == statements[0]:
            local_path, remote_path = statement.split(';')
            result = put(local_path, remote_path)
        else:
            result = run(statement)

        if result.failed:
            return False

    print('New version deployed!')
    return True
