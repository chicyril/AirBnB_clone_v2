#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, and distribute the archive to the
servers declared in env.hosts.
"""
from fabric.api import local, run, put, env
from datetime import datetime
from os.path import isdir, getsize, exists, basename, splitext
from os import mkdir
env.hosts = ['52.86.157.4', '100.25.14.58']
do_pack_run = False
archive_path = ""


def do_pack():
    """Fabric task for generating .tgz from the contents of
    web_static dir.
    """
    global do_pack_run
    global archive_path
    if do_pack_run:
        return archive_path
    try:
        if not isdir("versions"):
            mkdir("versions")
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{date_str}.tgz"
        print(f"Packing web_static to {archive_path}")
        local(f"tar -czvf {archive_path} web_static/*")
        size = getsize(archive_path)
        print(f'web_static packed: {archive_path} -> {size}Bytes')
        do_pack_run = True
        return archive_path
    except Exception as e:
        print("Error occured: ", e)
        return None


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


def deploy():
    """Function that calls other functions to perform the task."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
