from model import Board


class AIPlayer:
    def __init__(self, game):
        self.game = game
        self.marker = 'O'
        self.opponent_marker = 'X'
        self.board = self.game.board.board
        self.make_move()

    def make_move(self):
        best_move = self.find_best_move()
        self.game.take_turn(self.marker, best_move)

    def find_best_move(self):
        """
        Find best move among available, using minimax on each available move.
        Returns the index of the best move.
        """
        available_moves = []
        for i, move in enumerate(self.board):
            if move.marker == '':
                board_copy = self.get_board_copy(self.board)
                board_copy.add_move('O', i)
                score = self.minimax(board_copy, self.opponent_marker, 1)
                available_moves.append(score)
            else:
                available_moves.append(None)
        best_move = available_moves.index(max(available_moves))
        return best_move

    def get_score(self, board):
        """
        Score a final board for minimax.
        Computer win: 1
        Opponent win: -1
        Draw: 0
        """
        if board.winner() == self.marker:
            return 1
        elif board.winner() == self.opponent_marker:
            return -1
        else:
            return 0

    def minimax(self, board, player, depth):
        """
        Search space of available moves for best-scoring move.
        https://en.wikipedia.org/wiki/Minimax
        """
        if board.is_full() or board.winner() or depth > 6:
            return self.get_score(board)

        if player == self.marker:
            other_player = self.opponent_marker
            fn = max
            best_score = -2

        elif player == self.opponent_marker:
            other_player = self.marker
            fn = min
            best_score = 2

        for i, slot in enumerate(board.board):
            if slot.marker == '':
                board.add_move(player, i)
                score = self.minimax(board, other_player, depth+1)
                board.remove_move(player, i)
                best_score = fn(best_score, score)

        return best_score

    def get_board_copy(self, board):
        board_copy = Board([item.marker for item in board])
        return board_copy
