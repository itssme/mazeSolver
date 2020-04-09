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
    def __init__(self, pos, left=None, up=None, right=None, down=None, pred=None):
        self.pos = pos
        self.left = left
        self.up = up
        self.right = right
        self.down = down
        self.pred = pred
        self.visited = False


def main():
    reader = open("maze/maze2.txt", "r")

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

    visited_pos = []
    start = time.time()

    def resolve(current_node):
        print("solved maze in " + str(time.time() - start) + " seconds")

        while current_node.pos != start_pos:
            maze[current_node.pos.x][current_node.pos.y] = "O"
            current_node = current_node.pred

        for line in maze:
            line_str = ""
            for char in line:
                line_str += char
            print(line_str)

    def rec(current_node):
        if maze[current_node.pos.x-1][current_node.pos.y] != "#":
            new_pos = Pos(current_node.pos.x-1, current_node.pos.y)

            if new_pos not in visited_pos:
                visited_pos.append(new_pos)

                current_node.up = Node(pos=new_pos, pred=current_node, down=current_node)
                #print("going up")
                rec(current_node.up)

        if maze[current_node.pos.x][current_node.pos.y+1] != "#":
            new_pos = Pos(current_node.pos.x, current_node.pos.y+1)

            if new_pos not in visited_pos:
                visited_pos.append(new_pos)

                current_node.right = Node(pos=new_pos, pred=current_node, left=current_node)

                if maze[current_node.pos.x][current_node.pos.y+1] == "E":
                    print("ENDDD :))")
                    resolve(current_node)
                    quit(0)

                #print("going right")
                rec(current_node.right)

        if maze[current_node.pos.x+1][current_node.pos.y] != "#":
            new_pos = Pos(current_node.pos.x+1, current_node.pos.y)

            if new_pos not in visited_pos:
                visited_pos.append(new_pos)

                current_node.down = Node(pos=new_pos, pred=current_node, up=current_node)

                #print("going down")
                rec(current_node.down)

        if maze[current_node.pos.x][current_node.pos.y-1] != "#":
            new_pos = Pos(current_node.pos.x, current_node.pos.y-1)

            if new_pos not in visited_pos:
                visited_pos.append(new_pos)

                current_node.left = Node(pos=new_pos, pred=current_node, right=current_node)

                #print("going left")
                rec(current_node.left)

    current_node = Node(start_pos)
    rec(current_node)


if __name__ == '__main__':
    main()
