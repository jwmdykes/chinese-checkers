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
        self.m = 25
        self.board = [['NULL' for _ in range(self.m)] for _ in range(self.n)]
        self.refresh_board()  # start up board
        self.board_dict = {(i, j): self.board[i][j] for i in range(
            self.n) for j in range(self.m) if self.board[i][j] != 'NULL'}
        # quadrant definitions. Starts at 6 o'clock, 12 o'clock, 4, 10, 3, 7
        # dictionary with keys as quadrant number keys,
        # for example (0, 12, 1, 0) means the quadrant starts at (0, 12) and moves down but not left or right
        self.quadrants = {
            0: (0, 12, (1, -1), (1, 1)),
            1: (16, 12, (-1, -1), (-1, 1)),
            2: (12, 24, (0, -2), (-1, -1)),
            3: (4, 0, (0, 2), (1, 1)),
            4: (4, 24, (0, -2), (1, -1)),
            5: (12, 0, (0, 2), (-1, 1))
        }
        self.valid_colors = {'blue': 'b', 'green': 'g', 'purple': 'p',
                             'red': 'r', 'orange': 'o', 'yellow': 'y', 'white': 'w', 'black': 'B'}
        self.taken_colors = {}

        self.legal_moves = np.array([])

        self.players = []
        self.turn = None  # player whose turn it is

    def register_player(self, color: str):
        id = len(self.players) + 1
        if id <= 5 and color not in self.taken_colors and color in self.valid_colors:
            player = Player(color=color, board=self.board, id=id)
            self.players.append(player)
            self.taken_colors[color] = True
            return player
        else:
            return -1

    def get_quadrant(self, quadrant: int):
        """
        Get grid with 1s in quadrant 'quadrant' and 0 elsewhere
        """
        quad_index = []
        quadrants = self.quadrants
        start = quadrants[quadrant][0:2]
        d1 = np.array(quadrants[quadrant][2])
        d2 = np.array(quadrants[quadrant][3])
        indices = set({start})
        for i in range(4):
            quad_index.extend(indices)
            indices = set({tuple(np.array(x)+d1) for x in indices}
                          ) | set({tuple(np.array(x)+d2) for x in indices})

        return quad_index

    def fill_region(self, region, fill):
        """
        fill region (list of tuples) with fill (string)
        """
        for i, j in region:
            self.board[i][j] = fill

    def fill_quadrant(self, quadrant, fill):
        """
        fill quadrant (index from 0 to 5) with fill (string)
        """
        region = self.get_quadrant(quadrant=quadrant)
        self.fill_region(region=region, fill=fill)

    def clear_board(self, fill='NULL'):
        """
        clears board. does not clear players
        """
        for i in range(self.n):
            for j in range(self.m):
                self.board[i][j] = fill

    def refresh_board(self, blank='NULL', symbol='0'):
        self.clear_board(fill=blank)
        board = self.board

        n = self.n
        m = self.m
        indices = set({12})
        # build a triangle from the top
        for i in range(n-4):
            for j in range(m):
                if j in indices or board[i][j] == symbol:
                    board[i][j] = symbol
                else:
                    board[i][j] = blank

            indices = set({x-1 for x in indices}) | set({x+1 for x in indices})

        # build a triangle from the bottom
        indices = set({12})
        for i in range(n-1, 4-1, -1):
            for j in range(m-1, -1, -1):
                if j in indices or board[i][j] == symbol:
                    board[i][j] = symbol
                else:
                    board[i][j] = blank

            indices = set({x-1 for x in indices}) | set({x+1 for x in indices})

    def start_game_board(self):
        """
        Setup game board with current players
        """
        if not self.players:
            # need at least 1 palyer
            return -1

        self.refresh_board()  # start up board
        for player in self.players:
            self.fill_quadrant(
                quadrant=player.id, fill=self.valid_colors[player.color])

        self.turn = 0

    def move(self, move: Move):
        """
        do a move on the board
        """
        pass

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


class asciiBoard(Board):
    def __init__(self):
        Board.__init__(self)

    def __str__(self):
        s = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] != 'NULL':
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
    def __init__(self, color: str, board: Board, id: int):
        self.color = color
        self.board = board
        self.id = id

    def move():
        """
        Do a move. Check that it's your turn, and that the move is valid. 
        """
        pass


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
board = asciiBoard()
quadrant = 3
region = board.get_quadrant(quadrant)
board.fill_region(region, quadrant)
print(board)

# %%
player1 = board.register_player(color='blue')
player2 = board.register_player(color='red')
# %%
board.start_game_board()
# %%
print(board)
# %%
