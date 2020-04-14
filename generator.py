import argparse

from recursiv_backtracking_maze_generator import main as recursive_back
from recursiv_backtracking_maze_generator_curses import main as recursive_back_curses


def main(write: str, raw: bool, curses: bool):
    maze, start_pos, end_pos = recursive_back()

    maze_str = ""

    if raw:
        for line in maze:
            maze_str += "".join(line) + "\n"

        maze_str = maze_str[:-1]
        print(maze_str)

    if write != "":
        writer = open(write, "w")

        if maze_str == "":
            for line in maze:
                writer.write("".join(line) + "\n")
        else:
            writer.write(maze_str)

    if curses:
        recursive_back_curses()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate mazes")
    #parser.add_argument("--algo", default="recursive_back", type=str)
    parser.add_argument("--write", default="", type=str)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--curses", action="store_true")

    args = parser.parse_args()

    main(args.write, args.raw, args.curses)
