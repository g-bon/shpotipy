from __future__ import (print_function, unicode_literals, division, absolute_import)
from builtins import open
from future import standard_library
standard_library.install_aliases()

import json
import pickle
import requests
from requests.auth import HTTPBasicAuth
from subprocess import Popen, PIPE
from time import sleep
from osa import Osa
from configuration import Configuration
from termcolor import colored
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


def authenticate():
    response = requests.post(AUTH_URL,
                             auth=HTTPBasicAuth(Configuration.client_id, Configuration.client_secret),
                             data=AUTH_BODY)

    Configuration.auth_token = response.json().get("access_token", None)
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(Configuration.auth_token, f)


def search(search_type, query):
    if not Configuration.client_id or not Configuration.client_secret:
        try:
            with open(Configuration.credentials_file, 'rb') as f:
                Configuration.client_id, Configuration.client_secret = pickle.load(f)

        except IOError:
            print_error("Credentials missing, to perform this operation "
                        "set up your credentials calling shpotipy login")
            raise DocoptExit

    if not Configuration.auth_token:
        try:
            with open(TOKEN_FILE, 'rb') as f:
                Configuration.auth_token = pickle.load(f)

        except IOError:
            authenticate()

    search_URL = SEARCH_BASE_URL.format(query, search_type)
    headers = {'Authorization': "Bearer {}".format(Configuration.auth_token)}
    response = requests.get(search_URL, headers=headers)

    # if status code wrong re-authenticate
    if response.status_code == 200:
        return response
    else:
        authenticate()
        return requests.get(search_URL, headers=headers)


def search_and_play(type='track', query=None):
    assert type is None or type in ['track', 'album', 'artist', 'playlist', 'uri']
    response = search(type, query)
    items = json.loads(response.content)[type + "s"]["items"]  # terrible hack
    if len(items) is not 0:
        songURI = items[0]['uri']
        run_osa_script(Osa.playtrack.format(songURI))
        return items[0]
    return None


# Use brighter colors and bold
def print_status(msg):
    print(colored(msg, "green"))


def print_message(msg):
    print(colored(msg, "cyan"))


def print_warning(msg):
    print(colored(msg, "yellow"))


def print_error(msg):
    print(colored(msg, "red"))