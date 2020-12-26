from flask import *
import random
from Game import Game
from utilities import translator
from Coordinate import Coordinate

app = Flask(__name__)

board = [[0.24] * 9 for _ in range(9)]


@app.route('/button')
def hello_world():
    board = [[random.randint(1, 1000)] * 9 for _ in range(9)]
    return render_template('view.html', board=board, position=random.randint(1, 9), position2=random.randint(1, 9))


@app.route('/test')
def test():
    test_dic = {}
    test_dic['hello'] = 1
    board = [[random.randint(1, 1000)] * 9 for _ in range(9)]
    test_dic['board'] = board
    return jsonify(test_dic)


game = Game(9)
game.initiate_board()


@app.route('/board', methods=['GET'])
def show_board():
    return jsonify({'board': game.board})


@app.route('/board/update_time', methods=['GET'])
def update_board_time():
    game.update_board_with_time()
    return jsonify({'board': game.board})


@app.route('/board/update_sense/<int:board_cell>', methods=['POST'])
def update_board_with_sense(board_cell):
    scan_x, scan_y = translator(board_cell)
    sensor_color = game.update_with_sense(Coordinate(scan_x, scan_y))
    return jsonify({'board': game.board, 'color': sensor_color})


@app.route('/sense_ghost/<int:board_cell>', methods=['POST'])
def capture_ghost(board_cell):
    scan_x, scan_y = translator(board_cell)
    if int(scan_x) == game.ghost_position.x and int(scan_y) == game.ghost_position.y:
        return jsonify({'msg': 'GHOST IS BUSTED'})
    else:
        sensor_color = game.update_with_sense(Coordinate(int(scan_x), int(scan_y)))
        return jsonify({'board': game.board, 'color': sensor_color, 'msg': 'NO'})


@app.route('/sex', methods=["GET", "POST"])
def wtf():
    if request.method == "POST":
        b = [[random.randint(1, 1000)] * 9 for _ in range(9)]
        return render_template('view.html', board=b, position=random.randint(1, 10), position2=random.randint(1, 9))


if __name__ == '__main__':
    app.run()
