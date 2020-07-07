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
    start = grid.node(new[0], new[1])
    end = grid.node(end[0], end[1])
    win = grid.node(win[0], win[1])

    # pathfinding for NPC AI
    #finder = AStarFinder()
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    # print frame
    print(grid.grid_str(path=path, start=start, end=end, win=win)[0])
    walkable = grid.grid_str(path=path, start=start, end=end, win=win)[1]


    # return new position of NPC
    # TODO this is buggy, crashes near boarders, needs fixed
    try:
        if path[1][0] == new[0] and path[1][1] == new[1] - 1:
            if (new[0], new[1] - 2) in walkable:
                return (new[0], new[1] - 2), walkable
            else:
                return path[1], walkable
        elif path[1][1] == new[1] and path[1][0] == new[0] - 1:
            if (new[0] - 2, new[1]) in walkable:
                return (new[0] - 2, new[1]), walkable
            else:
                return path[1], walkable
        elif path[1][0] == new[0] and path[1][1] == new[1] + 1:
            if (new[0], new[1] + 2) in walkable:
                return (new[0], new[1] + 2), walkable
            else:
                return path[1], walkable
        elif path[1][1] == new[1] and path[1][0] == new[0] + 1:
            if (new[0] + 2, new[1]) in walkable:
                return (new[0] + 2, new[1]), walkable
            else:
                return path[1], walkable
        else:
            return path[1], walkable
    except IndexError:
        return path[0], walkable


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
    npc = [] 
    npc.append(level().start)
    player = level().end
    win = level().win
    back_player = player

    # win/loose logic
    while True:
        if npc[0] == player:
            print('\n[*]Ninja you got caught.[*]\n')
            quit()
        if player == win:
            print('\n[*]Ninja you won.[*]\n')
            input()
            break

        # clear screen and draw new frame
        os.system('cls' if os.name == 'nt' else 'clear')
        npc = frame(level_map, npc[0], player, win)
        player = move(player, npc[1])


if __name__ == '__main__':

    # run main game loop
    print('\nA game. You are the $. Girlfriend is the &. Run to the @.')
    print('Use wads to move (press return after choice), press q to quit.')
    print('Dotted line is the path your girlfriend plans to take to get you.')
    print('Get to the exit (@) before she hits you with a shoe.')
    print('Press return to start the game.')
    input()

    while True:
        try:
            main_loop(levels)
        except KeyboardInterrupt:
            print()
            quit()

