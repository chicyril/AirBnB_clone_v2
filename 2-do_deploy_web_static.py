#!/usr/bin/python3
"""Fabric script that distributes an archive to web-servers."""
from fabric.api import run, put, env
from os.path import exists, basename, splitext
env.hosts = ['52.86.157.4', '100.25.14.58']


def do_deploy(archive_path):
    """Deploy an archive to web-servers."""
    if not exists(archive_path):
        return False
    try:
        archive = basename(archive_path)
        dir_name = splitext(archive)[0]
        remote_location = f'/data/web_static/releases/{dir_name}'
        put(archive_path, f"/tmp/{archive}")
        run(f'mkdir -p {remote_location}')
        run(f'tar -xzf /tmp/{archive} -C {remote_location}')
        run(f'mv {remote_location}/web_static/* {remote_location}')
        run(f'rm -rf {remote_location}/web_static/')
        run(f'rm /tmp/{archive}')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {remote_location} /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception as e:
        print("Error: ", e)
        return False
