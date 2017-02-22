class Slot:
    def __init__(self, idx, marker=''):
        self.idx = idx
        self.marker = marker
        self.winning = False

    def __repr__(self):
        info = str(self.idx) + ': ' + self.marker
        return info


class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = [Slot(i) for i in range(9)]
        elif type(board) == list:
            self.board = [Slot(i, marker) for i, marker in enumerate(board)]
        elif isinstance(board, Board):
            self = board

    def add_move(self, marker, move):
        if self.validate_move(move):
            self.board[move].marker = marker
        else:
            raise ValueError("That's not a valid move.")

    def remove_move(self, marker, move):
        if self.board[move].marker == marker:
            self.board[move].marker = ''
        else:
            raise ValueError("No turn to remove.")

    def is_full(self):
        for slot in self.board:
            if slot.marker == '':
                return False
        return True

    def winner(self):
        win_indices = [[0, 1, 2],
                       [3, 4, 5],
                       [6, 7, 8],
                       [0, 3, 6],
                       [1, 4, 7],
                       [2, 5, 8],
                       [0, 4, 8],
                       [2, 4, 6]]

        for idx_set in win_indices:
            markers = [self.board[idx].marker for idx in idx_set]
            if len(set(markers)) == 1 and markers[0] != '':
                for idx in idx_set:
                    self.board[idx].winning = True
                return markers[0]

    def validate_move(self, move):
        if self.board[move].marker == '':
            return True
        else:
            return False


class Game:
    def __init__(self, board=None, ):
        if board is None:
            self.board = Board()
        else:
            self.board = Board(board)
        self.players = ['X', 'O']
        self.turn = self.whose_turn()

    def whose_turn(self):
        move_counts = {'X': 0, 'O': 0}
        for slot in self.board.board:
            if slot.marker != '':
                move_counts[slot.marker] += 1
        if move_counts['X'] == move_counts['O']:
            return 'X'
        elif move_counts['X'] > move_counts['O']:
            return 'O'

    def take_turn(self, player, move):
        if player != self.turn:
            raise ValueError("Wrong player's turn")
        if not self.check_winner() and not self.check_tie():
            try:
                self.board.add_move(player, move)
                self.turn = self.whose_turn()
            except ValueError:
                return

        return self.board_state()

    def board_state(self):
        self.check_winner()
        self.check_tie()
        return self.board

    def check_winner(self):
        return self.board.winner()

    def check_tie(self):
        return self.board.is_full()

    def serialize(self):
        output = {
            'winner': self.check_winner(),
            'tie': str(self.check_tie()),
            'board_state': []
            }

        for slot in self.board.board:
            slot_dict = {
                'marker': slot.marker,
                'winning': slot.winning
                }
            output['board_state'].append(slot_dict)
        return output
