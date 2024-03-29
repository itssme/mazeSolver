from solver.fastImpl import solverIterativ
from solver.fastImpl import solverIterativAstar

from solver.fastImpl.solverIterativ import Colors

from multiprocessing import Queue, Pipe, Pool

from main import parse_maze

import random
import math
import time
import os

symbols = [" ", "#"]


def get_fitness(maze, start_pos, end_pos):
    try:
        fitness, ln = solverIterativAstar.main(maze, start_pos, end_pos, False)
        return ln
    except KeyError:
        return -math.inf
    except IndexError:
        return -math.inf


def generator(start_maze, start_pos, end_pos, run: Queue, result: Queue):
    if not run.empty():
        print("why am I running >:(")
        time.sleep(1)
        return None
    maze = [x[:] for x in start_maze]
    max_mutations = 1
    max_loops = 2500
    mutations = max_mutations
    fitness = get_fitness(maze, start_pos, end_pos)
    print("started working on: " + str(fitness))
    start_time = time.time()
    loops = 0
    while run.empty():
        for i in range(0, 10):
            new_maze, new_fitness = mutate([x[:] for x in maze], mutations, start_pos, end_pos, fitness)

            if fitness < new_fitness:
                if run.empty():
                    print("FOUND BETTER: " + str(new_fitness))
                    result.put(new_maze)
                return None
            elif fitness == new_fitness:
                maze = new_maze

            mutations -= 1
            if mutations <= 1:
                mutations = max_mutations

            loops += 1
            if loops == max_loops:
                print("Took " + str(time.time() - start_time) + " seconds for " + str(max_loops) + ", max mutations=" + str(max_mutations))
                start_time = time.time()
                loops = 0
                if max_mutations < 15:
                    max_loops -= 100
                    max_mutations += 1
                else:
                    max_loops = 5000
                    max_mutations = 1

base_v = 5


def mutate(new_maze, mutations, start_pos, end_pos, best_fit):
    base_x = random.randrange(1 + base_v, 51 - base_v)
    base_y = random.randrange(1 + base_v, 200 - base_v)
    fitness = -math.inf

    for i in range(0, mutations*10):
        #x = random.randrange(1, 49)
        #y = random.randrange(1, 49)
        z = random.randrange(0, 100)

        x = random.randrange(base_x - base_v, base_x + base_v)
        y = random.randrange(base_y - base_v, base_y + base_v)

        if z < 50:
            z = 0
        else:
            z = 1

        #new_maze[x][y] = symbols[z] if new_maze[x][y] != symbols[z] else symbols[z-1]
        n = new_maze[x][y]
        if n != symbols[z]:
            new_maze[x][y] = symbols[z]
            if mutations > 5:
                fitness = get_fitness(new_maze, start_pos, end_pos)
                if fitness == -math.inf:
                    new_maze[x][y] = n
                elif best_fit < fitness:
                    return new_maze, fitness

    if fitness == -math.inf:
        fitness = get_fitness(new_maze, start_pos, end_pos)

    #os.system("clear")
    #printMaze(new_maze)
    #print(fitness)
    #time.sleep(0.05)
    return new_maze, fitness


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
    #path = "generated/"
    #path = "generated/Astar_20x20/"
    #save_as = "generated/savedAstar_"
    #save_as = "generated/Astar_20x20/savedAstarBIG_"
    path = "generated/Astar_test/"
    save_as = "generated/Astar_test/"


    filename = os.listdir(path)
    filename = [int(elem.split(".")[0]) for elem in filename if not "init" in elem]
    filename.sort()
    filename = str(filename[-1]) + ".txt" if filename else os.listdir(path)[0]

    #filename = os.listdir(path)[-1]
    maze, start_pos, end_pos = parse_maze(open(path + filename).read().split("\n"))
    fitness = get_fitness(maze, start_pos, end_pos)

    stop_queue = Queue()
    #parent_conn, child_conn = Pipe()
    result = Queue(0)

    worker_pool = Pool(4, generator, (maze, start_pos, end_pos, stop_queue, result))

    last_save = fitness

    try:
        while True:
            print("waiting for next maze")
            new_maze = result.get()
            print("got new maze")
            new_fitness = get_fitness([x[:] for x in new_maze], start_pos, end_pos)
            print("solved new maze with fitness " + str(new_fitness) + " current fitness is " + str(fitness))
            if fitness < new_fitness:
                print("using new maze")
                maze = new_maze
                stop_queue.put(True)
                worker_pool.close()
                print("waiting for join")
                worker_pool.join()
                print("getting stop")
                stop_queue.get()
                fitness = new_fitness
                worker_pool = Pool(4, generator, (maze, start_pos, end_pos, stop_queue, result))
                print("started new threads")
                time, _ = solverIterativAstar.main([x[:] for x in maze], start_pos, end_pos, True)
                print("Fitness is: " + str(fitness))
                print("Took: " + str(time))
                if fitness > last_save + 0:
                    print("SAVED MAZE")
                    write_maze = open(save_as + str(fitness) + ".txt", "w")
                    for i in range(0, len(maze) - 1):
                        write_maze.write("".join(maze[i]) + "\n")
                    write_maze.write("".join(maze[-1]))
                    write_maze.close()
                    last_save = fitness
    except KeyboardInterrupt:
        if stop_queue.empty():
            stop_queue.put(True)
            worker_pool.close()

        worker_pool.join()

        solverIterativAstar.main([x[:] for x in maze], start_pos, end_pos, True)
        print("Fitness is: " + str(fitness))

        write_maze = open(save_as + str(fitness) + ".txt", "w")
        for i in range(0, len(maze) - 1):
            write_maze.write("".join(maze[i]) + "\n")
        write_maze.write("".join(maze[-1]))
        write_maze.close()


if __name__ == '__main__':
    main()
