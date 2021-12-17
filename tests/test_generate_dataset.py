import unittest

import chess
import chess.pgn

from chess_engine.data.exceptions import InvalidHalfMoveError
from chess_engine.data.generate_dataset import get_last_halfmove_number, sample_game_state_result, extract_game


class TestGenerateDataset(unittest.TestCase):

    def test_get_last_halfmove_number_even(self):
        # Arrange
        pgn = open("resources/rolvag-kjartansson-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual = get_last_halfmove_number(game)

        # Assert
        expected = 56
        self.assertEqual(actual, expected)

    def test_get_last_halfmove_number_odd(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual = get_last_halfmove_number(game)

        # Assert
        expected = 91
        self.assertEqual(actual, expected)

    def test_sample_game_state_start(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual_fen, actual_result = sample_game_state_result(game, 0)

        # Assert
        expected_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        expected_result = '1/2-1/2'
        self.assertEqual(actual_fen, expected_fen)
        self.assertEqual(actual_result, expected_result)

    def test_sample_game_state_even(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual_fen, actual_result = sample_game_state_result(game, 8)

        # Assert
        expected_fen = 'r1bqk2r/ppppbppp/2n2n2/4p3/2P5/P1N1P3/1P1P1PPP/R1BQKBNR w KQkq - 1 5'
        expected_result = '1/2-1/2'
        self.assertEqual(actual_fen, expected_fen)
        self.assertEqual(actual_result, expected_result)

    def test_sample_game_state_odd(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual_fen, actual_result = sample_game_state_result(game, 81)

        # Assert
        expected_fen = '6k1/6p1/p7/1pp5/3nqQ1P/P1B3P1/1P5K/8 b - - 3 41'
        expected_result = '1/2-1/2'
        self.assertEqual(actual_fen, expected_fen)
        self.assertEqual(actual_result, expected_result)

    def test_sample_game_state_end(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        actual_fen, actual_result = sample_game_state_result(game, 91)

        # Assert
        expected_fen = '6k1/6p1/2n5/p7/1pp1KP1P/P7/1P1B4/8 b - - 1 46'
        expected_result = '1/2-1/2'
        self.assertEqual(actual_fen, expected_fen)
        self.assertEqual(actual_result, expected_result)

    def test_sample_game_state_result_raises_exception(self):
        # Arrange
        pgn = open("resources/sundararajan-ziatdinov-2018.pgn")
        game = chess.pgn.read_game(pgn)

        # Act
        self.assertRaises(InvalidHalfMoveError, sample_game_state_result, game, -1)
        self.assertRaises(InvalidHalfMoveError, sample_game_state_result, game, 92)

    def test_extract_game_three_games(self):
        # Arrange
        filename = 'resources/three_games.pgn'

        # Act
        actual = list(extract_game(filename))

        # Assert
        self.assertEqual(len(actual), 3)
        self.assertIsInstance(actual[0], chess.pgn.Game)
        self.assertIsInstance(actual[1], chess.pgn.Game)
        self.assertIsInstance(actual[2], chess.pgn.Game)

    def test_extract_game_one_game(self):
        # Arrange
        filename = 'resources/single_game.pgn'

        # Act
        actual = list(extract_game(filename))

        # Assert
        self.assertEqual(len(actual), 1)
        self.assertIsInstance(actual[0], chess.pgn.Game)

    def test_extract_game_empty_file(self):
        # Arrange
        filename = 'resources/empty.pgn'

        # Act
        actual = list(extract_game(filename))

        # Assert
        expected = []
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
