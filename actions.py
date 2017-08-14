from docopt import DocoptExit
from termcolor import colored
from utils import search_and_play, run_osa_script
from osa import Osa


def play(args):
    # shpotipy play [(album | artist | list | uri) <query>]
    if args['<query>']:
        if args['album']:
            search_and_play(type='album', query=args['<query>'])
        elif args['artist']:
            search_and_play(type='artist', query=args['<query>'])
        elif args['playlist']:
            search_and_play(type='playlist', query=args['<query>'])  # da sistemare perche non prende playlist utente
        elif args['uri']:
            run_osa_script(Osa.playtrack.format(args['<query>']))
        else:
            search_and_play(type='track', query=args['<query>'])

    else:
        run_osa_script(Osa.play)


def status(args=None):
    print("Spotify is currently {}".format(run_osa_script(Osa.getstate)))
    print("Artist: {}".format(run_osa_script(Osa.getartist)))
    print("Album: {}".format(run_osa_script(Osa.getalbum)))
    print("Track: {}".format(run_osa_script(Osa.gettrack)))
    pos()


def next_track(args):
    run_osa_script(Osa.playnexttrack)


def previous_track(args):
    run_osa_script(Osa.playprevioustrack)


def replay(args):
    run_osa_script(Osa.playfromstart)


def pos(args=None):
    print("Position: {} / {}".format(run_osa_script(Osa.getposition), run_osa_script(Osa.getduration)))


def pause(args):
    run_osa_script(Osa.pause)


def quit_spotify(args):
    run_osa_script(Osa.quit)


def vol(args):
    vol_step = 10

    if args['show']:
        print(run_osa_script(Osa.getvolume))

    elif args['up']:
        vol = run_osa_script(Osa.getvolume)
        run_osa_script(Osa.setvolume.format(int(vol) + vol_step))
        print("Volume: {}".format(int(vol) + vol_step))

    elif args['down']:
        vol = run_osa_script(Osa.getvolume)
        run_osa_script(Osa.setvolume.format(int(vol) - vol_step))
        print("Volume: {}".format(int(vol) - vol_step))

    elif args['set']:
        try:
            vol = int(args['<amount>'])
        except ValueError:
            print(colored("Volume value must be a number between 0 and 100", "red"))
            raise DocoptExit
        if 0 <= vol <= 100:
            run_osa_script(Osa.setvolume.format(args['<amount>']))
            print("Volume: {}".format(vol))
        else:
            print(colored("Volume value must be a number between 0 and 100", "red"))
            raise DocoptExit


def share(args):
    pass


def toggle_shuffle(args):
    run_osa_script(Osa.noshuffle)
    run_osa_script(Osa.shuffle)


def toggle_repeat(args):
    run_osa_script(Osa.norepeat)
    run_osa_script(Osa.repeat)