# -*- coding: utf-8 -*-
from .node import Node
import os

try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False
from pathfinding.core.diagonal_movement import DiagonalMovement

if os.name == 'nt':
    green = ''
    red = ''
    blue = ''
    yellow = ''
    endc = ''
else:
    green = '\033[32m'
    red = '\033[31m'
    blue = '\033[34m'
    yellow = '\033[33m'
    endc = '\033[m'

def build_nodes(width, height, matrix=None, inverse=False):
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.
    :rtype : list
    """
    nodes = []
    use_matrix = (isinstance(matrix, (tuple, list))) or \
        (USE_NUMPY and isinstance(matrix, np.ndarray) and matrix.size > 0)

    for y in range(height):
        nodes.append([])
        for x in range(width):
            # 1, '1', True will be walkable
            # while others will be obstacles
            # if inverse is False, otherwise
            # it changes
            weight = int(matrix[y][x]) if use_matrix else 1
            walkable = weight <= 0 if inverse else weight >= 1

            nodes[y].append(Node(x=x, y=y, walkable=walkable, weight=weight))
    return nodes


class Grid(object):
    def __init__(self, width=0, height=0, matrix=None, inverse=False):
        """
        a grid represents the map (as 2d-list of nodes).
        """
        self.width = width
        self.height = height
        if isinstance(matrix, (tuple, list)) or (
                USE_NUMPY and isinstance(matrix, np.ndarray) and
                matrix.size > 0):
            self.height = len(matrix)
            self.width = self.width = len(matrix[0]) if self.height > 0 else 0
        if self.width > 0 and self.height > 0:
            self.nodes = build_nodes(self.width, self.height, matrix, inverse)
        else:
            self.nodes = [[]]

    def node(self, x, y):
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y):
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y):
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        return self.inside(x, y) and self.nodes[y][x].walkable

    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        neighbors = []
        s0 = d0 = s1 = d1 = s2 = d2 = s3 = d3 = False

        # ↑
        if self.walkable(x, y - 1):
            neighbors.append(self.nodes[y - 1][x])
            s0 = True
        # →
        if self.walkable(x + 1, y):
            neighbors.append(self.nodes[y][x + 1])
            s1 = True
        # ↓
        if self.walkable(x, y + 1):
            neighbors.append(self.nodes[y + 1][x])
            s2 = True
        # ←
        if self.walkable(x - 1, y):
            neighbors.append(self.nodes[y][x - 1])
            s3 = True

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            d0 = s3 and s0
            d1 = s0 and s1
            d2 = s1 and s2
            d3 = s2 and s3
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            d0 = s3 or s0
            d1 = s0 or s1
            d2 = s1 or s2
            d3 = s2 or s3
        elif diagonal_movement == DiagonalMovement.always:
            d0 = d1 = d2 = d3 = True

        # ↖
        if d0 and self.walkable(x - 1, y - 1):
            neighbors.append(self.nodes[y - 1][x - 1])

        # ↗
        if d1 and self.walkable(x + 1, y - 1):
            neighbors.append(self.nodes[y - 1][x + 1])

        # ↘
        if d2 and self.walkable(x + 1, y + 1):
            neighbors.append(self.nodes[y + 1][x + 1])

        # ↙
        if d3 and self.walkable(x - 1, y + 1):
            neighbors.append(self.nodes[y + 1][x - 1])

        return neighbors

    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None, win=None,
                 border=True, start_chr=red+'&'+endc, end_chr=green+'$'+endc,
                 path_chr=yellow+'.'+endc, empty_chr=' ', block_chr='#',
                 win_chr=blue+'@'+endc, show_weight=False):
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        data = ''
        open_cell = []
        if border:
            data = '+{}+'.format('-'*len(self.nodes[0]))
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    open_cell.append((x,y))
                    line += end_chr
                elif node == win:
                    open_cell.append((x,y))
                    line += win_chr
                elif path and ((node.x, node.y) in path or node in path):
                    open_cell.append((x,y))
                    line += path_chr
                elif node.walkable:
                    open_cell.append((x, y))
                    # empty field
                    weight = str(node.weight) if node.weight < 10 else '+'
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = '|'+line+'|'
            if data:
                data += '\n'
            data += line
        if border:
            data += '\n+{}+'.format('-'*len(self.nodes[0]))
        return data, open_cell
