# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased] - yyyy-mm-dd

### Added

### Changed

### Removed

### Fixed

## [3.0.0] - 2025-09-14

### Added

- Detection of games manually ended by player.
- Post-processing of transcript adds expected columns before running pipe.
- Detection of private exchange of player for shares from company.
- Support for game Shikoku 1889.
- Games with different currency now supported: Game currency is replaced in
  transcript lines with default currency ($).
- Detection of master modes, consent confirmations and date entries, these will
  be detected but not added to the final result.

### Changed

- Start capital of Games18xx denote starting capital of each player and not the
  sum that is divided.

### Removed

### Fixed

- Regex pattern for GameOver: Detects everything up to the next comma (including
  spaces, hyphens, special letters, etc.)
- Missing columns are added in post-processing step.
- State verification of player values in game state and transcript result.
- Regex pattern for PlayerGoesBankrupt: Detect special characters as well.
- Sold shares when bankrupt do not add up to a players cash.
- If game over was found, game ending must be from a known list.

## [2.0.0] - 2025-06-09

### Added

- Function to retrieve game name from game enum, e.g., `G1830` -> `1830`.
- Functions to retrieve transcript identifier and ID from filename.

### Changed

- Made package `pipe` consisting of parsing and verification module.
- Parsed result expands the player and company states, including shares and
  train dictionaries
- Private dicts in parsed result are dumped to a json string.
- Invoking parse function will save the results and run minimal verification in
  any case.
- Full verification can be invoked as standalone.
- Metadata includes now final state, game ending, result and winner, unprocessed
  lines during parsing, and verification result of player values.

### Removed

- Option to flatten the result: Parsed result flattens the states now.
- Option to serialize the result.

### Fixed

- Initialization of the company game states: Takes the listed companies of the
  base game instead of companies from the transcript. This way, companies not
  floated during the game will show up as well.

## [1.0.0] - 2025-05-21

### Added

- First version of transcripts18xx.



