Usage
=====

Parsing a transcript
--------------------

With the package installation, single transcripts can be parsed by calling the
script ``trx`` from the command line.

The script takes the type of the game, e.g., ``G1830`` and the path to the
raw transcript as arguments.
After parsing, the final game state is compared to a ground truth file.
The file must be located in the transcript directory.
The verification can be skipped by setting the ``skip-verify`` flag.

Run the following to inspect command line arguments::

    $ trx --help

Game transcripts
^^^^^^^^^^^^^^^^

Game transcripts should be in plain text format as shown below:

.. code-block:: text

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

These raw transcripts must follow a consistent naming convention::

    <game_type>_<game_id>.txt

* ``game_type``: Abbreviation of the 18xx variant (e.g., ``1830``, ``1889``)
* ``game_id``: The 6-digit game ID

Game state verification
^^^^^^^^^^^^^^^^^^^^^^^

By default, the script runs a verification based on a truth file.

The file must be located in the transcript directory, must be in ``.json``
format and ``_truth`` must be appended to the transcript file name.

Output artifacts
----------------

Parsing a transcript, will generate two outputs:

* the parsed transcript,
* metadata describing general information of the game and parse results.

Parsed transcript
^^^^^^^^^^^^^^^^^

The parsing output is saved as Pandas DataFrame and contains detailed game state
information and can be structured into three major column groups.

The parsed transcript will be saved in the transcript directory, in ``.csv``
format and ``_final`` appended to the transcript file name.

Core actions and events
"""""""""""""""""""""""

These columns track key actions and events, involved entities and game flow:

+----------------------+-----------------+-------------------------------------------------------------+----------------+
| Category             | Column          | Description                                                 | Column Density |
+======================+=================+=============================================================+================+
| **General Metadata** | ``phase``       | Game phase (e.g., 2, 3, D)                                  | dense          |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``type``        | Type of action or event (e.g., Bid, BuyShare)               | dense          |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``sequence``    | Round identifier (e.g., SR 1, OR 3.1)                       | dense          |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``id``          | Sequence number within game                                 | dense          |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``parent``      | Group of which type is part of (e.g., Action or Event)      | dense          |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``major_round`` | Major stock and operating round (e.g., SR 1, OR 3)          | dense          |
+----------------------+-----------------+-------------------------------------------------------------+----------------+
| **Player Actions**   | ``player``      | Player involved                                             | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``amount``      | Amount of money in $ involved                               | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``source``      | Source involved (e.g., IPO, market, Depot, player, company) | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``private``     | Private company involved                                    | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``percentage``  | Share percentage involved                                   | sparse         |
+----------------------+-----------------+-------------------------------------------------------------+----------------+
| **Company Context**  | ``company``     | Company involved                                            | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``share_price`` | Share price at the time                                     | sparse         |
+----------------------+-----------------+-------------------------------------------------------------+----------------+
| **Map and Tokens**   | ``location``    | Hex location on the map                                     | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``tile``        | Tile placed                                                 | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``rotation``    | Orientation of the tile                                     | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``direction``   | Direction of the tile                                       | sparse         |
+----------------------+-----------------+-------------------------------------------------------------+----------------+
| **Train Operations** | ``train``       | Train involved                                              | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``route``       | Route run by the train                                      | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``old_train``   | Train being replaced                                        | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``new_train``   | New train being acquired                                    | sparse         |
|                      +-----------------+-------------------------------------------------------------+----------------+
|                      | ``per_share``   | Payout per share in dividend                                | sparse         |
+----------------------+-----------------+-------------------------------------------------------------+----------------+

Besides the general metadata, the other columns are sparsely filled as they will
be used most often for a specific event or action only.

Player state columns
""""""""""""""""""""

Each player has a dedicated block of columns which represents its state at
any point in time.

- ``<player>_cash`` — Cash on hand
- ``<player>_privates`` — Private companies owned, including their values
- ``<player>_value`` — Net worth at this point
- ``<player>_priority_deal`` — Whether the player has the priority deal token
- ``<player>_shares_<company>`` — Shareholding in each company (
  e.g. ``player1_shares_B&O``)

Company state columns
"""""""""""""""""""""

Each company has a set of attributes describing its state at any point in time.

- ``<company>_cash`` — Company treasury
- ``<company>_privates`` — Privates owned by the company
- ``<company>_ipo`` — Shares remaining in IPO
- ``<company>_market`` — Shares in market
- ``<company>_president`` — President player
- ``<company>_share_price`` — Current market price
- ``<company>_trains_<trains>`` — Train counts by type (e.g. ``PRR_trains_2``)

Game metadata
^^^^^^^^^^^^^

The game metadata complements the processed CSV file.
It provides game information, the final game state, player results, a
verification result and unprocessed lines during parsing.

The transcript metadata will be saved in the transcript directory, in ``.json``
format and ``_metadata`` appended to the transcript file name.

Game information
""""""""""""""""

+-----------------+----------------------------------------------------------+
| Field           | Description                                              |
+=================+==========================================================+
| ``game``        | Game variant (e.g., 1830)                                |
+-----------------+----------------------------------------------------------+
| ``id``          | Game ID                                                  |
+-----------------+----------------------------------------------------------+
| ``num_players`` | Total number of players                                  |
+-----------------+----------------------------------------------------------+
| ``finished``    | Game end condition (e.g., BankBroke, PlayerGoesBankrupt) |
+-----------------+----------------------------------------------------------+
| ``winner``      | Player with the highest value in the end                 |
+-----------------+----------------------------------------------------------+

Player mapping
""""""""""""""

The ``mapping`` field records how usernames were anonymized to ``<player>``.
This is useful for identifying which real player corresponds to which parsed
record.

Player results
""""""""""""""

The ``result`` field depicts the ranking of the players and their final value.
This result is extracted from the transcripts last line.
If the transcript does not represent a full game with a game over identifier,
e.g. an ongoing game, this field will be empty.

Final state
"""""""""""

The final state depicts the player and company state columns as a full, dense
snapshot of the game state at its conclusion.
It is structured into players and companies, as shown below.

.. code-block:: json

    {
      "final_state": {
        "players": {
        },
        "companies": {
        }
      }
    }

Example for a final player state in an 1830 game:

.. code-block:: json

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

Example for the PRR company state in an 1830 game:

.. code-block:: json

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

Verification
""""""""""""

The verification compares the final value of each player reported in the
transcript and the one calculated during the game state processing.
The verification result will be depicted in the ``success`` field.
Differences will be written to the ``diffs`` field.

Unprocessed lines
"""""""""""""""""

For debugging purposes, unprocessed lines, i.e. lines that were not matched to a
step during parsing, will be written to the metadata as well.

Parse result
""""""""""""

The parse result depicts the success of the raw transcript parsing. If no errors
occurred, it will be set to ``SUCCESS``. Otherwise, the received error will be
written, i.e., ``No players found``.


Example
-------

This section will explain the usage using an exemplary raw transcript and
a associated ground truth file, you can download them here:

* :download:`1830_201210.txt <_static/1830_201210.txt>`
* :download:`1830_201210_truth.json <_static/1830_201210_truth.json>`

In the following, the structure below is assumed::

    ~/Downloads
    ├── 1830_201210.txt
    └── 1830_201210_truth.json

As depicted by the transcript name, its game variant is ``1830`` and its game
id is ``201210``.

To parse the transcript, run the following::

    $ trx G1830 ~/Downloads/1830_201210.txt

After successful parsing, the script will output the metadata and some state
differences to the console.

.. admonition:: Note

    The state difference will output that tokens, liquidity and certs are
    missing for the players. This is no error, but rather a missing
    implementation to parse these elements.

As noted above, the output artifacts will be saved in the transcript
directory.
Hence the following files will now be available in the downloads folder::

    ~/Downloads
    ├── 1830_201210.txt
    ├── 1830_201210_final.csv
    ├── 1830_201210_metadata.json
    └── 1830_201210_truth.json

The output artifacts are available here as well:

* :download:`1830_201210_final.csv <_static/1830_201210_final.csv>`
* :download:`1830_201210_metadata.json <_static/1830_201210_metadata.json>`