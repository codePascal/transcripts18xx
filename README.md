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

The core of the library is the `transcript` module.
It implements a transcript parser than takes the path to the transcript and the
game type as argument.

```pycon
>>> from transcripts18xx import transcript

>>> transcript_path = Path('1830_123456.txt')
>>> game_type = transcript.games.Game1830()
>>> parser = transcript.TranscriptParser(transcript_path, game_type)
```

### Parsing the transcript

The transcript parser parses the raw transcript into a pandas Dataframe.
Actions and events of the game are represented as rows depicting the phase,
round, player and company states.

```pycon
>>> parser.parse()
```

### Saving the results

The full data consisting of the dataframe, metadata and final state can then
be saved.

```pycon
>>> parser.save()
```

This will create three files within the transcript directory:

```
/
├── 1830_123456.txt             --> The original raw transcript
├── 1830_123456_final.csv       --> The parsed final transcript data
├── 1830_123456_metadata.json   --> The metadata of the game
└── 1830_123456_states.json     --> The final states of player and companies
```

#### Parsed transcript

The [parsing output](tests/resources/1830_201210_final.csv) is saved as pandas
Dataframe.

#### Game metadata

The [game metadata](tests/resources/1830_201210_metadata.json) saves the game
type, game id, number of players and the player mapping.
The player mapping depicts the anonymization that is performed in order to
generalize the result.

#### Final states

The [final states](tests/resources/1830_201210_states.json) represent the player
and company states after the game ended.
As noted above, the player names are anonymized and can be replicated using
the game metadata.

### Modifying the results

The library implements two functions to modify the resulting data into other
structures than a pandas Dataframe.

#### Serializing the data

The data can be serialized into a dictionary with the keys representing the
row indexes and the values representing the row data as dictionary.
The function requires the original raw transcript path as argument.

```pycon
>>> from transcripts18xx import transcript

>>> transcript_path = Path('1830_123456.txt')
>>> transcript.serialize(transcript_path)
```

The [serialized data](tests/resources/1830_201210_serialized.json) will be saved
in the transcript directory as well:

```
/
├── 1830_123456.txt
├── 1830_123456_final.csv
├── 1830_123456_metadata.json
├── 1830_123456_states.json
└── 1830_123456_serialized.json --> The serialized data
```

#### Flattening the data

The data can be flattened into a pandas Dataframe.
The dictionaries representing the player and company states are expanded to
columns in the dataframe, e.g. `player1_cash`.
The function requires the original raw transcript path as argument.

```pycon
>>> from transcripts18xx import transcript

>>> transcript_path = Path('1830_123456.txt')
>>> transcript.flatten(transcript_path)
```

The [flattened data](tests/resources/1830_201210_flattened.csv) will be saved
in the transcript directory as well:

```
/
├── 1830_123456.txt
├── 1830_123456_final.csv
├── 1830_123456_metadata.json
├── 1830_123456_states.json
└── 1830_123456_flattened.csv   --> The flattened data
```

Supported Games
---------------

The following games are supported:

* [1830: Railroads & Robber Barons](https://en.wikipedia.org/wiki/1830:_The_Game_of_Railroads_and_Robber_Barons)

