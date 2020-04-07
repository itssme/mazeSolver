import time


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Pos(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Pos):
            return o.x == self.x and o.y == self.y
        else:
            return super(Pos, self).__eq__()


class Node:
    def __init__(self, pos, left=None, up=None, right=None, down=None, pred=None, cost=0):
        self.pos = pos
        self.left = left
        self.up = up
        self.right = right
        self.down = down
        self.pred = pred
        self.visited = False
        self.cost = cost

    def __str__(self):
        return "Node(" + str(self.pos) + ", cost=" + str(self.cost) + ")"

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.cost < other.cost
        else:
            raise NotImplementedError


def main():
    reader = open("maze2.txt", "r")

    maze_read = reader.readlines()
    maze = []
    start_pos = None

    for line_i in range(0, len(maze_read)):
        maze_line = []
        for char_i in range(0, len(maze_read[line_i])):
            char = maze_read[line_i][char_i]

            if char == 'S':
                start_pos = Pos(line_i, char_i)

            if char != '\n':
                maze_line.append(char)

        maze.append(maze_line)

    del maze_read

    if start_pos is None:
        raise Exception("Could not find start position")

    print("Starting at: " + str(start_pos))
    current_node = Node(start_pos)

    sortedList = []

    while maze[current_node.pos.x][current_node.pos.y] != "E":
        pass


if __name__ == '__main__':
    main()
