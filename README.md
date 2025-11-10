18xx Transcript Parser
======================

![docs](https://img.shields.io/readthedocs/transcripts18xx)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/codePascal/transcripts18xx/test_pytest.yml)
![GitHub Tag](https://img.shields.io/github/v/tag/codePascal/transcripts18xx)

A Python package to parse and process game transcripts
from [18xx.games](https://18xx.games/).
It produces structured data suitable for analysis, modeling and visualization.

For a more enriched documentation, visit the project documentation on
readthedocs
[transcripts18xx documentation](https://transcripts18xx.readthedocs.io/).

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

Parsing a transcript
--------------------

After installation, single transcripts can be parsed by calling the poetry
script `trx` from the command line.

Run the following command to see command line options:

```bash
trx --help
```

Quick references
----------------

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
transcript_directory
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

Contributing
------------

Here are some ways you can contribute to this project:

* You can [open an issue](https://github.com/codePascal/transcripts18xx/issues)
  if you would like to request a feature or report a bug/error.
* If you found a bug, please illustrate it with a minimal [reprex](https://tidyverse.org/help/#reprex)
* If you want to contribute on a deeper level, it is a good idea to file an
  issue first. I will be happy to discuss other ways of contribution!


