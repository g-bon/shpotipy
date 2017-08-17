# spotipy
A python based command line interface for spotify.

The project is a python implementation of [Shpotify](https://github.com/hnarayanan/shpotify) by [Harish Narayanan](https://harishnarayanan.org/).

The projects was created to support token based authentication of Spotify's search API.

To make search work please get your credentials from [https://developer.spotify.com/](https://developer.spotify.com/) and set
your **client id** and **client secret** in configuration.py or calling spotipy login and following instructions.

## Usage:
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

