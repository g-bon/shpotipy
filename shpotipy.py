#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shpotipy.


Usage:
    shpotipy play [(album | artist | playlist | uri) <query>]
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
"""

import actions
from docopt import docopt

__version__ = "0.1.0"
__author__ = "Gabriele Bonetti"
__license__ = "MIT"


def main():
    """Main entry point for the shpotipy CLI."""
    args = docopt(__doc__)
    # print(args)

    commands_functions = {
        'play': actions.play,
        'status': actions.status,
        'next': actions.next_track,
        'prev': actions.previous_track,
        'replay': actions.replay,
        'pos': actions.pos,
        'pause': actions.pause,
        'quit': actions.quit_spotify,
        'vol': actions.vol,
        'share': actions.share,
        'shuffle': actions.toggle_shuffle,
        'repeat': actions.toggle_repeat
    }

    arg = next(arg for arg in args if arg in commands_functions.keys() and args[arg] is True)
    commands_functions[arg](args=args)


if __name__ == '__main__':
    main()
