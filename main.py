from solver.curses import solverIterativ_curses
from solver.curses import solverIterativAstar_curses

from solver.fastImpl import solverIterativ
from solver.fastImpl import solverIterativAstar

import argparse


def parse_maze(file):
    reader = open(file, "r")

    maze_read = reader.readlines()
    maze = []
    start_pos = None
    end_pos = None

    for line_i in range(0, len(maze_read)):
        maze_line = []
        for char_i in range(0, len(maze_read[line_i])):
            char = maze_read[line_i][char_i]

            if char == 'S':
                start_pos = (line_i, char_i)

            if char != '\n':
                maze_line.append(char)

            if char == 'E':
                end_pos = (line_i, char_i)
                maze_line.append(' ')

        maze.append(maze_line)

    if start_pos is None:
        raise Exception("Could not find start position")

    if end_pos is None:
        raise Exception("Could not find end position")

    return maze, start_pos, end_pos


def main(file: str, algo: str, use_curses: bool, loop_delay: float):
    maze, start_pos, end_pos = parse_maze(file)

    if algo == "astar":
        if use_curses:
            solverIterativAstar_curses.main(maze, start_pos, end_pos, loop_delay)
        else:
            solverIterativAstar.main(maze, start_pos, end_pos, print_maze=True)
    elif algo == "dijkstra":
        if use_curses:
            solverIterativ_curses.main(maze, start_pos, end_pos, loop_delay)
        else:
            solverIterativ.main(maze, start_pos, end_pos, print_maze=True)
    else:
        raise Exception("No algorithm implementation named '" + str(algo) + "'")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Solve mazes")
    parser.add_argument("--algo", default="astar", type=str)
    parser.add_argument("--maze", default="maze0.txt", type=str)
    parser.add_argument("--curses", action="store_true")
    parser.add_argument("--delay", default=0, type=float)
    args = parser.parse_args()

    main(args.maze, args.algo.lower(), args.curses, args.delay)
