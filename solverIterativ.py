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


class Node:
    def __init__(self, x, y, maze, pred=None, cost=0):
        self.x = x
        self.y = y
        self.pred = pred
        self.cost = cost
        self.costN = cost + 1

        self.conns = []

        if maze[self.x - 1][self.y] != '#':
            self.conns.append((self.x - 1, self.y))
        if maze[self.x][self.y+1] != '#':
            self.conns.append((self.x, self.y + 1))
        if maze[self.x + 1][self.y] != '#':
            self.conns.append((self.x + 1, self.y))
        if maze[self.x][self.y - 1] != '#':
            self.conns.append((self.x, self.y - 1))

        self.len = len(self.conns)

    def __str__(self):
        #return "Node(" + str(self) + ", cost=" + str(self.cost) + ")"
        return str(self.cost)

    def __eq__(self, o):
        return o.x == self.x and o.y == self.y

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def get_next(self, maze):
        if self.len:
            self.len -= 1
            x, y = self.conns.pop()
            return Node(x, y, maze, pred=self, cost=self.costN)


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
                start_pos = (line_i, char_i)

            if char != '\n':
                maze_line.append(char)

            if char == 'E':
                maze_line.append(' ')

        maze.append(maze_line)

    del maze_read

    if start_pos is None:
        raise Exception("Could not find start position")

    next_node = Node(start_pos[0], start_pos[1], maze)
    start_pos = next_node
    sortedList = [next_node, Node(-1, -1, maze, cost=math.inf)]

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
            if new_node.cost < sortedList[i].cost:
                if sortedList[i-1].cost <= new_node.cost:
                    break
                else:
                    i = i // 2
            else:
                if new_node.cost <= sortedList[i+1].cost:
                    i += 1
                    break
                else:
                    i += (leng - i) // 2

        sortedList.insert(i, new_node)

    os.system("clear")
    printMaze()

    start = time.time()
    draw = 0
    unique_dic = {}
    while maze[next_node.x][next_node.y] != 'E':
        next_node = None

        i = 0
        while next_node is None:
            next_node = sortedList[i].get_next(maze)
            i += 1

        #printList()

        old_n = unique_dic.get((next_node.x, next_node.y))
        if old_n:
            if next_node.cost < old_n.cost:
                sortedList.remove(next_node)
                insert_node(next_node)
                unique_dic[(next_node.x, next_node.y)] = next_node
        else:
            insert_node(next_node)
            unique_dic[(next_node.x, next_node.y)] = next_node

        """
        if maze[next_node.x][next_node.y] != 'E' and maze[next_node.x][next_node.y] != 'S':
            maze[next_node.x][next_node.y] = Colors.BLUEBG + ' ' + Colors.ENDC
            draw += 1
            if draw % 300 == 0:
                os.system("clear")
                printMaze()
        """

    end_time = time.time()

    #draw = 0
    while next_node != start_pos:
        maze[next_node.x][next_node.y] = Colors.GREENBG2 + ' ' + Colors.ENDC
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
