import flask
import os

from model import Game
from AIPlayer import AIPlayer

app = flask.Flask(__name__)


@app.route('/')
def board():
    game = Game()
    game_board = game.board.board
    return flask.render_template('board.html',
                                 game_board=game_board)


@app.route('/move/<int:move_id>', methods=['POST'])
def make_move(move_id):
    board_data = flask.request.form
    board_state = [board_data[str(i)] for i in range(9)]

    game = Game(board_state)
    try:
        game.take_turn('X', move_id)
        AIPlayer(game)
        new_board_state = game.serialize()
        return flask.jsonify(new_board_state)

    except ValueError:
        return ('Move not allowed', 405)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000))
            )
