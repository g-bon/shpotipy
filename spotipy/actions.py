import pyperclip
from builtins import (input, int)
from docopt import DocoptExit
from configuration import Configuration
from osa import Osa
from utils import (run_osa_script, search_and_play, set_volume, print_error,
                            print_status, TRACKS_URL, authenticate, SIGN_UP_URL)


def play(args):
    """
    Play current song if no additional parameters are given.
    Search and play otherwise.
    """
    if args['<query>']:
        if args['album']:
            search_and_play(type='album', query=args['<query>'])
        elif args['artist']:
            search_and_play(type='artist', query=args['<query>'])
        elif args['playlist']:
            search_and_play(type='playlist', query=args['<query>'])  # Todo: fix to only search for user playlist
        elif args['uri']:
            run_osa_script(Osa.playtrack.format(args['<query>']))
        else:
            search_and_play(type='track', query=args['<query>'])

    else:
        run_osa_script(Osa.play)


def next_track(args):
    run_osa_script(Osa.playnexttrack)


def previous_track(args):
    run_osa_script(Osa.playprevioustrack)


def replay(args):
    run_osa_script(Osa.playfromstart)


def pause(args):
    print_status("Pausing Spotify")
    run_osa_script(Osa.pause)


def quit_spotify(args):
    run_osa_script(Osa.quit)


def vol(args):
    vol_step = 10

    if args['show']:
        print("Volume: {}".format(run_osa_script(Osa.getvolume)))

    elif args['up']:
        volume = run_osa_script(Osa.getvolume)
        new_vol = min(int(volume) + vol_step, 100)
        set_volume(new_vol)
        print("Volume: {}".format(new_vol))

    elif args['down']:
        volume = run_osa_script(Osa.getvolume)
        new_vol = max(int(volume) - vol_step, 0)
        set_volume(new_vol)
        print("Volume: {}".format(new_vol))

    elif args['set']:
        try:
            volume = int(args['<amount>'])
        except ValueError:
            print_error("Volume value must be a number between 0 and 100")
            raise DocoptExit

        set_volume(volume)
        print("Volume: {}".format(args['<amount>']))


def status(args=None):
    status_info = run_osa_script(Osa.getstate)
    artist_info = run_osa_script(Osa.getartist)
    album_info = run_osa_script(Osa.getalbum)
    track_info = run_osa_script(Osa.gettrack)
    curr_pos, total_time = _get_position()

    print_status("Spotify is currently {}".format(status_info))
    print("Artist: {}\nAlbum: {}\nTrack: {}\nPosition: {} / {}\n"
          .format(artist_info, album_info, track_info, curr_pos, total_time))


def _get_position():
    return run_osa_script(Osa.getposition), run_osa_script(Osa.getduration)


def share(args):
    uri = run_osa_script(Osa.geturi)

    if args['uri']:
        pyperclip.copy(uri)

    elif args['url']:
        song_uri = uri.split(':')[2]
        url = TRACKS_URL + song_uri
        pyperclip.copy(url)


def toggle_shuffle(args):
    run_osa_script(Osa.noshuffle)
    shuffle_enabled = run_osa_script(Osa.shuffle) == 'true'
    shuffle_status = "enabled" if shuffle_enabled else "disabled"
    print_status("Shuffle mode {}".format(shuffle_status))


def toggle_repeat(args):
    run_osa_script(Osa.norepeat)
    repeat_enabled = run_osa_script(Osa.repeat) == 'true'
    repeat_status = "enabled" if repeat_enabled else "disabled"
    print_status("Repeat mode {}".format(repeat_status))


def login_wizard(args):
    print("Please get your credentials from {}".format(SIGN_UP_URL))
    Configuration.client_id = input("Insert your client id: ")
    Configuration.client_secret = input("Insert your client secret: ")
    Configuration.store_credentials()
    authenticate()
    print("Credentials stored successfully, try playing something")
