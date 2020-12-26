from Game import Game
import pprint
from Coordinate import Coordinate

if __name__ == '__main__':
    game = Game(9)
    game.initiate_board()
    game.print_board()

    while True:
        print('1. Advance Time 2. Scan 3. Bust The Ghost')
        choice = input('choose: ')
        if choice == '1':
            game.update_board_with_time()
            game.print_board()
        elif choice == '2':
            scan_x, scan_y = input('Enter coordinate for scanning: ').split(',')
            game.update_with_sense(Coordinate(int(scan_x), int(scan_y)))
        elif choice == '3':
            scan_x, scan_y = input('Enter coordinate for Busting: ').split(',')
            if int(scan_x) == game.ghost_position.x and int(scan_y) == game.ghost_position.y:
                print('Ghost is busted!!')
                break
            else:
                print('Could not bust ghost! Rescanning the cell.')
                game.update_with_sense(Coordinate(int(scan_x), int(scan_y)))



