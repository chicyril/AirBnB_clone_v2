#!./.venv/bin/python
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, using the function do_pack.
"""

from os import mkdir
from os.path import isdir, getsize
from datetime import datetime
from fabric.api import local


def do_pack():
    """Subtask for generating .tgz from the contents of
    web_static dir.
    """

    if not isdir('versions'):
        mkdir('versions')
    date_str = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = f'versions/web_static_{date_str}.tgz'

    print(f'Packing web_static to {archive_path}')
    if local(f'tar -czvf {archive_path} web_static/*').failed:
        return None

    size = getsize(archive_path)
    print(f'web_static packed: {archive_path} -> {size}Bytes')
    return archive_path
