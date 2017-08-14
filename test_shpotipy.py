# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import pytest

"""
Shpotipy.


Usage:
    shpotipy play [(album | artist | playlist | uri) <query>]
    shpotipy next
    shpotipy prev
    shpotipy replay
    shpotipy pos [<time>]
    shpotipy pause
    shpotipy quit
    shpotipy vol [show | up | down | set <amount>]
    shpotipy status
    shpotipy share
    shpotipy share url
    shpotipy share uri
    shpotipy toggle shuffle
    shpotipy toggle repeat
"""


def test_no_parameters():
    """An example test."""
    result = None
    try:
        result = run_cmd("python shpotipy.py")
    except CalledProcessError:
        pass
    assert result == __doc__


def test_play():
    run_cmd("python shpotipy.py play")
    result = run_cmd("python shpotipy.py status")
    "spotify is currently playing" in result


def run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    return check_output(cmd, shell=True).decode('utf-8')
