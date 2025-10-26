#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.pipe import parsing
from transcripts18xx.games import Game1889

from tests import context


class TestGameTranscriptProcessor1889(unittest.TestCase):
    df = None

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1889()
        gtp = parsing.GameTranscriptProcessor(Game1889())
        df = gtp.parse_transcript(raw_transcript)
        cls.df = df

    @classmethod
    def tearDownClass(cls) -> None:
        filepath = context.transcript_1889().parent.joinpath(
            context.transcript_1889().stem + '_parsed.csv'
        )
        cls.df.to_csv(filepath, index=False, sep=',')

    def test_shape(self):
        self.assertEqual(1053, self.df.shape[0])
        self.assertEqual(24, self.df.shape[1])

    def test_columns(self):
        expected = [
            'phase', 'type', 'parent', 'id', 'line', 'player', 'amount',
            'private', 'entity', 'source', 'percentage', 'company', 'sequence',
            'location', 'tile', 'rotation', 'direction', 'share_price', 'train',
            'route', 'per_share', 'old_train', 'new_train', 'result'
        ]
        self.assertEqual(sorted(expected), sorted(list(self.df.columns)))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.phase.dropna().unique()))

    def test_type(self):
        expected = {
            'AllPrivatesClose', 'BankBroke', 'Bid', 'BuyPrivate', 'BuyShare',
            'BuyTrain', 'Collect', 'CompanyFloats', 'Contribute', 'DoesNotRun',
            'ExchangeTrain', 'GameOver', 'LayTile', 'NewPhase',
            'OperatesCompany', 'OperatingRound', 'Par', 'Pass', 'PayOut',
            'PlaceToken', 'PresidentNomination', 'PriorityDeal', 'ReceiveFunds',
            'RunTrain', 'SellShares', 'SharePriceMoves', 'Skip', 'StockRound',
            'TrainsRust', 'Withhold'
        }
        self.assertEqual(expected, set(self.df['type'].dropna().unique()))

    def test_parent(self):
        expected = {'Action', 'Event'}
        self.assertEqual(expected, set(self.df.parent.dropna().unique()))

    def test_id(self):
        self.assertEqual(self.df.shape[0], len(self.df.id.dropna().unique()))

    def test_player(self):
        expected = {
            'Millie', 'Sprint', 'camping no reception', 'mindbomb(UTC+9)',
            'tado', 'zorbak'
        }
        self.assertEqual(expected, set(self.df.player.dropna().unique()))

    def test_amount(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.amount.dropna().unique())
        )

    def test_private(self):
        expected = {
            'Dougo Railway', 'Ehime Railway', 'Mitsubishi Ferry',
            'South Iyo Railway', 'Sumitomo Mines Railway',
            'Takamatsu E-Railroad', 'Uno-Takamatsu Ferry'
        }
        self.assertEqual(expected, set(self.df.private.dropna().unique()))

    def test_entity(self):
        expected = {
            'AR', 'IR', 'KO', 'KU', 'Millie', 'SR', 'Sprint', 'TR', 'UR',
            'camping no reception', 'mindbomb(UTC+9)', 'tado', 'zorbak'
        }
        self.assertEqual(expected, set(self.df.entity.dropna().unique()))

    def test_source(self):
        expected = {
            'Auction', 'Dougo Railway', 'Ehime Railway', 'IPO', 'KO', 'KU',
            'Millie', 'Mitsubishi Ferry', 'South Iyo Railway', 'Sprint',
            'Sumitomo Mines Railway', 'Takamatsu E-Railroad', 'The Depot',
            'Uno-Takamatsu Ferry', 'camping no reception', 'market', 'zorbak'
        }
        self.assertEqual(expected, set(self.df.source.dropna().unique()))

    def test_percentage(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.percentage.dropna().unique())
        )

    def test_company(self):
        expected = {'KU', 'TR', 'UR', 'TR (MF)', 'IR', 'KO', 'SR', 'AR'}
        self.assertEqual(expected, set(self.df.company.dropna().unique()))

    def test_sequence(self):
        expected = {
            'OR 1.1',
            'OR 2.1', 'OR 2.2',
            'OR 3.1', 'OR 3.2',
            'OR 4.1', 'OR 4.2',
            'OR 5.1', 'OR 5.2', 'OR 5.3',
            'OR 6.1', 'OR 6.2', 'OR 6.3',
            'SR 1', 'SR 2', 'SR 3', 'SR 4', 'SR 5', 'SR 6',
        }
        self.assertEqual(expected, set(self.df.sequence.dropna().unique()))

    def test_location(self):
        expected = {
            'B5', 'B7', 'C10', 'C10 (Kubokawa)', 'C4 (Ohzu)', 'C8', 'D3', 'D9',
            'E2', 'E2 (Matsuyama)', 'E4', 'E8', 'F3 (Saijou)', 'F5', 'F7', 'F9',
            'F9 (Kouchi)', 'G10 (Nangoku)', 'G12 (Nahari)', 'G4 (Niihama)',
            'H11', 'H3', 'H5', 'H7 (Ikeda)', 'I12 (Muki)', 'I2',
            'I2 (Marugame)', 'I4 (Kotohira)', 'I6', 'I8', 'J11 (Anan)', 'J3',
            'J5 (Ritsurin Kouen)', 'J9 (Komatsujima)', 'K4', 'K4 (Takamatsu)',
            'K6', 'K8', 'K8 (Tokushima)'
        }
        self.assertEqual(expected, set(self.df.location.dropna().unique()))

    def test_tile(self):
        expected = {
            '12', '14', '15', '205', '206', '23', '24', '25', '27', '29', '40',
            '41', '437', '438', '439', '440', '448', '45', '465', '466', '47',
            '492', '5', '57', '58', '6', '611', '8', '9'
        }
        self.assertEqual(expected, set(self.df.tile.dropna().unique()))

    def test_rotation(self):
        expected = {'0', '1', '2', '3', '4', '5'}
        self.assertEqual(expected, set(self.df.rotation.dropna().unique()))

    def test_direction(self):
        expected = {'down', 'right', 'up', 'left'}
        self.assertEqual(expected, set(self.df.direction.dropna().unique()))

    def test_share_price(self):
        self.assertTrue(any(
            float(s).is_integer() for s in
            self.df.share_price.dropna().unique())
        )

    def test_train(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.train.dropna().unique()))

    def test_route(self):
        # Follows: `tile-tile-tile-...` scheme
        pass

    def test_per_share(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.per_share.dropna().unique())
        )

    def test_old_train(self):
        expected = {'4'}
        self.assertEqual(expected, set(self.df.old_train.dropna().unique()))

    def test_new_train(self):
        expected = {'D'}
        self.assertEqual(expected, set(self.df.new_train.dropna().unique()))

    def test_result(self):
        expected = {
            'Millie': 2468,
            'Sprint': 3968,
            'camping no reception': 3775,
            'mindbomb(UTC+9)': 2807,
            'tado': 4249,
            'zorbak': 2804
        }
        self.assertEqual(expected, eval(self.df.iloc[-1, :].result))


class TestTranscriptPostProcessor1889(unittest.TestCase):
    df = None

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1889()
        gtp = parsing.GameTranscriptProcessor(Game1889())
        df = gtp.parse_transcript(raw_transcript)
        tpp = parsing.TranscriptPostProcessor(df, Game1889())
        df = tpp.process()
        cls.df = df

    @classmethod
    def tearDownClass(cls) -> None:
        filepath = context.transcript_1889().parent.joinpath(
            context.transcript_1889().stem + '_processed.csv'
        )
        cls.df.to_csv(filepath, index=False, sep=',')

    def test_shape(self):
        self.assertEqual(1053, self.df.shape[0])
        self.assertEqual(23, self.df.shape[1])

    def test_columns(self):
        expected = [
            'amount', 'company', 'direction', 'id', 'location', 'new_train',
            'old_train', 'parent', 'per_share', 'percentage', 'phase', 'player',
            'private', 'rotation', 'route', 'sequence', 'share_price', 'source',
            'tile', 'train', 'type', 'result', 'major_round'
        ]
        self.assertEqual(sorted(expected), sorted(list(self.df.columns)))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.phase.unique()))

    def test_company(self):
        expected = {'KU', 'AR', 'TR', 'IR', 'UR', 'KO', 'SR'}
        self.assertEqual(expected, set(self.df.company.dropna().unique()))

    def test_sequence(self):
        expected = {
            'ISR 1',
            'OR 1.1',
            'OR 2.1', 'OR 2.2',
            'OR 3.1', 'OR 3.2',
            'OR 4.1', 'OR 4.2',
            'OR 5.1', 'OR 5.2', 'OR 5.3',
            'OR 6.1', 'OR 6.2', 'OR 6.3',
            'SR 1', 'SR 2', 'SR 3', 'SR 4', 'SR 5', 'SR 6',
        }
        self.assertEqual(expected, set(self.df.sequence.unique()))

    def test_location(self):
        expected = {
            'B5', 'B7', 'C10', 'C4', 'C8', 'D3', 'D9', 'E2', 'E4', 'E8', 'F3',
            'F5', 'F7', 'F9', 'G10', 'G12', 'G4', 'H11', 'H3', 'H5', 'H7',
            'I12', 'I2', 'I4', 'I6', 'I8', 'J11', 'J3', 'J5', 'J9', 'K4', 'K6',
            'K8'
        }
        self.assertEqual(expected, set(self.df.location.dropna().unique()))

    def test_source(self):
        expected = {
            'Auction', 'Dougo Railway', 'Ehime Railway', 'IPO', 'KO', 'KU',
            'Millie', 'Mitsubishi Ferry', 'South Iyo Railway', 'Sprint',
            'Sumitomo Mines Railway', 'Takamatsu E-Railroad', 'The Depot',
            'Uno-Takamatsu Ferry', 'camping no reception', 'market', 'zorbak'
        }
        self.assertEqual(expected, set(self.df.source.dropna().unique()))

    def test_contributions(self):
        self.assertEqual('UR', self.df.iloc[773, :].company)
        self.assertEqual('IR', self.df.iloc[906, :].company)
        self.assertEqual('SR', self.df.iloc[923, :].company)

    def test_major_rounds(self):
        expected = {
            'ISR 1',
            'OR 1', 'OR 2', 'OR 3', 'OR 4', 'OR 5', 'OR 6',
            'SR 1', 'SR 2', 'SR 3', 'SR 4', 'SR 5', 'SR 6',
        }
        self.assertEqual(expected, set(self.df.major_round.unique()))
