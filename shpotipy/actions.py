import pyperclip
from docopt import DocoptExit
from shpotipy.configuration import Configuration
from shpotipy.osa import Osa
from shpotipy.utils import (
    run_osa_script,
    search_and_play,
    set_volume,
    print_error,
    print_status,
    TRACKS_URL,
    _authenticate,
    SIGN_UP_URL,
)


def play(args):
    """
    Play current song if no additional parameters are given.
    Search and play otherwise.
    """
    if args["<query>"]:
        if args["album"]:
            album = search_and_play(play_type="album", query=args["<query>"])
            print_status(f"Playing album: {album}")
        elif args["artist"]:
            artist = search_and_play(play_type="artist", query=args["<query>"])
            print_status(f"Playing artist: {artist}")
        elif args["playlist"]:
            playlist = search_and_play(
                play_type="playlist", query=args["<query>"]
            )  # Todo: fix to only search for user playlist
            print_status(f"Playing playlist: {playlist}")
        elif args["uri"]:
            run_osa_script(Osa.playtrack.format(args["<query>"]))
            print_status(f"Playing uri: {args['uri']}")
        else:
            search_and_play(play_type="track", query=args["<query>"])

    else:
        run_osa_script(Osa.play)
        status()

def next_track(args):
    print_status("Playing next track")
    run_osa_script(Osa.playnexttrack)
    status()


def previous_track(args):
    print_status("Playing previous track")
    run_osa_script(Osa.playprevioustrack)
    status()


def replay(args):
    print_status("Playing track from the beginning")
    run_osa_script(Osa.playfromstart)
    status()


def pause(args):
    print_status("Pausing Spotify")
    run_osa_script(Osa.pause)


def quit_spotify(args):
    print_status("Quitting Spotify")
    run_osa_script(Osa.quit)


def vol(args):
    vol_step = 10

    if args["show"]:
        print_status(f"Volume: {run_osa_script(Osa.getvolume)}")

    elif args["up"]:
        volume = run_osa_script(Osa.getvolume)
        new_vol = min(int(volume) + vol_step, 100)
        set_volume(new_vol)
        print_status(f"Volume: {new_vol}")

    elif args["down"]:
        volume = run_osa_script(Osa.getvolume)
        new_vol = max(int(volume) - vol_step, 0)
        set_volume(new_vol)
        print_status(f"Volume: {new_vol}")

    elif args["set"]:
        try:
            volume = int(args["<amount>"])
        except ValueError:
            print_error("Volume value must be a number between 0 and 100")
            raise DocoptExit

        set_volume(volume)
        print_status(f'Volume: {args["<amount>"]}')


def status(args=None):
    status_info = run_osa_script(Osa.getstate)
    artist_info = run_osa_script(Osa.getartist)
    album_info = run_osa_script(Osa.getalbum)
    track_info = run_osa_script(Osa.gettrack)
    curr_pos, total_time = _get_position()

    print_status(f"Spotify is currently {status_info}")
    print(f"Artist: {artist_info}\n"
          f"Album: {album_info}\n"
          f"Track: {track_info}\n"
          f"Position: {curr_pos} / {total_time}\n")


def _get_position():
    return run_osa_script(Osa.getposition), run_osa_script(Osa.getduration)


def share(args):
    uri = run_osa_script(Osa.geturi)

    if args["uri"]:
        pyperclip.copy(uri)
        print_status(f"Song URI: {uri} copied to clipboard")

    elif args["url"]:
        song_uri = uri.split(":")[2]
        url = TRACKS_URL + song_uri
        pyperclip.copy(url)
        print_status(f"Song URL: {url} copied to clipboard")


def toggle_shuffle(args):
    run_osa_script(Osa.noshuffle)
    shuffle_enabled = run_osa_script(Osa.shuffle) == "true"
    shuffle_status = "enabled" if shuffle_enabled else "disabled"
    print_status(f"Shuffle mode {shuffle_status}")


def toggle_repeat(args):
    run_osa_script(Osa.norepeat)
    repeat_enabled = run_osa_script(Osa.repeat) == "true"
    repeat_status = "enabled" if repeat_enabled else "disabled"
    print_status(f"Repeat mode {repeat_status}")


def login_wizard(args):
    print_status(f"Please get your credentials from {SIGN_UP_URL}")
    Configuration.client_id = input("Insert your client id: ")
    Configuration.client_secret = input("Insert your client secret: ")
    Configuration.store_credentials()
    _authenticate()
    print_status("Credentials stored successfully, try playing something")
