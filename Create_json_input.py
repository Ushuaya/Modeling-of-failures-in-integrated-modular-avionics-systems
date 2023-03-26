import json 
import configparser
import igraph as ig
import random

TASK_CRASHED_ID = 0
# use it only in a case when task is separated on two part in different partitions (0 or 1 means left or right)
CRASHED_PART_OF_TASK = 0 
MF_PERIOD = 100
FIXATOR_TIME = 1
n = 22
edges = [[11, 9], [2, 0]]
duration = [random.randint(1,7) for _ in range(22)]

GRAPH_INITIAL_APP = ig.Graph(n=22, edges=[[11, 9], [2, 0]])
GRAPH_INITIAL_APP.vs["duration"] = [8, 8, 8] + [random.randint(1,7) for _ in range(len(GRAPH_INITIAL_APP.vs) - 3)]

# Partition numbers sequence must start from 0 
MAP_PARTITION_TASK = {0: (0, 1, 2), 1: (3, 4, 5), 2: (6, 7, 8, 9, 10, 11), }
MAP_WINDOW_PARTITION = {(0, 20): 0, (20, 40): 1, (40, 80): 2, (80, 100): 0}

parser = configparser.ConfigParser()

parser["INIT_DATA"] = {"TASK_CRASHED_ID": TASK_CRASHED_ID, "CRASHED_PART_OF_TASK": CRASHED_PART_OF_TASK, "MF_PERIOD": MF_PERIOD, "FIXATOR_TIME": FIXATOR_TIME}
# parser["TASK_CRASHED_ID"] = TASK_CRASHED_ID
# parser["CRASHED_PART_OF_TASK"] = CRASHED_PART_OF_TASK
# parser["MF_PERIOD"] = MF_PERIOD
# parser["FIXATOR_TIME"] = FIXATOR_TIME
parser["GRAPH_VERTEX"] = {"QUANTITY": n, "MESSAGES": edges, "DURATION": duration,}

parser["MAP_PARTITION_TASK"] = {"DICT": MAP_PARTITION_TASK}
parser["MAP_WINDOW_PARTITION"] = {"DICT": MAP_WINDOW_PARTITION}

with open('example.ini', 'w') as configfile:
    parser.write(configfile)




