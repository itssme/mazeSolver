"""
call this program like:
> cat maze.txt | python3 solve.py
> python3 generator.py --raw | python3 solver.py
"""


from main import parse_maze

from solver.curses import solverIterativ_curses
from solver.curses import solverIterativAstar_curses

from solver.fastImpl import solverIterativ
from solver.fastImpl import solverIterativAstar

import sys
import argparse

# example:
# python3 generator.py --height 25 --width 100 --raw | python3 solve.py --curses --delay 0.005 --delay_final 0.005


def main(algo, use_curses, loop_delay, loop_delay_final):
    data = sys.stdin.read().split("\n")

    if not data[-1]:
        data = data[:-1]

    maze, start_pos, end_pos = parse_maze(data)

    if algo == "astar":
        if use_curses:
            solverIterativAstar_curses.main(maze, start_pos, end_pos, loop_delay, loop_delay_final)
        else:
            solverIterativAstar.main(maze, start_pos, end_pos, print_maze=True)
    elif algo == "dijkstra":
        if use_curses:
            solverIterativ_curses.main(maze, start_pos, end_pos, loop_delay, loop_delay_final)
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
    parser.add_argument("--delay_final", default=0, type=float)
    args = parser.parse_args()

    main(args.algo.lower(), args.curses, args.delay, args.delay_final)
