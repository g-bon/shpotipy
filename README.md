# Shpotipy
A python based command line interface for spotify.

The project is a python implementation of [Shpotify](https://github.com/hnarayanan/shpotify) by [Harish Narayanan](https://harishnarayanan.org/).

The projects was created to support token based authentication of Spotify's search API.

To make search work please get your credentials from [https://developer.spotify.com/](https://developer.spotify.com/) and set
your **client id** and **client secret** in configuration.py or calling shpotipy login and following instructions.

## Usage:
    shpotipy play [(album | artist | playlist | uri) <query>]
    shpotipy next
    shpotipy prev
    shpotipy replay
    shpotipy pos [<time>]
    shpotipy pause
    shpotipy quit
    shpotipy vol [show | up | down | set <amount>]
    shpotipy status
    shpotipy shuffle
    shpotipy repeat
    shpotipy login

