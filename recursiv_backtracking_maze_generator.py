from solver.fastImpl.solverIterativ import Colors  # TODO: replace with color object in root

from solver.curses.solverIterativAstar_curses import main as cursesAstar
from solver.curses.solverIterativ_curses import main as cursesDijkstra

from solver.fastImpl.solverIterativ import main as dijkstra

import random


class Node:
    def __init__(self, x, y, pred_node=None):
        self.x = x
        self.y = y
        self.pred_node = pred_node

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y


def printMaze(maze):
    for line in maze:
        line_str = ""
        for char in line:
            if char == '#':
                line_str += Colors.REDBG + ' ' + Colors.ENDC
            elif char == 'S':
                line_str += Colors.WHITEBG + ' ' + Colors.ENDC
            elif char == 'E':
                line_str += Colors.WHITEBG + ' ' + Colors.ENDC
            else:
                line_str += char
        print(line_str)


def get_next(maze: [[]], node: Node) -> Node:
    pos_change = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    pos_choice = range(0, len(pos_change))

    random.shuffle(pos_change)
    i = random.choice(pos_choice)

    attempt = 0
    while attempt != 4:
        attempt += 1
        x, y = pos_change[i]
        x = node.x + x
        y = node.y + y

        i -= 1

        if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[x]):
            continue

        if maze[x][y] is None:
            new_node = Node(x, y)
            new_node.pred_node = node
            maze[x][y] = new_node
            return new_node


def main():
    width = 190
    height = 5000
    pre_maze = [[None for n in range(0, width)] for nn in range(0, height)]

    start_node = Node(0, 0)
    pre_maze[0][0] = start_node
    current_node = start_node

    maze = [['#' for n in range(0, width * 2 + 1)] for nn in range(0, height * 2 + 1)]

    current_node = get_next(pre_maze, current_node)
    while current_node != start_node:
        next_node = get_next(pre_maze, current_node)

        if next_node is None:
            maze[current_node.x * 2 + 1][current_node.y * 2 + 1] = ' '
            if current_node.x > current_node.pred_node.x:
                maze[current_node.x * 2][current_node.y * 2 + 1] = ' '
            elif current_node.x < current_node.pred_node.x:
                maze[current_node.x * 2 + 2][current_node.y * 2 + 1] = ' '
            elif current_node.y < current_node.pred_node.y:
                maze[current_node.x * 2 + 1][current_node.y * 2 + 2] = ' '
            elif current_node.y > current_node.pred_node.y:
                maze[current_node.x * 2 + 1][current_node.y * 2] = ' '

            current_node = current_node.pred_node
            maze[current_node.x * 2 + 1][current_node.y * 2 + 1] = ' '
        else:
            current_node = next_node

    maze[1][1] = 'S'
    maze[-2][-2] = 'E'
    #printMaze(maze)

    #cursesDijkstra(maze, (1, 1), (-2, -2), 0, 0)
    print(dijkstra(maze, (1, 1), (-2, -2), True))


if __name__ == '__main__':
    main()
