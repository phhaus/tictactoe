import logging

import gym
import numpy as np
from gym import spaces

'''
Utilities
'''
GAME_TITLE = 'TicTacToe'
SIZE = 9
O_REWARD = 1
X_REWARD = -1
NO_REWARD = 0
START_MARK = 'O'
tokens = {0: ' ', 1: 'O', 2: 'X'}
LEFT_PAD = '  '
LOG_FMT = logging.Formatter('%(levelname)s '
                            '[%(filename)s:%(lineno)d] %(message)s',
                            '%Y-%m-%d %H:%M:%S')


def next_mark(mark):
    return 'X' if mark == 'O' else 'O'


def agent_by_mark(agents, mark):
    for agent in agents:
        if agent.mark == mark:
            return agent


def to_token(code: int):
    return tokens[code]


def to_code(token: str):
    return 1 if token == 'O' else 2


def check_game_status(board):
    '''Return game status by current board status.
    Args:
        board (list): Current board state
    Returns:
        int:
            -1: game in progress
            0: draw game,
            1 or 2 for finished game(winner mark code).
    '''
    for t in [1, 2]:
        for j in range(0, SIZE, 3):
            if [t] * 3 == [board[i] for i in range(j, j + 3)]:
                return t
        for j in range(0, 3):
            if board[j] == t and board[j + 3] == t and board[j + 6] == t:
                return t
        if board[0] == t and board[4] == t and board[8] == t:
            return t
        if board[2] == t and board[4] == t and board[6] == t:
            return t

    for i in range(SIZE):
        if board[i] == 0:
            # still playing
            return -1

    # draw game
    return 0


def next_mark(mark):
    return 'X' if mark == 'O' else 'O'


'''
Enviroment for game
'''


class TicTacToe(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(SIZE)
        self.observation_space = spaces.Discrete(SIZE)
        self.seed()
        self.reset()

    def reset(self):
        self.board = np.zeros(SIZE)
        self.mark = START_MARK
        self.done = False
        return self._get_obs()

    def step(self, action: int):
        """Step environment by action.
               Args:
                   action (int): Location
               Returns:
                   list: Obeservation
                   int: Reward
                   bool: Done
                   dict: Additional information
        """
        assert self.action_space.contains(action)
        loc = action
        if self.done:
            return self._get_obs(), 0, True, None

        reward = NO_REWARD
        # update bord
        self.board[loc] = to_code(self.mark)

        # check if game has ended
        status = check_game_status(self.board)
        if status >= 0:
            self.done = True
            if status in [1, 2]:
                reward = O_REWARD if self.mark == 'O' else X_REWARD

        # update mark
        self.mark = next_mark(self.mark)

        return self._get_obs(), reward, self.done, None

    def _get_obs(self):
        return (self.board, self.mark)

    def render(self, close=False):
        print("a")
        if close:
            return
        self._show_board()

    def show_episode(self, human, episode):
        self._show_episode(print if human else logging.warning, episode)

    def _show_episode(self, episode):
        print("==== Episode {} ====".format(episode))

    def _show_board(self):
        '''Draw tictactoe board.'''
        for j in range(0, 9, 3):
            print('-------')
            for i in range(3):
                print('|' + to_token(self.board[i + j]), end='')
            print('|')
        print('-------')

    def show_turn(self, mark):
        self._show_turn(mark)

    def _show_turn(self, mark):
        print("{}'s turn.".format(mark))

    def show_result(self, mark, reward):
        self._show_result(mark, reward)

    def _show_result(self, mark, reward):
        status = check_game_status(self.board)
        assert status >= 0
        if status == 0:
            print("==== Finished: Draw ====")
        else:
            msg = "Winner is '{}'!".format(to_token(status))
            print("==== Finished: {} ====".format(msg))
        print('')

    def available_actions(self):
        return [i for i, c in enumerate(self.board) if c == 0]
