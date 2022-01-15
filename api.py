# %%
from dataclasses import dataclass
import numpy as np

# %%


@dataclass(init=True)
class Player:
    color: str
    player_id: int


@dataclass(init=True)
class Move:
    start: np.ndarray
    end: np.ndarray
    player: Player


# %%


class Board:
    """
    Board representation class.
        - 0 is an empty square.
        - -1 is not a sqare. on the board
    """

    def __init__(self):
        self.n = 17
        self.m = 26
        self.board = np.zeros([self.n, self.m], dtype='int')
        self.refresh_board()  # start up board
        self.board_dict = {(i, j): self.board[i][j] for i in range(
            self.n) for j in range(26) if self.board[i][j] != -1}

        self.legal_moves = np.array([])

        self.players = np.array([])

        # self.teams = ['black', 'blue', 'red', 'green', 'purple', 'yellow']

    def register_player(self, player: Player):
        id = len(self.players) + 1
        color = player.color
        if color not in self.players[:, 1]:
            self.players.append((id, player.color))

        return id

    def get_quadrant(quadrant: int):
        """
        Get grid with 1s in quadrant 'quadrant' and 0 elsewhere
        """
        pass

    def clear_board(self, fill=-1):
        for i in range(17):
            for j in range(26):
                self.board[i][j] = fill

    def refresh_board(self, blank=-1):
        self.clear_board(fill=blank)
        board = self.board

        n = 17
        m = 26
        indices = set({12})
        # build a triangle from the top
        for i in range(n-4):
            for j in range(m):
                if j in indices or board[i][j] == 0:
                    board[i][j] = 0
                else:
                    board[i][j] = blank

            indices = set({x-1 for x in indices}) | set({x+1 for x in indices})

        # build a triangle from the bottom
        indices = set({12})
        for i in range(n-1, 4-1, -1):
            for j in range(m-1, -1, -1):
                if j in indices or board[i][j] == 0:
                    board[i][j] = 0
                else:
                    board[i][j] = blank

            indices = set({x-1 for x in indices}) | set({x+1 for x in indices})

    def legal_moves(self):
        """
        takes a move and does the move if its legal, otherwise returns -1
        """
        pass

    def game_won(self):
        """
        returns -1 if game not yet won, and id of player who won the game if game is done.
        """
        pass


# %%
def clear_board(board, fill=-1):
    for i in range(17):
        for j in range(26):
            board[i][j] = fill
# %%


def refresh_board(board, blank=-1):
    clear_board(board, fill=blank)

    n = 17
    m = 26
    indices = set({12})
    # build a triangle from the top
    for i in range(n-4):
        for j in range(m):
            if j in indices or board[i][j] == 0:
                board[i][j] = 0
            else:
                board[i][j] = blank

        indices = set({x-1 for x in indices}) | set({x+1 for x in indices})

    # build a triangle from the bottom
    indices = set({12})
    for i in range(n-1, 4-1, -1):
        for j in range(m-1, -1, -1):
            if j in indices or board[i][j] == 0:
                board[i][j] = 0
            else:
                board[i][j] = blank

        indices = set({x-1 for x in indices}) | set({x+1 for x in indices})


# %%


class asciiBoard(Board):
    def __init__(self):
        Board.__init__(self)

    def __str__(self):
        s = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] != -1:
                    s.append(str(self.board[i][j]))
                else:
                    # s.append(str(self.board[i][j]))
                    s.append(' ')
                s.append(' ')
            s.append('\n')
        return "".join(s)

    def draw(self):
        print(self.__str__())

# %%


class Player:
    def __init__(self, color: str, board: Board, player_number: int):
        self.color = color
        self.board = board
        self.player_number = player_number

    def setup(self, quadrant):
        quadrant_indices = self.board.get_quadrant(quadrant)
        for (i, j), x in np.ndenumerate(quadrant_indices):
            if x == 1:
                self.board[i, j] = self.color

# %%


class asciiPlayer(Player):
    def __init__(self, color: str, board: Board):
        Player.__init__(self, color, board)

    def turn(self):
        valid_move = False
        while not valid_move:
            print(f"please pick a valid square.")
            print(f"pick a start square")
            start = input()
            try:
                start = np.array(eval(start))
            except:
                continue

            print(f"pick end square")
            end = input()
            try:
                end = np.array(eval(end))
            except:
                continue

            move = Move(start=start, end=end, color=self.color,
                        player_id=self.player_id)
            valid_move = move in self.board.legal_moves

# %%
