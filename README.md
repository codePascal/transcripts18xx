transcripts18xx
===============

A Python package to parse and process game transcripts
from [18xx.games](https://18xx.games/).
It produces structured data suitable for analysis, modeling and visualization.

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

### Game transcripts

Game transcripts should be in plain text format as shown below:

```text
 -- Phase 2 (Operating Rounds: 1 | Train Limit: 4 | Available Tiles: Yellow) --
[23:29] player1 bids $165 for Camden & Amboy
[23:30] player2 bids $75 for Delaware & Hudson
[23:30] player3 bids $115 for Mohawk & Hudson
[23:31] player4 bids $120 for Mohawk & Hudson
[23:32] player1 buys Schuylkill Valley for $20
[23:32] player2 bids $170 for Camden & Amboy
[23:32] player3 bids $175 for Camden & Amboy
[23:33] player4 buys Champlain & St.Lawrence for $40
[23:33] player2 wins the auction for Delaware & Hudson with the only bid of $75
```

These raw transcripts must follow a consistent naming convention:

```text
<game_type>_<game_id>.txt
```

* `game_type`: Abbreviation of the 18xx variant (e.g., `1830`, `1889`)
* `game_id`: The 6-digit game ID

### Transcript parser

The core of the library is the `TranscriptParser` class.
It implements a transcript parser that takes the path to the transcript and the
game type as argument and generates a parsed transcript in CSV format and
complementing metadata in JSON format.

```pycon
>>> import transcripts18xx as trx
>>> transcript_path = Path('1830_123456.txt')
>>> game_type = trx.Games.G1830.select()
>>> parser = trx.TranscriptParser(transcript_path, game_type)
>>> parser.parse()
```

This will create two new files within the transcript directory:

```
/
├── 1830_123456.txt
├── 1830_123456_final.csv       --> The parsed final transcript data
└── 1830_123456_metadata.json   --> The metadata of the game
```

### Transcript context

To handle multiple parsed transcripts, the `TranscriptContext` is implemented.
It implements a dataclass that contains the relevant metadata as well as paths
to the raw transcript, final data and metadata. Further, it can be used to load
metadata or dataframe of the record.

```pycon
>>> import transcripts18xx as trx
>>> transcript_path = Path('1830_123456.txt')
>>> trx_ctx = trx.TranscriptContext.from_raw(transcript_path)
```

Output Artifacts
----------------

### Parsed transcript

The parsing output is saved as Pandas DataFrame and contains detailed game state
information and can be structured into three major column groups.

#### Core actions and events

These columns track key actions and events, involved entities and game flow:

| Category             | Column        | Description                                                 | Column Density |
|----------------------|---------------|-------------------------------------------------------------|----------------|
| **General Metadata** | `phase`       | Game phase (e.g., 2, 3, D)                                  | dense          |
|                      | `type`        | Type of action or event (e.g., Bid, BuyShare)               | dense          |
|                      | `sequence`    | Round identifier (e.g., SR 1, OR 3.1)                       | dense          |
|                      | `id`          | Sequence number within game                                 | dense          |
|                      | `parent`      | Group of which type is part of (e.g., Action or Event)      | dense          |
| **Player Actions**   | `player`      | Player involved                                             | sparse         |
|                      | `amount`      | Amount of money in $ involved                               | sparse         |
|                      | `source`      | Source involved (e.g., IPO, market, Depot, player, company) | sparse         |
|                      | `private`     | Private company involved                                    | sparse         |
|                      | `percentage`  | Share percentage involved                                   | sparse         |
| **Company Context**  | `company`     | Company involved                                            | sparse         |
|                      | `share_price` | Share price at the time                                     | sparse         |
| **Map and Tokens**   | `location`    | Hex location on the map                                     | sparse         |
|                      | `tile`        | Tile placed                                                 | sparse         |
|                      | `rotation`    | Orientation of the tile                                     | sparse         |
|                      | `direction`   | Direction of the tile                                       | sparse         |
| **Train Operations** | `train`       | Train involved                                              | sparse         |
|                      | `route`       | Route run by the train                                      | sparse         |
|                      | `old_train`   | Train being replaced                                        | sparse         |
|                      | `new_train`   | New train being acquired                                    | sparse         |
|                      | `per_share`   | Payout per share in dividend                                | sparse         |

Besides the general metadata, the other columns are sparsely filled as they will
be used most often for a specific event or action only.

#### Player state columns

Each player has a dedicated block of columns which represents its state at
any point in time.

- `<player>_cash` — Cash on hand
- `<player>_privates` — Private companies owned, including their values
- `<player>_value` — Net worth at this point
- `<player>_priority_deal` — Whether the player has the priority deal token
- `<player>_shares_<company>` — Shareholding in each company (
  e.g. `player1_shares_B&O`)

#### Company state columns

Each company has a set of attributes describing its state at any point in time.

- `<company>_cash` — Company treasury
- `<company>_privates` — Privates owned by the company
- `<company>_ipo` — Shares remaining in IPO
- `<company>_market` — Shares in market
- `<company>_president` — President player
- `<company>_share_price` — Current market price
- `<company>_trains_<trains>` — Train counts by type (e.g. `PRR_trains_2`)

### Game metadata

The game metadata complements the processed CSV file.
It provides game information, the final game state, player results, a
verification result and unprocessed lines during parsing.

#### Game information

| Field         | Description                                              |
|---------------|----------------------------------------------------------|
| `game`        | Game variant (e.g., 1830)                                |
| `id`          | Game ID                                                  |
| `num_players` | Total number of players                                  |
| `finished`    | Game end condition (e.g., BankBroke, PlayerGoesBankrupt) |
| `winner`      | Player with the highest value in the end                 |

#### Player mapping

The `mapping` field records how usernames were anonymized to `<player>`.
This is useful for identifying which real player corresponds to which parsed
record.

#### Player results

The `result` field depicts the ranking of the players and their final value.
This result is extracted from the transcripts last line.
If the transcript does not represent a full game with a game over identifier,
e.g. an ongoing game, this field will be empty.

#### Final state

The final state depicts the player and company state columns as a full, dense
snapshot of the game state at its conclusion.
It is structured into players and companies, as shown below.

```json
{
  "final_state": {
    "players": {
    },
    "companies": {
    }
  }
}
```

Example for a final player state in an 1830 game:

```json
{
  "name": "player1",
  "cash": 3304.0,
  "privates": {
  },
  "value": 6735.0,
  "shares": {
    "B&M": 6,
    "B&O": 6,
    "C&O": 1,
    "CPR": 0,
    "ERIE": 4,
    "NYC": 1,
    "NYNH": 0,
    "PRR": 1
  },
  "priority_deal": false
}
```

Example for the PRR company state in an 1830 game:

```json
{
  "name": "PRR",
  "cash": 40.0,
  "privates": {},
  "trains": {
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "D": 1
  },
  "ipo": 0,
  "market": 0,
  "president": "player3",
  "share_price": 67.0
}
```

#### Verification

The verification compares the final value of each player reported in the
transcript and the one calculated during the game state processing.
The verification result will be depicted in the `success` field.
Differences will be written to the `diffs` field.

#### Unprocessed lines

For debugging purposes, unprocessed lines, i.e. lines that were not matched to a
step during parsing, will be written to the metadata as well.

#### Parse result

The parse result depicts the success of the raw transcript parsing. If no errors
occurred, it will be set to `SUCCESS`. Otherwise, the received error will be
written, i.e., `No players found`.

Supported Games
---------------

The following games are supported:

* [1830: Railroads & Robber Barons](https://en.wikipedia.org/wiki/1830:_The_Game_of_Railroads_and_Robber_Barons)

Games soon to be supported:

* [1889: The History of Railroading in Shikoku](https://boardgamegeek.com/boardgame/23540/shikoku-1889)
