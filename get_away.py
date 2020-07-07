#!/usr/bin/env python3

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from random import randint
from maps import *
import os


# import levels
levels = [MapOne, MapTwo, MapThree, MapFour, MapFive]


# processes pathfinding, draws game frame
def frame(level, new, end, win):

    # set up map with nodes
    matrix = level
    grid = Grid(matrix=matrix)
    starts = grid.node(new[0], new[1])
    ends = grid.node(end[0], end[1])
    wins = grid.node(win[0], win[1])

    # pathfinding for NPC AI
    finder = AStarFinder()
    path, runs = finder.find_path(starts, ends, grid)

    # print frame and get open spaces
    print(grid.grid_str(path=path, start=starts, end=ends, win=wins)[0])
    walkable = grid.grid_str(path=path, start=starts, end=ends, win=wins)[1]


    # gives the NPC a random chance of moving 0, 1, or 2
    # spaces along the path, and returns new position of npc
    # and list of open spaces
    rand3 = randint(0,3)
    try:
        locale = path[rand3]
        return locale, walkable
    except IndexError:
        try:
            return path[2], walkable

        # loose logic
        except IndexError:
            print('\n[*]Ninja you got caught.[*]\n')
            quit()



def controls(direction):

    # switch function for user input
    thing = {"w": (0, -1),
             "s": (0, +1),
             "d": (+1, 0),
             "a": (-1, 0),
             "n": (0, 0)
            }
    return thing[direction.lower()]


def move(player, npc):

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
    move_to =  tuple(map(sum,zip(controls(direction), player)))
    if move_to in npc:
        return move_to
    else:
        return player


# main game loop
def main_loop(levels):

    # setup random level
    level = levels[randint(0,4)]
    level_map = level().matrix
    npc = [level().start] 
    player = level().end
    win = level().win

    # win logic
    while True:
        if player == win:
            print('\n[*]Ninja you won.[*]\n')
            input()
            break

        # clear screen and draw new frame
        os.system('cls' if os.name == 'nt' else 'clear')
        npc = frame(level_map, npc[0], player, win)
        player = move(player, npc[1])


if __name__ == '__main__':

    # print welcome screen
    print('\nA game. You are the $. Girlfriend is the &. Run to the @.')
    print('Use wads to move (press return after choice), press q to quit.')
    print('Dotted line is the path your girlfriend plans to take to get you.')
    print('Get to the exit (@) before she hits you with a shoe.')
    print('Press return to start the game.')
    input()

    # run main game loop
    while True:
        try:
            main_loop(levels)
        except KeyboardInterrupt:
            print()
            quit()

