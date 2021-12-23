import unittest

import numpy as np

from chess_engine.data.serializer import convert_fen_to_array, \
    convert_piece_list_to_array, convert_game_result_to_int


class TestSerializer(unittest.TestCase):

    def test_serialize_initial_state(self):
        # Arrange
        # White
        white_king = np.zeros((8, 8), np.int8)
        white_king[7, 4] = 1
        white_queen = np.zeros((8, 8), np.int8)
        white_queen[7, 3] = 1
        white_rook = np.zeros((8, 8), np.int8)
        white_rook[7, 0] = 1
        white_rook[7, 7] = 1
        white_bishop = np.zeros((8, 8), np.int8)
        white_bishop[7, 2] = 1
        white_bishop[7, 5] = 1
        white_knight = np.zeros((8, 8), np.int8)
        white_knight[7, 1] = 1
        white_knight[7, 6] = 1
        white_pawn = np.zeros((8, 8), np.int8)
        for i in range(0, 8):
            white_pawn[6, i] = 1

        # Black
        black_king = np.zeros((8, 8), np.int8)
        black_king[0, 4] = 1
        black_queen = np.zeros((8, 8), np.int8)
        black_queen[0, 3] = 1
        black_rook = np.zeros((8, 8), np.int8)
        black_rook[0, 0] = 1
        black_rook[0, 7] = 1
        black_bishop = np.zeros((8, 8), np.int8)
        black_bishop[0, 2] = 1
        black_bishop[0, 5] = 1
        black_knight = np.zeros((8, 8), np.int8)
        black_knight[0, 1] = 1
        black_knight[0, 6] = 1
        black_pawn = np.zeros((8, 8), np.int8)
        for i in range(0, 8):
            black_pawn[1, i] = 1

        # Stack
        expected = np.stack([white_king,
                             white_queen,
                             white_rook,
                             white_bishop,
                             white_knight,
                             white_pawn,
                             black_king,
                             black_queen,
                             black_rook,
                             black_bishop,
                             black_knight,
                             black_pawn], axis=0)

        initial_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        # Act
        actual = convert_fen_to_array(initial_fen)

        # Assert
        self.assertTrue(np.array_equal(actual, expected))

    def test_serialize_scholars_mate(self):
        # Arrange
        # White
        white_king = np.zeros((8, 8), np.int8)
        white_king[7, 4] = 1
        white_queen = np.zeros((8, 8), np.int8)
        white_queen[1, 5] = 1
        white_rook = np.zeros((8, 8), np.int8)
        white_rook[7, 0] = 1
        white_rook[7, 7] = 1
        white_bishop = np.zeros((8, 8), np.int8)
        white_bishop[7, 2] = 1
        white_bishop[4, 2] = 1
        white_knight = np.zeros((8, 8), np.int8)
        white_knight[7, 1] = 1
        white_knight[7, 6] = 1
        white_pawn = np.zeros((8, 8), np.int8)
        for i in [0, 1, 2, 3, 5, 6, 7]:
            white_pawn[6, i] = 1
        white_pawn[4, 4] = 1

        # Black
        black_king = np.zeros((8, 8), np.int8)
        black_king[0, 4] = 1
        black_queen = np.zeros((8, 8), np.int8)
        black_queen[0, 3] = 1
        black_rook = np.zeros((8, 8), np.int8)
        black_rook[0, 0] = 1
        black_rook[0, 7] = 1
        black_bishop = np.zeros((8, 8), np.int8)
        black_bishop[0, 2] = 1
        black_bishop[0, 5] = 1
        black_knight = np.zeros((8, 8), np.int8)
        black_knight[2, 2] = 1
        black_knight[2, 5] = 1
        black_pawn = np.zeros((8, 8), np.int8)
        for i in [0, 1, 2, 3, 6, 7]:
            black_pawn[1, i] = 1
        black_pawn[3, 4] = 1

        # Stack
        expected = np.stack([white_king,
                             white_queen,
                             white_rook,
                             white_bishop,
                             white_knight,
                             white_pawn,
                             black_king,
                             black_queen,
                             black_rook,
                             black_bishop,
                             black_knight,
                             black_pawn], axis=0)

        initial_fen = 'r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4'

        # Act
        actual = convert_fen_to_array(initial_fen)

        # Assert
        self.assertTrue(np.array_equal(actual, expected))

    def test_convert_piece_list_to_array_knights(self):
        # Arrange
        piece_position_list = [1, 6]  # Initial position for white knights

        # Act
        actual = convert_piece_list_to_array(piece_position_list)

        # Assert
        expected = np.zeros((8, 8))
        expected[7, 1] = 1
        expected[7, 6] = 1
        self.assertTrue(np.array_equal(actual, expected))

    def test_convert_piece_list_to_array_diagonal_pawns(self):
        # Arrange
        piece_position_list = [8, 17, 26, 35, 44, 53, 62, 55]  # diagonal white pawns

        # Act
        actual = convert_piece_list_to_array(piece_position_list)

        # Assert
        expected = np.zeros((8, 8))
        expected[0, 6] = 1
        expected[1, 5] = 1
        expected[2, 4] = 1
        expected[3, 3] = 1
        expected[4, 2] = 1
        expected[5, 1] = 1
        expected[6, 0] = 1
        expected[1, 7] = 1
        self.assertTrue(np.array_equal(actual, expected))

    def test_convert_win_to_1(self):
        # Arrange
        game_result = '1-0'

        # Act
        actual = convert_game_result_to_int(game_result)
        expected = 1

        # Assert
        self.assertEqual(actual, expected)

    def test_convert_tie_to_0(self):
        # Arrange
        game_result = '1/2-1/2'

        # Act
        actual = convert_game_result_to_int(game_result)
        expected = 0

        # Assert
        self.assertEqual(actual, expected)

    def test_convert_loss_to_negative_1(self):
        # Arrange
        game_result = '0-1'

        # Act
        actual = convert_game_result_to_int(game_result)
        expected = -1

        # Assert
        self.assertEqual(actual, expected)
