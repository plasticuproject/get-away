#!/usr/bin/env python3

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from random import randint
from maps import *
import os


# import levels
levels = [MapOne, MapTwo, MapThree, MapFour, MapFive]


# processes pathfinding, draws game frame
def frame(level, start, end, win):

    # set up map with nodes
    matrix = level
    grid = Grid(matrix=matrix)
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])
    win = grid.node(win[0], win[1])

    # pathfinding for NPC AI
    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    # print frame
    print(grid.grid_str(path=path, start=start, end=end, win=win))

    # return new position of NPC
    return path[1]


def controls(direction):

    # switch function for user input
    thing = {"w": (0, -1),
             "s": (0, +1),
             "d": (+1, 0),
             "a": (-1, 0),
             "n": (0, 0)
            }
    return thing[direction.lower()]


def move(y):

    # user input
    valid_d = ['w', 's', 'd', 'a', '']
    direction = input('[*]Your move: ')

    # game escape
    if direction.lower() == 'q' or direction.lower() == 'quit':
        quit()

    # process user move
    while direction not in valid_d:
        print('[*]Please use "w, s, d, a, or just press enter to stay in place.[*]')
        direction = input('[*]Your move: ')
    if direction == '':
        direction = 'n'
    return tuple(map(sum,zip(controls(direction), y)))


# main game loop
def main_loop(levels):

    # setup random level
    level = levels[randint(0,4)]
    level_map = level().matrix
    x = level().start
    y = level().end
    win = level().win
    back_y = y

    # win/loose logic
    while True:
        if x == y:
            print('\n[*]Ninja you got caught.[*]\n')
            quit()
        if y == win:
            print('\n[*]Ninja you won.[*]\n')
            input()
            break

        try:
            # clear screen and draw new frame
            os.system('cls' if os.name == 'nt' else 'clear')
            x = frame(level_map, x, y, win)
        except IndexError:
            # colision detection for border and walls
            # will waste a user turn
            os.system('cls' if os.name == 'nt' else 'clear')
            x = frame(level_map, x, back_y, win)
            y = back_y
        back_y = y
        y = move(y)


if __name__ == '__main__':

    while True:

        # run main game loop
        print('\nA game. You are the $. Girlfriend is the &. Run to the @.')
        print('Use wads to move (press return after choice), press q to quit.')
        print('Dotted line is the path your girlfriend plans to take to get you.')
        print('Get to the exit (@) before she hits you with a shoe.')
        print('Press return to start the game.')
        input()
        try:
            main_loop(levels)
        except KeyboardInterrupt:
            print()
            quit()

