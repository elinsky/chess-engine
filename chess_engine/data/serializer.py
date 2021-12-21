import chess
import numpy as np

LAYERS = [(chess.WHITE, chess.KING),
          (chess.WHITE, chess.QUEEN),
          (chess.WHITE, chess.ROOK),
          (chess.WHITE, chess.BISHOP),
          (chess.WHITE, chess.KNIGHT),
          (chess.WHITE, chess.PAWN),
          (chess.BLACK, chess.KING),
          (chess.BLACK, chess.QUEEN),
          (chess.BLACK, chess.ROOK),
          (chess.BLACK, chess.BISHOP),
          (chess.BLACK, chess.KNIGHT),
          (chess.BLACK, chess.PAWN)]


def convert_fen_to_array(fen: str):
    """
    Given a FEN string that represents a chess game state, return a numpy array
    representing the game state. The resulting arrays is of shape (12, 8, 8).
    Each channel represents the presence of a piece (K, Q, R, B, N, P). The
    first six channels represent white's pieces; the second six are for black.
    The returns array is stacked as follows: wK, wQ, wR, wB, wN, wP, bK, bQ, bR,
    bB, bN, bP.

    As an example, this is what white's pawns look like at the start of the
    game:

    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    1 1 1 1 1 1 1 1
    0 0 0 0 0 0 0 0

    :param fen:
    :return: np array
    """

    board = chess.Board(fen=fen)
    piece_arrays = []
    for color, piece_type in LAYERS:
        piece_square_list = list(board.pieces(piece_type, color))
        piece_array = convert_piece_list_to_array(piece_square_list)
        piece_arrays.append(piece_array)

    return np.stack(piece_arrays, axis=0)


def convert_piece_list_to_array(piece_position_list: list[int]):
    """
    Takes as input a list of integers. Each integer represents the presence of a
    piece on a chess board. 0 = A1, 1 = B1, 2 = C1, ..., 7 = A2, ..., 63 = H8.
    Returns a 8x8 one-hot encoded numpy array indicating the presence or
    absence of pieces on the board. Most of the time you will want to pass in
    a list of integers for a single piece. E.g. [0, 8] will return the starting
    position of white's rooks:

    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    1 0 0 0 0 0 0 1

    :param piece_position_list: List[int] location of the pieces on the board.
    :return: 8x8 one-hot encoded numpy array.
    """
    piece_array = np.zeros((8, 8), np.int8)
    for piece in piece_position_list:
        row = 7 - (piece // 8)
        col = piece % 8
        piece_array[row, col] = 1

    return piece_array
