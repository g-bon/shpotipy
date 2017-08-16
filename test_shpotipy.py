# -*- coding: utf-8 -*-
from __future__ import (print_function, unicode_literals, division, absolute_import)
from future import standard_library
standard_library.install_aliases()
from subprocess import check_output, CalledProcessError, STDOUT
from utils import run_osa_script, set_volume
from osa import Osa
import pytest


def _run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    output = check_output(cmd, shell=True, stderr=STDOUT).decode('utf-8')
    return output


class TestPlaybackControls(object):
    """Test playback controls play, pause, next, prev, replay, pos"""
    def test_play(self):
        _run_cmd("python shpotipy.py play")
        result = run_osa_script(Osa.getstate)
        assert "playing" in result


class TestSearchPlay(object):
    def test_search_and_play_artist(self):
        artist_search = "passenger"
        _run_cmd("python shpotipy.py play artist {}".format(artist_search))
        result = _run_cmd("python shpotipy.py status").lower()
        assert "playing" in result
        assert artist_search in result

    def test_search_and_play_album(self):
        album_search = "vagabond"
        _run_cmd("python shpotipy.py play album {}".format(album_search))
        result = _run_cmd("python shpotipy.py status").lower()
        assert "playing" in result
        assert album_search in result

    def test_search_and_play_track(self):
        track_search = "scare away the dark"
        _run_cmd('python shpotipy.py play "{}"'.format(track_search))
        result = _run_cmd("python shpotipy.py status").lower()
        assert "playing" in result
        assert track_search in result

    def test_search_and_play_playlist(self):
        pass

    def test_search_and_play_uri(self):
        pass


class TestVolume(object):
    def test_set_volume(self):
        _run_cmd("python shpotipy.py vol set 42")
        assert run_osa_script(Osa.getvolume) == "42"

    def test_incorrect_volume(self):
        with pytest.raises(CalledProcessError):
            _run_cmd("python shpotipy.py vol set Beeblebrox")

    def test_increase_volume(self):
        set_volume(42)
        _run_cmd("python shpotipy.py vol up")
        assert run_osa_script(Osa.getvolume) == "52"
        set_volume(95)
        _run_cmd("python shpotipy.py vol up")
        assert run_osa_script(Osa.getvolume) == "100"

    def test_decrease_volume(self):
        set_volume(42)
        _run_cmd("python shpotipy.py vol down")
        assert run_osa_script(Osa.getvolume) == "32"


def test_quit():
    _run_cmd("python shpotipy.py quit")


class TestShare(object):
    pass


class TestToggle(object):
    pass


class TestStatus(object):
    pass

# shpotipy play [(album | artist | playlist | uri) <query>]
# shpotipy next
# shpotipy prev
# shpotipy replay
# shpotipy pos [<time>]
# shpotipy pause
# shpotipy quit
# shpotipy vol [show | up | down | set <amount>]
# shpotipy status
# shpotipy share
# shpotipy share url
# shpotipy share uri
# shpotipy toggle shuffle
# shpotipy toggle repeat
