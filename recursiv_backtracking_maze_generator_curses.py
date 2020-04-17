import curses
import time

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


pos_change = [(0, -1), (0, 1), (1, 0), (-1, 0)]
pos_choice = range(0, len(pos_change))


def setup():
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)
    return stdscr


def get_next(maze: [[]], node: Node, height, width) -> Node:
    random.shuffle(pos_change)
    i = random.choice(pos_choice)

    attempt = 0
    while attempt != 4:
        attempt += 1
        x, y = pos_change[i]
        x = node.x + x
        y = node.y + y

        i -= 1

        if x < 0 or y < 0 or x >= height or y >= width:
            continue

        if maze[x][y] is None:
            new_node = Node(x, y)
            new_node.pred_node = node
            maze[x][y] = new_node
            return new_node


def main(height=20, width=50, seed=None, delay=0):
    stdscr = setup()
    MAX_X, MAX_Y = stdscr.getmaxyx()
    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)

    height //= 2
    width //= 2

    random.seed(seed)
    pre_maze = [[None for n in range(0, width)] for nn in range(0, height)]

    start_node = Node(0, 0)
    pre_maze[0][0] = start_node
    current_node = start_node

    maze = [['#' for n in range(0, width * 2 + 1)] for nn in range(0, height * 2 + 1)]

    for i_line in range(0, len(maze)):
        for i_char in range(0, len(maze[i_line])):
            main_window.addstr(i_line, i_char, ' ', curses.color_pair(1))

    calc_height = len(pre_maze)
    calc_width = len(pre_maze[0])

    main_window.refresh()
    main_window.getch()
    time.sleep(1)

    current_node = get_next(pre_maze, current_node, calc_height, calc_width)
    last_pos = (current_node.x, current_node.y)
    while current_node != start_node:
        next_node = get_next(pre_maze, current_node, calc_height, calc_width)

        main_window.addstr(current_node.x * 2 + 1, current_node.y * 2 + 1, ' ')
        if current_node.x > current_node.pred_node.x:
            main_window.addstr(current_node.x * 2, current_node.y * 2 + 1, ' ')
            maze[current_node.x * 2][current_node.y * 2 + 1] = ' '

        elif current_node.x < current_node.pred_node.x:
            main_window.addstr(current_node.x * 2 + 2, current_node.y * 2 + 1, ' ')
            maze[current_node.x * 2 + 2][current_node.y * 2 + 1] = ' '

        elif current_node.y < current_node.pred_node.y:
            main_window.addstr(current_node.x * 2 + 1, current_node.y * 2 + 2, ' ')
            maze[current_node.x * 2 + 1][current_node.y * 2 + 2] = ' '

        elif current_node.y > current_node.pred_node.y:
            main_window.addstr(current_node.x * 2 + 1, current_node.y * 2, ' ')
            maze[current_node.x * 2 + 1][current_node.y * 2] = ' '

        if next_node is None:
            current_node = current_node.pred_node
            main_window.addstr(current_node.x * 2 + 1, current_node.y * 2 + 1, ' ')
            maze[current_node.x * 2 + 1][current_node.y * 2 + 1] = ' '
        else:
            current_node = next_node

        main_window.addstr(last_pos[0] * 2 + 1, last_pos[1] * 2 + 1, ' ')
        last_pos = (current_node.x, current_node.y)
        main_window.addstr(last_pos[0] * 2 + 1, last_pos[1] * 2 + 1, ' ', curses.color_pair(2))

        main_window.refresh()
        time.sleep(delay)

    maze[1][1] = 'S'
    maze[-2][-2] = 'E'

    main_window.addstr(1, 1, ' ', curses.color_pair(2))
    main_window.addstr(len(maze)-2, len(maze[0])-2, ' ', curses.color_pair(2))

    main_window.refresh()
    main_window.getch()
    time.sleep(2)
    curses.endwin()

    return maze, (1, 1), (-2, -2)


if __name__ == '__main__':
    main()
