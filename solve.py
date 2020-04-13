"""
call this program like:
> cat maze.txt | python3 solve.py
> python3 generator.py --raw | python3 solver.py
"""

from main import parse_maze
from solver.fastImpl.solverIterativ import main as dijkstra

import sys


def main():
    data = sys.stdin.read().split("\n")

    if not data[-1]:
        data = data[:-1]

    maze, start_pos, end_pos = parse_maze(data)

    dijkstra(maze, start_pos, end_pos, True)


if __name__ == '__main__':
    main()
