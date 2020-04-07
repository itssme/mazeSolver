import os
import time
import math


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Pos(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, o: object) -> bool:
        return o.x == self.x and o.y == self.y


class Node:
    def __init__(self, pos, pred=None, cost=0):
        self.pos = pos
        self.left = False
        self.up = False
        self.right = False
        self.down = False
        self.pred = pred
        self.cost = cost

    def __str__(self):
        #return "Node(" + str(self.pos) + ", cost=" + str(self.cost) + ")"
        return str(self.cost)

    def __eq__(self, o: object) -> bool:
        return o.pos == self.pos

    def __lt__(self, other: object) -> bool:
        return self.cost < other.cost

    def __le__(self, other: object) -> bool:
        return self.cost <= other.cost

    def get_next(self, maze):
        if not self.up and maze[self.pos.x - 1][self.pos.y] != '#':
            self.up = True
            return Node(Pos(self.pos.x - 1, self.pos.y), pred=self, cost=self.cost + 1)

        elif not self.right and maze[self.pos.x][self.pos.y+1] != '#':
            self.right = True
            return Node(Pos(self.pos.x, self.pos.y + 1), pred=self, cost=self.cost + 1)

        elif not self.down and maze[self.pos.x + 1][self.pos.y] != '#':
            self.down = True
            return Node(Pos(self.pos.x + 1, self.pos.y), pred=self, cost=self.cost + 1)

        elif not self.left and maze[self.pos.x][self.pos.y - 1] != '#':
            self.left = True
            return Node(Pos(self.pos.x, self.pos.y - 1), pred=self, cost=self.cost + 1)


def main():
    reader = open("maze3.txt", "r")

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

    next_node = Node(start_pos)
    sortedList = [next_node, Node(Pos(-1, -1), cost=math.inf)]

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
                if char == '#':
                    line_str += Colors.REDBG + ' ' + Colors.ENDC
                elif char == 'S':
                    line_str += Colors.WHITEBG + ' ' + Colors.ENDC
                elif char == 'E':
                    line_str += Colors.WHITEBG + ' ' + Colors.ENDC
                else:
                    line_str += char
            print(line_str)

    def insert_node(new_node: Node):
        i = len(sortedList)//2
        leng = len(sortedList)
        for n in range(0, i):
            if new_node < sortedList[i]:
                if sortedList[i-1] <= new_node:
                    break
                else:
                    i = i // 2
            else:
                if new_node <= sortedList[i+1]:
                    i += 1
                    break
                else:
                    i += (leng - i) // 2

        sortedList.insert(i, new_node)

    os.system("clear")
    printMaze()

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

        """
        if maze[next_node.pos.x][next_node.pos.y] != 'E' and maze[next_node.pos.x][next_node.pos.y] != 'S':
            maze[next_node.pos.x][next_node.pos.y] = Colors.BLUEBG + ' ' + Colors.ENDC
            draw += 1
            if draw % 100 == 0:
                os.system("clear")
                printMaze()
        """

    end_time = time.time()

    #draw = 0
    while next_node.pos != start_pos:
        maze[next_node.pos.x][next_node.pos.y] = Colors.GREENBG2 + ' ' + Colors.ENDC
        next_node = next_node.pred
        #draw += 1
        #if draw % 4 == 0:
        #    os.system("clear")
        #    printMaze()
        #time.sleep(0.05)

    os.system("clear")
    printMaze()
    print("solved maze in " + str(end_time - start) + " seconds")


if __name__ == '__main__':
    main()
