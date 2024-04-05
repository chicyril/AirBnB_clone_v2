#!/usr/bin/python3
"""Fabric (v1.14) script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, and distribute the archive to the
servers declared in env.hosts.
"""

from os import mkdir
from os.path import isdir, isfile, getsize, basename, splitext
from datetime import datetime
from fabric.api import local, run, put, env

# env.host = ['52.86.157.4', '100.25.14.58']
# DONE_DO_PACK = False
# ARCHIVE_PATH = ""
HOSTS = ['52.86.157.4', '100.25.14.58']


def do_pack():
    """Subtask for generating .tgz from the contents of
    web_static dir.
    """

    if not isdir("versions"):
        mkdir("versions")
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{date_str}.tgz"

    print(f"Packing web_static to {archive_path}")
    if local(f"tar -czvf {archive_path} web_static/*").failed:
        return None

    size = getsize(archive_path)
    print(f'web_static packed: {archive_path} -> {size}Bytes')
    return archive_path


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
        f'rm /tmp/{archive}',
        'rm -rf /data/web_static/current',
        f'ln -sf {remote_location}/ /data/web_static/current'
    ]

    for statement in statements:
        if statement == statements[0]:
            local, remote = statement.split(';')
            result = put(local, remote)
        else:
            result = run(statement)
        if result.failed:
            return False

    print('New version deployed!')
    return True


def deploy():
    """Fab task that calls other task to perform the deploy op."""

    # global DONE_DO_PACK
    # global ARCHIVE_PATH

    # if not DONE_DO_PACK:
    #     ARCHIVE_PATH = do_pack()
    #     DONE_DO_PACK = True

    # if ARCHIVE_PATH:
    #     return do_deploy(ARCHIVE_PATH)
    # return False

    archive_path = do_pack()
    if not archive_path:
        return False

    for host in HOSTS:
        env.host_string = host
        print(f"[{host}] Executing task \'{env.command}\'")
        if not do_deploy(archive_path):
            return False
    return True
