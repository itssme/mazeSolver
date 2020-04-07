import os
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
            raise NotImplementedError


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

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Node):
            return o.pos == self.pos
        else:
            raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.cost < other.cost
        else:
            raise NotImplementedError

    def get_next(self, maze):
        if self.up is None and maze[self.pos.x - 1][self.pos.y] != '#':
            self.up = Node(Pos(self.pos.x - 1, self.pos.y), pred=self, cost=self.cost + 1)
            return self.up

        if self.right is None and maze[self.pos.x][self.pos.y+1] != '#':
            self.right = Node(Pos(self.pos.x, self.pos.y + 1), pred=self, cost=self.cost + 1)
            return self.right

        if self.down is None and maze[self.pos.x + 1][self.pos.y] != '#':
            self.down = Node(Pos(self.pos.x + 1, self.pos.y), pred=self, cost=self.cost + 1)
            return self.down

        if self.left is None and maze[self.pos.x][self.pos.y - 1] != '#':
            self.left = Node(Pos(self.pos.x, self.pos.y - 1), pred=self, cost=self.cost + 1)
            return self.left

        return None


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
    next_node = Node(start_pos)
    sortedList = [next_node]

    def printList():
        str_list = "["
        for node in sortedList:
            str_list += str(node) + ","
        str_list = str_list[:-1] + "]"
        print(str_list)

    def printMaze():
        for line in maze:
            line_str = ""
            for char in line:
                line_str += char
            print(line_str)

    def insert_node(new_node: Node):
        i = 0
        while i < len(sortedList):
            if new_node < sortedList[i]:
                sortedList.insert(i, new_node)
                i = len(sortedList)
            i += 1

        if i == len(sortedList):
            sortedList.append(new_node)

    start = time.time()
    draw = 0
    while maze[next_node.pos.x][next_node.pos.y] != 'E':
        next_node = None

        i = 0
        while next_node is None:
            next_node = sortedList[i].get_next(maze)
            i += 1

        #printList()

        if next_node in sortedList:
            old_i = sortedList.index(next_node)
            if next_node.cost < sortedList[old_i].cost:
                sortedList.remove(next_node)
                insert_node(next_node)
        else:
            insert_node(next_node)

        if maze[next_node.pos.x][next_node.pos.y] != 'E':
            maze[next_node.pos.x][next_node.pos.y] = '.'
            draw += 1
            if draw % 100 == 0:
                os.system("clear")
                printMaze()

    print("solved maze in " + str(time.time() - start) + " seconds")

    while next_node.pos != start_pos:
        maze[next_node.pos.x][next_node.pos.y] = "O"
        next_node = next_node.pred

    printMaze()


if __name__ == '__main__':
    main()
