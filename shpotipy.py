import json
import requests
from requests.auth import HTTPBasicAuth
from configurations import client_id, client_secret
from subprocess import Popen, PIPE

body = {'grant_type': 'client_credentials'}
authUrl = "https://accounts.spotify.com/api/token"


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class Shpotipy:
    def __init__(self):
        self.authToken = self.authenticate(client_id, client_secret)

    def authenticate(self, usr, pwd):
        response = requests.post(authUrl, auth=HTTPBasicAuth(usr, pwd), data=body)
        return response.json().get("access_token", None)


    def set_client_id(self, client_id):
        pass


    def set_client_secret(self, client_secret):
        pass

    def search_and_play(self, type='track', query=None):
        assert type is None or type in ['track', 'album', 'artist', 'list', 'uri']
        searchUrl = "https://api.spotify.com/v1/search?q={}&type={}".format(query, type)
        headers = {'Authorization': "Bearer {}".format(self.authToken)}
        response = requests.get(searchUrl, headers=headers)
        items = json.loads(response.content)["tracks"]["items"]
        if len(items) is not 0:
            songURI = items[0]['uri']
            self.run_osa_script(Commands.playtrack.format(songURI))
            return items[0]
        return None

    def get_state(self):
        returncode, state, stderr = self.run_osa_script(Commands.getstate)
        print("Spotify is currently {}".format(state))


    def get_artist(self):
        returncode, artist, stderr = self.run_osa_script(Commands.getartist)
        print("Artist: {}".format(artist))


    def get_album(self):
        returncode, album, stderr = self.run_osa_script(Commands.getalbum)
        print("Album: {}".format(album))


    def get_track(self):
        returncode, track, stderr = self.run_osa_script(Commands.gettrack)
        print("Track: {}".format(track))


    def get_duration(self):
        returncode, duration, stderr = self.run_osa_script(Commands.getduration)
        return duration


    def get_position(self):
        returncode, position, stderr = self.run_osa_script(Commands.getposition)
        return position

    def play_pause(self):
        print("PlayPausing")
        self.run_osa_script(Commands.playpause)


    def show_complete_status(self):
        self.get_state()
        self.get_artist()
        self.get_album()
        self.get_track()
        print("Position: {} / {}".format(self.get_position(), self.get_duration()))


    def run_osa_script(self, script):
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        return p.returncode, stdout.strip(), stderr


    def showHelp(self):
        pass


    def getStatus(self):
        pass


class Commands:
    getstate = 'tell application "Spotify" to player state as string'
    getartist = 'tell application "Spotify" to artist of current track as string'
    getalbum = 'tell application "Spotify" to album of current track as string'
    gettrack = 'tell application "Spotify" to name of current track as string'
    playtrack = 'tell application "Spotify" to play track "{}"'
    activate = 'tell application "Spotify" to activate'
    play = 'tell application "Spotify" to play'
    state = 'tell application "Spotify" to player state as string'
    playpause = 'tell application "Spotify" to playpause'
    quit = 'tell application "Spotify" to quit'
    nexttrack = 'tell application "Spotify" to next track'
    playfromstart = 'tell application "Spotify" to set player position to 0'
    setvolume = 'tell application "Spotify" to set sound volume to {}'
    noshuffle = 'tell application "Spotify" to set shuffling to not shuffling'
    shuffle = 'tell application "Spotify" to shuffling'
    norepeat = 'tell application "Spotify" to set repeating to not repeating'
    repeat = 'tell application "Spotify" to repeating'
    getduration = '''
            tell application "Spotify"
            set durSec to (duration of current track / 1000) as text
            set tM to (round (durSec / 60) rounding down) as text
            if length of ((durSec mod 60 div 1) as text) is greater than 1 then
                set tS to (durSec mod 60 div 1) as text
            else
                set tS to ("0" & (durSec mod 60 div 1)) as text
            end if
            set myTime to tM as text & ":" & tS as text
            end tell
    '''
    getposition = '''
            tell application "Spotify"
            set pos to player position
            set nM to (round (pos / 60) rounding down) as text
            if length of ((round (pos mod 60) rounding down) as text) is greater than 1 then
                set nS to (round (pos mod 60) rounding down) as text
            else
                set nS to ("0" & (round (pos mod 60) rounding down)) as text
            end if
            set nowAt to nM as text & ":" & nS as text
            end tell
    '''


if __name__ == "__main__":
    shpotipy = Shpotipy()
    song = shpotipy.search_and_play('track', "stu larsen chicago")
