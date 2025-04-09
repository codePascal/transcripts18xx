transcripts18xx
===============

A Python package to parse and process game transcripts
from [18xx.games](https://18xx.games/).

Installation
------------

To install the Python library, run

```shell
pip install transcripts18xx
```

Library usage
-------------

The module provides just one function `transcipt.parse`.
It takes a transcript file and the game type as input, and generates a pandas
Dataframe which depicts the actions, events and game state:

```pycon
>>> from transcripts18xx import transcript, games

>>> df = transcript.parse(Path('<path_to_the_transcript.txt>'), games.Game18xx())
>>> print(df)
     phase             type  parent    id  ... route per_share old_train new_train
0        2         NewPhase   Event     0  ...   NaN       NaN       NaN       NaN
1        2              Bid  Action     1  ...   NaN       NaN       NaN       NaN
2        2              Bid  Action     2  ...   NaN       NaN       NaN       NaN
3        2              Bid  Action     3  ...   NaN       NaN       NaN       NaN
4        2              Bid  Action     4  ...   NaN       NaN       NaN       NaN
...    ...              ...     ...   ...  ...   ...       ...       ...       ...
1341     D           PayOut  Action  1341  ...   NaN        42       NaN       NaN
1342     D  SharePriceMoves   Event  1342  ...   NaN       NaN       NaN       NaN
1343     D             Pass  Action  1343  ...   NaN       NaN       NaN       NaN
1344     D             Skip  Action  1344  ...   NaN       NaN       NaN       NaN
1345     D         GameOver   Event  1345  ...   NaN       NaN       NaN       NaN

[1346 rows x 21 columns]

```

The result is saved as `.csv` file as well: `<path_to_the_transcript.csv>`.

Supported Games
---------------

The following games are supported:

* [1830: Railroads & Robber Barons](https://en.wikipedia.org/wiki/1830:_The_Game_of_Railroads_and_Robber_Barons)

