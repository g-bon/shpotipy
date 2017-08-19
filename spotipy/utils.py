from __future__ import (print_function, unicode_literals, division, absolute_import)
from future import standard_library
standard_library.install_aliases()

import json
import requests
import colored
from requests.auth import HTTPBasicAuth
from subprocess import Popen, PIPE
from time import sleep
from osa import Osa
from configuration import Configuration
from docopt import DocoptExit


SIGN_UP_URL = "https://developer.spotify.com/"
TRACKS_URL = "http://open.spotify.com/track/"
AUTH_URL = "https://accounts.spotify.com/api/token"
AUTH_BODY = {'grant_type': 'client_credentials'}
SEARCH_BASE_URL = "https://api.spotify.com/v1/search?q={}&type={}"
TOKEN_FILE = "token.pickle"


def activate():
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(Osa.checkrunning)
    active = "true" in stdout
    if not active:
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        p.communicate(Osa.activate)
        sleep(2)


def run_osa_script(script):
    activate()
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    return stdout.strip()


def _authenticate():
    response = requests.post(AUTH_URL,
                             auth=HTTPBasicAuth(Configuration.client_id, Configuration.client_secret),
                             data=AUTH_BODY)

    if response.status_code == 200:
        Configuration.auth_token = response.json().get("access_token", None)
        print_status("Success.")
        Configuration.store_token()
    else:
        print_error("Authentication failed, try to re-insert id and secret with \"spotipy login\"")
        raise DocoptExit


def _authenticate_with_credentials():
    if not Configuration.client_id or not Configuration.client_secret:
        try:
            print_error("No stored token, trying to obtain a new one...")
            Configuration.load_credentials()
            _authenticate()
        except IOError:
            print_error("Credentials missing, to perform this operation "
                        "set up your credentials calling \"spotipy login\"")
            raise DocoptExit


def search(search_type, query):
    if not Configuration.auth_token:  # always True in normal use, handy for dev
        try:
            Configuration.load_token()
        except IOError:
            _authenticate_with_credentials()

    search_URL = SEARCH_BASE_URL.format(query, search_type)
    headers = {'Authorization': "Bearer {}".format(Configuration.auth_token)}
    response = requests.get(search_URL, headers=headers)

    # if status code wrong re-authenticate
    if response.status_code == 200:
        return response
    else:
        _authenticate_with_credentials()
        response = requests.get(search_URL, headers=headers)
        if response.status_code == 200:
            return response
        else:
            print_error("Authentication failed, try to re-insert id and secret with \"spotipy login\"")
            raise DocoptExit


def search_and_play(type='track', query=None):
    assert type is None or type in ['track', 'album', 'artist', 'playlist']
    response = search(type, query)
    response_json = json.loads(response.text)
    if response.status_code in [200]:
        items = response_json[type + "s"]["items"]  # terrible hack
        if len(items) is not 0:
            songURI = items[0]['uri']
            run_osa_script(Osa.playtrack.format(songURI))
            return items[0]['name']
    else:
        print_error("Spotify search API answered with error: {}.".format(response_json['error']['message']))
        raise DocoptExit


def set_volume(volume):
    if 0 <= volume <= 100:
        # Fix weird spotify behavior when setting volume
        volume = volume if volume == 100 else volume + 1
        run_osa_script(Osa.setvolume.format(str(volume)))
    else:
        print_error("Volume value must be a number between 0 and 100")
        raise DocoptExit


status_style = colored.fg(119) + colored.attr("bold")
message_style = colored.fg("cyan") + colored.attr("bold")
warning_style = colored.fg("yellow") + colored.attr("bold")
error_style = colored.fg("red") + colored.attr("bold")


def print_status(msg):
    print(colored.stylize(msg, status_style))


def print_message(msg):
    print(colored.stylize(msg, message_style))


def print_warning(msg):
    print(colored.stylize(msg, warning_style))


def print_error(msg):
    print(colored.stylize(msg, error_style))
