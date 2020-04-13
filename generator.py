import argparse

from recursiv_backtracking_maze_generator import main as recursive_back


def main(write: str, raw: bool):
    maze, start_pos, end_pos = recursive_back()

    if raw:
        maze_str = ""
        for line in maze:
            maze_str += "".join(line) + "\n"

        print(maze_str)

    if write != "":
        writer = open(write, "w")

        for line in maze:
            writer.write("".join(line) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate mazes")
    #parser.add_argument("--algo", default="recursive_back", type=str)
    parser.add_argument("--write", default="", type=str)
    parser.add_argument("--raw", action="store_true")

    args = parser.parse_args()

    main(args.write, args.raw)
