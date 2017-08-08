#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Shpotipy.


Usage:
    shpotipy play [(album | artist | list | uri) <query>]
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
'''

from __future__ import unicode_literals, print_function, absolute_import
from docopt import docopt, DocoptExit
from subprocess import Popen, PIPE
from termcolor import colored
from configurations import client_id, client_secret

__version__ = "0.1.0"
__author__ = "Gabriele Bonetti"
__license__ = "MIT"


class Osa:
    getstate = 'tell application "Spotify" to player state as string'
    getartist = 'tell application "Spotify" to artist of current track as string'
    getalbum = 'tell application "Spotify" to album of current track as string'
    gettrack = 'tell application "Spotify" to name of current track as string'
    playtrack = 'tell application "Spotify" to play track "{}"'
    playprevioustrack = '''tell application "Spotify"
                               set player position to 0
                               previous track
                           end tell'''
    playnexttrack = 'tell application "Spotify" to next track'
    playfromstart = 'tell application "Spotify" to set player position to 0'
    playpause = 'tell application "Spotify" to playpause'
    quit = 'tell application "Spotify" to quit'
    activate = 'tell application "Spotify" to activate'
    play = 'tell application "Spotify" to play'
    state = 'tell application "Spotify" to player state as string'
    setvolume = 'tell application "Spotify" to set sound volume to {}'
    noshuffle = 'tell application "Spotify" to set shuffling to not shuffling'
    shuffle = 'tell application "Spotify" to shuffling'
    norepeat = 'tell application "Spotify" to set repeating to not repeating'
    repeat = 'tell application "Spotify" to repeating'
    getvolume = 'tell application "Spotify" to sound volume as integer'
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


def run_osa_script(script):
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    return stdout.strip()


def status(args):
    print("Spotify is currently {}".format(run_osa_script(Osa.getstate)))
    print("Artist: {}".format(run_osa_script(Osa.getartist)))
    print("Album: {}".format(run_osa_script(Osa.getalbum)))
    print("Track: {}".format(run_osa_script(Osa.gettrack)))
    pos()

def next_track(args):
    run_osa_script(Osa.playnexttrack)


def previous_track(args):
    run_osa_script(Osa.playprevioustrack)


def play(args):
    pass


def replay(args):
    run_osa_script(Osa.playfromstart)


def pos(args):
    print("Position: {} / {}".format(run_osa_script(Osa.getposition), run_osa_script(Osa.getduration)))


def pause(args):
    run_osa_script(Osa.playpause)


def quit_spotify(args):
    run_osa_script(Osa.quit)


def vol(args):
    vol_step = 10

    if args['show']:
        print(run_osa_script(Osa.getvolume))

    elif args['up']:
        vol = run_osa_script(Osa.getvolume)
        run_osa_script(Osa.setvolume.format(vol + vol_step))
        print("Volume: {}".format(vol+vol_step))

    elif args['down']:
        vol = run_osa_script(Osa.getvolume)
        run_osa_script(Osa.setvolume.format(vol - vol_step))
        print("Volume: {}".format(vol-vol_step))

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
    pass


def toggle_repeat(args):
    pass


def main():
    '''Main entry point for the shpotipy CLI.'''
    args = docopt(__doc__)
    # print(args)

    command = next(arg for arg in args if arg in ['play', 'status', 'next', 'prev', 'replay', 'pos', 'pause', 'quit', 'vol', 'share', 'shuffle', 'repeat'] and args[arg] is True)

    {
        'play': play,
        'status': status,
        'next': next_track,
        'prev': previous_track,
        'replay': replay,
        'pos': pos,
        'pause': pause,
        'quit': quit_spotify,
        'vol': vol,
        'share': share,
        'shuffle': toggle_shuffle,
        'repeat': toggle_repeat
    }[command](args)


if __name__ == '__main__':
    main()
