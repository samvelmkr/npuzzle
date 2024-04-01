#!/usr/bin/env python3
from enum import Enum
from search import *


class Tiles(State):
    EMPTY_TILE = 0

    def __init__(self, tiles=None):
        if tiles:
            self.width = len(tiles)
            self._tiles = [0] * (self.width * self.width)
            empty_row = -1
            empty_col = -1
            index = 0
            for row in range(0, self.width):
                for col in range(0, self.width):
                    tile = tiles[row][col]
                    if tile == self.EMPTY_TILE:
                        empty_row = row
                        empty_col = col
                    self._tiles[index] = tile
                    index += 1
            self.empty_tile_row = empty_row
            self.empty_tile_col = empty_col

    def _init(self, width, tiles, empty_tile_row, empty_tile_col):
        self.width = width
        self._tiles = tiles
        self.empty_tile_row = empty_tile_row
        self.empty_tile_col = empty_tile_col

    def get_tile(self, row, col):
        return self._tiles[row * self.width + col]

    def get_applicable_actions(self):
        actions = set()
        for movement in Movement:
            new_empty_tile_row = self.empty_tile_row + movement.delta_row
            new_empty_tile_col = self.empty_tile_col + movement.delta_col
            if (0 <= new_empty_tile_row and new_empty_tile_row < self.width and
                    0 <= new_empty_tile_col and new_empty_tile_col < self.width):
                actions.add(movement)
        return actions

    def get_action_result(self, movement):
        new_empty_tile_row = self.empty_tile_row + movement.delta_row
        new_empty_tile_col = self.empty_tile_col + movement.delta_col
        new_tiles = self._tiles.copy()
        new_tiles[self.empty_tile_row * self.width + self.empty_tile_col] = self.get_tile(new_empty_tile_row,
                                                                                          new_empty_tile_col)
        new_tiles[new_empty_tile_row * self.width + new_empty_tile_col] = self.EMPTY_TILE
        result = Tiles(None)
        result._init(self.width, new_tiles, new_empty_tile_row, new_empty_tile_col)
        return result

    def __eq__(self, other):
        if not isinstance(other, Tiles):
            return False
        return self._tiles == other._tiles

    def __hash__(self):
        return hash(tuple(self._tiles))


class Movement(Action, Enum):
    UP = (-1, 0)
    LEFT = (0, -1)
    DOWN = (1, 0)
    RIGHT = (0, 1)

    def __init__(self, delta_row, delta_col):
        self.delta_row = delta_row
        self.delta_col = delta_col


class TilesGoalTest(GoalTest):
    def is_goal(self, tiles):
        last_tile_index = tiles.width * tiles.width - 1
        for index in range(last_tile_index, 0, -1):
            if tiles._tiles[index - 1] != index:
                return False
        return tiles._tiles[last_tile_index] == Tiles.EMPTY_TILE


class NPuzzlePrinting(Printing):
    @staticmethod
    def print_action(movement):
        print('move ', movement.name, sep='', end='')

    @staticmethod
    def print_state(tiles):
        width = tiles.width
        cell_length = len(str(width * width))
        print('-', end='')
        for col in range(0, width):
            print('-' * (cell_length + 3), end='')
        print()
        for row in range(0, width):
            print('|', end='')
            for col in range(0, width):
                print(' ', end='')
                if row == tiles.empty_tile_row and col == tiles.empty_tile_col:
                    print(' ' * cell_length, end='')
                else:
                    cell = str(tiles.get_tile(row, col))
                    print(' ' * (cell_length - len(cell)), end='')
                    print(cell, end='')
                print(' |', end='')
            print()
            print('-', end='')
            for col in range(0, width):
                print('-' * (cell_length + 3), end='')
            print()


def BFTS_demo():
    print('This is a demonstration of breadth-first tree search on 8-puzzle')
    print()

    initial_configuration = Tiles([
        [7, 4, 2],
        [8, 1, 3],
        [5, 0, 6]
    ])

    goal_test = TilesGoalTest()
    solution = IterativeDeepeningTreeSearch().find_solution(initial_configuration, goal_test)
    NPuzzlePrinting.print_solution(solution)


if __name__ == '__main__':
    BFTS_demo()
