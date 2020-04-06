class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    reader = open("maze.txt", "r")

    maze_read = reader.readlines()
    maze = []

    for line_i in range(0, len(maze_read)):
        maze_line = []
        for char_i in range(0, len(maze_read[line_i])):
            if maze_read[line_i][char_i] != '\n':
                maze_line.append(maze_read[line_i][char_i])

        maze.append(maze_line)

    del maze_read
    print(maze)


if __name__ == '__main__':
    main()
