# -*- coding: utf-8 -*-
from __future__ import (print_function, unicode_literals, division, absolute_import)
from future import standard_library


standard_library.install_aliases()

import pytest
from shpotipy.osa import Osa
from shpotipy.utils import run_osa_script, set_volume
from subprocess import check_output, CalledProcessError, STDOUT


def _run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    output = check_output(cmd, shell=True, stderr=STDOUT).decode('utf-8')
    return output


class TestVolume(object):
    def test_set_volume(self):
        _run_cmd("shpotipy vol set 42")
        assert run_osa_script(Osa.getvolume) == "42"

    def test_incorrect_volume(self):
        with pytest.raises(CalledProcessError):
            _run_cmd("shpotipy vol set Beeblebrox")

    def test_increase_volume(self):
        set_volume(42)
        _run_cmd("shpotipy vol up")
        assert run_osa_script(Osa.getvolume) == "52"
        set_volume(95)
        _run_cmd("shpotipy vol up")
        assert run_osa_script(Osa.getvolume) == "100"

    def test_decrease_volume(self):
        set_volume(42)
        _run_cmd("shpotipy vol down")
        assert run_osa_script(Osa.getvolume) == "32"
        set_volume(5)
        _run_cmd("shpotipy vol down")
        assert run_osa_script(Osa.getvolume) == "0"


class TestPlaybackControls(object):
    """Test playback controls play, pause, next, prev, replay, pos"""
    def test_play(self):
        _run_cmd("shpotipy play")
        result = run_osa_script(Osa.getstate)
        assert "playing" in result


class TestSearchPlay(object):
    def test_search_and_play_artist(self):
        artist_search = "passenger"
        _run_cmd("shpotipy play artist {}".format(artist_search))
        result = _run_cmd("shpotipy status").lower()
        assert "playing" in result
        assert artist_search in result

    def test_search_and_play_album(self):
        album_search = "vagabond"
        _run_cmd("shpotipy play album {}".format(album_search))
        result = _run_cmd("shpotipy status").lower()
        assert "playing" in result
        assert album_search in result

    def test_search_and_play_track(self):
        track_search = "scare away the dark"
        _run_cmd('shpotipy play "{}"'.format(track_search))
        result = _run_cmd("shpotipy status").lower()
        assert "playing" in result
        assert track_search in result

    def test_search_and_play_playlist(self):
        pass

    def test_search_and_play_uri(self):
        pass


def test_quit():
    _run_cmd("shpotipy quit")


class TestShare(object):
    pass


class TestToggle(object):
    pass


class TestStatus(object):
    pass
