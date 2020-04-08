import os
import time
import math
import curses

"""
                       _     _           _                      _             
  __ _ _ __ __ _ _ __ | |__ (_) ___ __ _| | __   _____ _ __ ___(_) ___  _ __  
 / _` | '__/ _` | '_ \| '_ \| |/ __/ _` | | \ \ / / _ \ '__/ __| |/ _ \| '_ \ 
| (_| | | | (_| | |_) | | | | | (_| (_| | |  \ V /  __/ |  \__ \ | (_) | | | |
 \__, |_|  \__,_| .__/|_| |_|_|\___\__,_|_|   \_/ \___|_|  |___/_|\___/|_| |_|
 |___/          |_|                                                           

"""


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


WALL = Colors.REDBG + ' ' + Colors.ENDC
START = Colors.WHITEBG + ' ' + Colors.ENDC
END = Colors.WHITEBG + ' ' + Colors.ENDC


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


def setup():
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)
    return stdscr


def main():
    reader = open("maze4.txt", "r")

    maze_read = reader.readlines()
    maze = []
    start_pos = None

    stdscr = setup()
    MAX_X, MAX_Y = stdscr.getmaxyx()
    main_window = curses.newwin(MAX_X, MAX_Y, 0, 0)

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

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)

    for i_line in range(0, len(maze)):
        for i_char in range(0, len(maze[i_line])):
            if maze[i_line][i_char] == '#':
                main_window.addstr(i_line, i_char, ' ', curses.color_pair(1))
            elif maze[i_line][i_char] == 'S':
                main_window.addstr(i_line, i_char, ' ', curses.color_pair(2))
            elif maze[i_line][i_char] == 'E':
                main_window.addstr(i_line, i_char, ' ', curses.color_pair(2))

    main_window.refresh()

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
                    line_str += WALL
                elif char == 'S':
                    line_str += START
                elif char == 'E':
                    line_str += END
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

    #os.system("clear")
    #printMaze()

    start = time.time()
    unique_dic = {}
    while maze[next_node.x][next_node.y] != 'E':
        next_node = None

        i = 1
        while i < len(sortedList) - 1:
            if not sortedList[i].len:
                main_window.addstr(sortedList[i].x, sortedList[i].y, ' ', curses.color_pair(4))
                del sortedList[i]
            else:
                i += 1

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

        #"""
        if maze[next_node.x][next_node.y] != 'E' and maze[next_node.x][next_node.y] != 'S':
            if next_node.len and not old_n:
                main_window.addstr(next_node.x, next_node.y, ' ', curses.color_pair(3))
            main_window.refresh()
        #"""

    end_time = time.time()

    while next_node != start_pos:
        next_node = next_node.pred
        main_window.addstr(next_node.x, next_node.y, ' ', curses.color_pair(5))
        main_window.refresh()
        time.sleep(0.005)

    time.sleep(2)

    curses.endwin()

    print("solved maze in " + str(end_time - start) + " seconds")


if __name__ == '__main__':
    main()
