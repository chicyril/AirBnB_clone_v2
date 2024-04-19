#!/usr/bin/python3
"""This module contains a fabric(1.14) task that deletes out of date versions.
"""
from os import listdir
from fabric.api import lcd, local, cd, run, env

HOSTS = ['52.86.157.4', '100.25.14.58']


def do_clean(number=0):
    """Delete out-of-date archives locally and remote.
    """
    number = 1 if int(number) <= 1 else int(number)

    with lcd('versions'):
        old_archives = sorted(listdir("versions"))[:-number]
        to_rm = ' '.join(old_archives)
        local(f'rm -f {to_rm}')

    with cd('/data/web_static/releases'):
        for host in HOSTS:
            env.host_string = host
            old_releases = ([version for version in run("ls -tr").split()
                            if 'web_static' in version][:-number])
            to_rm = ' '.join(old_releases)
            run(f'rm -rf {to_rm}')
