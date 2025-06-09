transcripts18xx
===============

A Python package to parse and process game transcripts
from [18xx.games](https://18xx.games/).

Installation
------------

Python library can be installed with `poetry`. Run the following command:

```shell
poetry add git+ssh://git@github.com:codePascal/transcripts18xx.git
```

Or use https instead of ssh:

```shell
poetry add git+https://git@github.com:codePascal/transcripts18xx.git
```

See the [poetry documentation](https://python-poetry.org/docs/cli/#add) for more
information.

Library usage
-------------

### Transcript parser

The core of the library is the `transcript` module.
It implements a transcript parser than takes the path to the transcript and the
game type as argument.
The parser parses the raw transcript into a Pandas DataFrame.
Actions and events of the game are represented as rows depicting the phase,
round, player and company states.

```pycon
>>> from transcripts18xx import transcript

>>> transcript_path = Path('1830_123456.txt')
>>> game_type = transcript.games.Game1830()
>>> parser = transcript.TranscriptParser(transcript_path, game_type)
>>> parser.parse()
```

This will create two new files within the transcript directory:

```
/
├── 1830_123456.txt
├── 1830_123456_final.csv       --> The parsed final transcript data
└── 1830_123456_metadata.json   --> The metadata of the game
```

#### Parsed transcript

The [parsing output](docs/source/_static/1830_201210_final.csv) is saved as
Pandas DataFrame.

#### Game metadata

The [game metadata](docs/source/_static/1830_201210_metadata.json) saves the
game type, game id, number of players and the player mapping.
The player mapping depicts the anonymization that is performed in order to
generalize the result.


Supported Games
---------------

The following games are supported:

* [1830: Railroads & Robber Barons](https://en.wikipedia.org/wiki/1830:_The_Game_of_Railroads_and_Robber_Barons)

