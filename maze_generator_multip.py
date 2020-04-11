from solver.fastImpl import solverIterativ
from solver.fastImpl import solverIterativAstar

from solver.fastImpl.solverIterativ import Colors

from multiprocessing import Process, Queue, Pipe, Pool

from main import parse_maze

import random
import signal
import math
import time
import os

symbols = [" ", "#"]


def get_fitness(maze, start_pos, end_pos):
    sum = 0
    try:
        #for i in range(0, 10):
        fitness, ln = solverIterativ.main(maze, start_pos, end_pos, False)
        #    sum += fitness
        sum = ln
    except KeyError:
        return -math.inf
    except IndexError:
        return -math.inf

    #return sum / 10
    return sum


def check_valid(maze, start_pos, end_pos):
    try:
        solverIterativ.main(maze, start_pos, end_pos, False)
    except KeyError:
        return False
    except IndexError:
        return False
    return True


def generator(start_maze, start_pos, end_pos, run: Queue, p: Pipe):
    maze = [x[:] for x in start_maze]
    mutations = 100
    fitness = get_fitness(maze, start_pos, end_pos)
    print("started working on: " + str(fitness))
    start_time = time.time()
    loops = 0
    while run.empty():
        for i in range(0, 10):
            new_maze = mutate([x[:] for x in maze], mutations, start_pos, end_pos)
            new_fitness = get_fitness(new_maze, start_pos, end_pos)

            if fitness < new_fitness:
                print("FOUND BETTER: " + str(new_fitness))
                p.send(new_maze)
                return None
            elif fitness == new_fitness:
                maze = new_maze

            mutations -= 1
            if mutations <= 1:
                mutations = 50

            loops += 1
            if loops == 100:
                print("Took " + str(time.time() - start_time) + " seconds for 100 runs")
                start_time = time.time()
                loops = 0


def mutate(new_maze, mutations, start_pos, end_pos):
    for i in range(0, mutations):
        x = random.randrange(1, 19)
        y = random.randrange(1, 19)
        z = random.randrange(0, 100)

        if z < 50:
            z = 0
        else:
            z = 1

        n = new_maze[x][y]
        new_maze[x][y] = symbols[z] if new_maze[x][y] != symbols[z] else symbols[z-1]
        if not check_valid(new_maze, start_pos, end_pos):
            new_maze[x][y] = n
    return new_maze


def printMaze(maze):
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


def main():
    maze, start_pos, end_pos = parse_maze("generated/saved_172.txt")
    fitness = get_fitness(maze, start_pos, end_pos)

    stop_queue = Queue()
    parent_conn, child_conn = Pipe()

    worker_pool = Pool(4, generator, (maze, start_pos, end_pos, stop_queue, child_conn))

    try:
        while True:
            new_maze = parent_conn.recv()
            print("got new maze")
            new_fitness = get_fitness(new_maze, start_pos, end_pos)
            if fitness < new_fitness:
                maze = new_maze
                stop_queue.put(True)
                worker_pool.close()
                worker_pool.join()
                stop_queue.get()
                fitness = new_fitness
                worker_pool = Pool(4, generator, (maze, start_pos, end_pos, stop_queue, child_conn))
                print("started new threads")
                solverIterativ.main([x[:] for x in maze], start_pos, end_pos, True)
                print("Fitness is: " + str(fitness))
    except KeyboardInterrupt:
        if stop_queue.empty():
            stop_queue.put(True)
            worker_pool.close()

        worker_pool.join()

        solverIterativ.main([x[:] for x in maze], start_pos, end_pos, True)
        print("Fitness is: " + str(fitness))

        write_maze = open("generated/saved_" + str(fitness) + ".txt", "w")
        for i in range(0, len(maze) - 1):
            write_maze.write("".join(maze[i]) + "\n")
        write_maze.write("".join(maze[-1]))
        write_maze.close()


if __name__ == '__main__':
    main()