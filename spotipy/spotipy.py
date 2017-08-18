#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""



Usage:
    spotipy play [(album | artist | playlist | uri) <query>]
    spotipy next
    spotipy prev
    spotipy replay
    spotipy pos [<time>]
    spotipy pause
    spotipy quit
    spotipy vol [show | up | down | set <amount>]
    spotipy status
    spotipy share (uri | url)
    spotipy shuffle
    spotipy repeat
    spotipy login
"""

from __future__ import (print_function, unicode_literals, division, absolute_import)
from future import standard_library

standard_library.install_aliases()



from builtins import next
from docopt import docopt
from spotipy import actions

__version__ = "0.4"
__author__ = "Gabriele Bonetti"
__license__ = "MIT"


def main():
    """Main entry point for the spotipy CLI."""
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
        'repeat': actions.toggle_repeat,
        'login': actions.login_wizard
    }

    arg = next(arg for arg in args if arg in commands_functions.keys() and args[arg] is True)
    commands_functions[arg](args=args)


if __name__ == '__main__':
    main()
