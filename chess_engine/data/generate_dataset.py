import io
from os.path import dirname
import argparse
import re
from random import randrange, seed
from typing import Tuple

import chess.pgn
import numpy as np

from chess_engine.data.exceptions import InvalidHalfMoveError
from chess_engine.data.serializer import convert_fen_to_array, \
    convert_game_result_to_int


def get_last_halfmove_number(game: chess.pgn.Game) -> int:
    # Get last move number
    last_move = str(game.end())  # e.g. '46. Ke4' or '28... Rxd2'
    p = re.compile(r'^(\d+)')  # get all digits at start of string
    last_move_number = int(p.match(last_move).group())

    # Did white or black move last?
    q = re.compile(r'(\w+)\.{3,}')  # ellipsis indicates black makes last move
    is_black = bool(q.match(last_move))

    # Calculate last halfmove number
    if is_black:
        last_halfmove_number = last_move_number * 2
    else:
        last_halfmove_number = last_move_number * 2 - 1

    return last_halfmove_number


def sample_game_state_result(game: chess.pgn.Game, halfmove_num: int) \
        -> Tuple[str, str]:
    """
    Given a chess.pgn.Game object and a halfmove number, returns the FEN string
    of the game after halfmove_num has been played, along with the result of
    the game. For the results:

    '1-0' = white wins
    '0-1' = black wins
    '1/2-1/2' = draw
    '*' = unfinished game

    :param game: A chess.pgn.Game object.
    :param halfmove_num: halfmove number for the desired state.
    :return: Tuple[FEN: str, game result: int]
    """

    # Get last halfmove number
    last_halfmove_number = get_last_halfmove_number(game)

    # Check if desired half-move number is valid
    if halfmove_num < 0 or halfmove_num > last_halfmove_number:
        raise InvalidHalfMoveError('Halfmove number:', halfmove_num, 'is \
        outside the valid range')

    # Get game result
    result = game.headers['Result']

    # Get fen
    while halfmove_num > 0:
        game = game.next()
        halfmove_num -= 1
    fen = game.board().fen()

    return fen, result


def sample_random_game_state_result(game: chess.pgn.Game) -> Tuple[str, str]:
    last_halfmove_number = get_last_halfmove_number(game)
    state_num = randrange(1, last_halfmove_number)
    fen, result = sample_game_state_result(game, state_num)
    return fen, result


def extract_game(pgn_file):
    """
    Generates chess.pgn.game objects from a file with multiple chess games in
    PGN format.

    :param pgn_file: File with multiple PGNs. Each PGN should be separated by a
    single newline character. And the file should end with 2 newline characters.
    :return: Returns an iterator. Each call to next() will return a
    chess.pgn.game object.
    """
    with open(pgn_file, 'r') as file:
        current_pgn = ''
        newline_count = 0
        for line in file:
            current_pgn += line
            if line == '\n':
                newline_count += 1
            if newline_count == 2:  # end of PGN
                pgn_io = io.StringIO(current_pgn)
                yield chess.pgn.read_game(pgn_io)
                current_pgn = ''
                newline_count = 0


def print_dataset_status(max_n):
    if max_n % 1000 == 0:
        print(max_n, 'games left to extract.')


def create_state_result_dataset(dataset_filename, max_n=None):
    """
    Given a file with multiple PGNs, selects a random state in each PGN,
    converts the state to a numpy array, and returns the array along with the
    game outcome.
    :param dataset_filename: File with multiple PGNs. Each PGN should be separated by
    a single newline character. And the file should end with 2 newline
    characters.
    :param max_n: Max number of games to extract.
    :return: Tuple[np array, np array]
    """

    x_list = []
    y_list = []

    for game in extract_game(dataset_filename):
        fen, game_result = sample_random_game_state_result(game)

        # Filter out draws and incomplete games
        if game_result in {'1/2-1/2', '*'}:
            continue

        array = convert_fen_to_array(fen)
        game_result_int = convert_game_result_to_int(game_result)

        x_list.append(array)
        y_list.append(game_result_int)

        if max_n:
            max_n -= 1
            print_dataset_status(max_n)
            if max_n == 0:
                break

    x = np.stack(x_list, axis=0)
    y = np.stack(y_list, axis=0)

    return x, y


if __name__ == '__main__':
    # TODO - add an overall description.
    parser = argparse.ArgumentParser(description='Converts a clean PGN file'
                                                 'containing multiple PGNs into '
                                                 'a dataset for supervised learning.')
    # ../chess-engine/data/cleaned/clean_dataset.pgn
    clean_dataset_path = dirname(dirname(dirname(__file__))) + '/data/cleaned/clean_dataset.pgn'
    parser.add_argument("--clean_dataset_path",
                        default=clean_dataset_path,
                        help='The absolute path to the clean_dataset.pgn file. '
                             'This should be the output from  clean_dataset.sh')
    # ../chess-engine/data/features/
    target_dir = dirname(dirname(dirname(__file__))) + '/data/features/'
    parser.add_argument('--target_dir',
                        default=target_dir,
                        help='directory to place the numpy features and labels.')
    parser.add_argument("--max_n",
                        default=None,
                        type=int,
                        help='Max number of games to parse and output into the '
                             'numpy dataset.')
    args = parser.parse_args()
    x, y = create_state_result_dataset(args.clean_dataset_path,
                                       max_n=args.max_n)
    np.save(target_dir + 'x.npy', x)
    np.save(target_dir + 'y.npy', y)
