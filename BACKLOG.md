# Backlog

## General issues

* Thread-safe pool executor for line processing: mapping on index of line
* Add debug outputs

## Parsing issues

* Omit date entries in transcript: `-- yyyy-mm-dd --`
* Omit optional rules per game
* Omit master actions `\u2022 Action(action) via Master Mode by: player`
* In case of game over: take players from game over
    * Otherwise: parse from transcript lines
* Add error codes why game could not be parsed
    * OK
    * FAILED (general purpose)
    * VERIFICATION_FAILED
    * NO_PLAYERS_FOUND