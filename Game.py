from Coordinate import Coordinate
import pprint
import random
from copy import deepcopy
import numpy as np

SIDEWAYS_MOVE_PROB = 0.8
DIAGONAL_MOVE_PROB = 1 - SIDEWAYS_MOVE_PROB
SELF_POS_PROB = 0.2
ROUND_UPTO = 3

DIAGONAL_TYPE = 'DIAGONAL'
SIDE_TYPE = 'SIDE'
SELF = 'SELF'
RED = 'RED'
ORANGE = 'ORANGE'
GREEN = 'GREEN'


class Game:
    def __init__(self, grid_size):
        self.board = []
        self.row = grid_size
        self.column = grid_size
        self.ghost_position = None
        self.max_manhattan_distance = 2 * self.row - 1

    def initiate_board(self) -> None:
        """
        Initiating the board with equal probability 
        :return: void
        """
        self.board = [[round(1 / (self.row * self.row), 3)] * self.column for _ in range(self.row)]
        self.ghost_position = Coordinate(random.randint(0, self.row - 1), random.randint(0, self.row - 1))

    def print_board(self) -> None:
        """
        Prints the whole board
        """
        pprint.pprint(self.board)
        # pprint.pprint(f"The ghost is in position: {self.ghost_position}")

    def move_ghost(self) -> Coordinate:
        random_num = random.uniform(0, 1)

        neighbors = self.find_valid_neighbors(self.ghost_position)

        side_neighbors, side_neighbors_count, \
        other_neighbors, other_neighbors_count = self.get_neighbor_information(self.ghost_position, neighbors)

        if random_num >= SIDEWAYS_MOVE_PROB:
            self.move_ghost_helper(other_neighbors_count, other_neighbors)
        else:
            self.move_ghost_helper(side_neighbors_count, side_neighbors)

        # pprint.pprint(f'The ghost moved to {self.ghost_position}')
        return self.ghost_position

    def move_ghost_helper(self, neighbors_count, neighbors):
        neighbor_to_move = random.randint(0, neighbors_count - 1)
        self.ghost_position.x = neighbors[neighbor_to_move].x
        self.ghost_position.y = neighbors[neighbor_to_move].y

    def update_board_with_time(self) -> None:

        original_board = deepcopy(self.board)
        normalizer = 0

        for row in range(self.row):
            for col in range(self.column):
                temp_prob = 0
                current_coord = Coordinate(row, col)
                neighbors = self.find_valid_neighbors(current_coord)

                for neighbor in neighbors:
                    transition_prob = self.calc_transition_prob(current_coord, neighbor)
                    # print(f'transition: {transition_prob}')
                    neighbor_prob = original_board[neighbor.x][neighbor.y]
                    # print(f'neighbor_prob: {neighbor_prob}')
                    temp_prob += transition_prob * neighbor_prob
                    # print(f'temp: {temp_prob}')

                self.board[row][col] = temp_prob
                normalizer += temp_prob

        self.board = np.round(np.array(self.board) / normalizer, decimals=ROUND_UPTO).tolist()

        self.move_ghost()
        # print(sum([self.board[row][col] for col in range(self.column) for row in range(self.row)]))

    def get_neighbor_information(self, source, neighbors):
        side_neighbors = [neighbor for neighbor in neighbors
                          if self.find_neighbor_type(source, neighbor) == SIDE_TYPE]
        other_neighbors = [neighbor for neighbor in neighbors
                           if self.find_neighbor_type(source, neighbor) != SIDE_TYPE]

        side_neighbors_count = len(side_neighbors)
        other_neighbors_count = len(other_neighbors)

        return side_neighbors, side_neighbors_count, other_neighbors, other_neighbors_count

    def update_with_sense(self, sense_coordinate) -> str:

        sensed_color = self.sensor_color(sense_coordinate, self.ghost_position)
        print(f'SENSOR READING: {sensed_color}')
        original_board = deepcopy(self.board)
        normalizer = 0

        for row in range(self.row):
            for col in range(self.column):
                if self.sensor_color(sense_coordinate, Coordinate(row, col)) == sensed_color:
                    emission_prob = 1
                else:
                    emission_prob = 0
                current_cell_prob = original_board[row][col]
                self.board[row][col] = emission_prob * current_cell_prob
                normalizer += self.board[row][col]

        # print(f'normalizer: {normalizer}')

        self.board = np.round(np.array(self.board) / normalizer, decimals=ROUND_UPTO).tolist()
        # print(sum([self.board[row][col] for col in range(self.column) for row in range(self.row)]))
        self.print_board()

        return sensed_color

    def calc_transition_prob(self, to: Coordinate, _from: Coordinate) -> float:

        neighbors = self.find_valid_neighbors(_from)
        side_neighbors, side_neighbors_count, \
        other_neighbors, other_neighbors_count = self.get_neighbor_information(_from, neighbors)

        destination_type = self.find_neighbor_type(_from, to)

        if destination_type == SIDE_TYPE:
            return SIDEWAYS_MOVE_PROB / side_neighbors_count
        else:
            return DIAGONAL_MOVE_PROB / (other_neighbors_count + 1)

    def find_valid_neighbors(self, cell: Coordinate):
        all_possible_neighbors = [
            Coordinate(cell.x, cell.y),
            Coordinate(cell.x - 1, cell.y),
            Coordinate(cell.x + 1, cell.y),
            Coordinate(cell.x, cell.y - 1),
            Coordinate(cell.x, cell.y + 1),
            Coordinate(cell.x - 1, cell.y - 1),
            Coordinate(cell.x + 1, cell.y + 1),
            Coordinate(cell.x - 1, cell.y + 1),
            Coordinate(cell.x + 1, cell.y - 1),
        ]

        return list(filter(self.is_valid_coordinate, all_possible_neighbors))

    def is_valid_coordinate(self, coord: Coordinate):
        if coord.x < 0 or coord.x >= self.row or coord.y < 0 or coord.y >= self.column:
            return False
        return True

    @staticmethod
    def find_neighbor_type(source: Coordinate, neighbor: Coordinate):
        if (neighbor.x == source.x and neighbor.y != source.y) or (neighbor.x != source.x and neighbor.y == source.y):
            return SIDE_TYPE
        elif neighbor.x == source.x and neighbor.y == source.y:
            return SELF
        return DIAGONAL_TYPE

    @staticmethod
    def sensor_color(sense_coordinate, ghost_pos) -> str:
        real_intermediate_dist = sense_coordinate.calculate_manhatten_distance(ghost_pos)
        if real_intermediate_dist <= 3:
            return RED
        elif 3 < real_intermediate_dist <= 6:
            return ORANGE
        elif real_intermediate_dist > 6:
            return GREEN
