#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime
from os.path import isdir, getsize
from os import mkdir


def do_pack():
    """Fabric task for generating .tgz from the contents of
    web_static dir.
    """
    if not isdir("versions"):
        mkdir("versions")
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{date_str}.tgz"
    print(f"Packing web_static to {archive_path}")
    local(f"tar -czvf {archive_path} web_static/*")
    size = getsize(archive_path)
    print(f'web_static packed: {archive_path} -> {size}Bytes')
