class Osa(object):
    """
    Osascript commands to interact with spotify.

    Commands that need parametrization are written with
    curly bracket placeholder to be used with string.format
    """

    getstate = 'tell application "Spotify" to player state as string'
    getartist = 'tell application "Spotify" to artist of current track as string'
    getalbum = 'tell application "Spotify" to album of current track as string'
    gettrack = 'tell application "Spotify" to name of current track as string'
    playtrack = 'tell application "Spotify" to play track "{}"'
    playprevioustrack = """
                        tell application "Spotify"
                            set player position to 0
                            previous track
                        end tell
                        """
    playnexttrack = 'tell application "Spotify" to next track'
    playfromstart = 'tell application "Spotify" to set player position to 0'
    playpause = 'tell application "Spotify" to playpause'
    pause = 'tell application "Spotify" to pause'
    quit = 'tell application "Spotify" to quit'
    checkrunning = 'application "Spotify" is running'
    activate = 'tell application "Spotify" to activate'
    play = 'tell application "Spotify" to play'
    geturi = 'tell application "Spotify" to spotify url of current track'
    state = 'tell application "Spotify" to player state as string'
    setvolume = 'tell application "Spotify" to set sound volume to {}'
    noshuffle = 'tell application "Spotify" to set shuffling to not shuffling'
    shuffle = 'tell application "Spotify" to shuffling'
    norepeat = 'tell application "Spotify" to set repeating to not repeating'
    repeat = 'tell application "Spotify" to repeating'
    getvolume = 'tell application "Spotify" to sound volume as integer'
    getduration = """
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
                  """
    getposition = """
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
                  """
