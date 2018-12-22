import pytest

from shpotipy.configuration import Configuration
from shpotipy.osa import Osa
from shpotipy.utils import run_osa_script, set_volume, _authenticate
from subprocess import check_output, CalledProcessError, STDOUT

# To run the tests that require authentication set
# Your client id and secret in Configuration


def _run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    output = check_output(cmd, shell=True, stderr=STDOUT).decode("utf-8")
    return output


@pytest.mark.skipif(
    not Configuration.client_id or not Configuration.client_secret, reason="Credentials needed to run this test"
)
class TestLogin(object):
    def test_login(self):
        Configuration.store_credentials()
        _authenticate()


class TestVolume(object):
    def test_set_volume(self):
        _run_cmd("spotipy vol set 42")
        assert run_osa_script(Osa.getvolume) == "42"

    def test_incorrect_volume(self):
        with pytest.raises(CalledProcessError):
            _run_cmd("spotipy vol set Beeblebrox")

    def test_increase_volume(self):
        set_volume(42)
        _run_cmd("spotipy vol up")
        assert run_osa_script(Osa.getvolume) == "52"
        set_volume(95)
        _run_cmd("spotipy vol up")
        assert run_osa_script(Osa.getvolume) == "100"

    def test_decrease_volume(self):
        set_volume(42)
        _run_cmd("spotipy vol down")
        assert run_osa_script(Osa.getvolume) == "32"
        set_volume(5)
        _run_cmd("spotipy vol down")
        assert run_osa_script(Osa.getvolume) == "0"


class TestPlaybackControls(object):
    """Test playback controls play, pause, next, prev, replay, pos"""

    def test_play(self):
        _run_cmd("spotipy play")
        result = run_osa_script(Osa.getstate)
        assert "playing" in result


@pytest.mark.skipif(
    not Configuration.client_id or not Configuration.client_secret, reason="Credentials needed to run this test"
)
class TestSearchPlay(object):
    def test_search_and_play_artist(self):
        artist_search = "passenger"
        _run_cmd(f"spotipy play artist {artist_search}")
        result = _run_cmd("spotipy status").lower()
        assert "playing" in result
        assert artist_search in result

    def test_search_and_play_album(self):
        album_search = "vagabond"
        _run_cmd(f"spotipy play album {album_search}")
        result = _run_cmd("spotipy status").lower()
        assert "playing" in result
        assert album_search in result

    def test_search_and_play_track(self):
        track_search = "scare away the dark"
        _run_cmd(f'spotipy play "{track_search}"')
        result = _run_cmd("spotipy status").lower()
        assert "playing" in result
        assert track_search in result

    def test_search_and_play_playlist(self):
        pass

    def test_search_and_play_uri(self):
        pass


def test_quit():
    _run_cmd("spotipy quit")


class TestShare(object):
    pass


class TestToggle(object):
    pass


class TestStatus(object):
    pass
