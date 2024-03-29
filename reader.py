import configparser
import igraph as ig

def read_data(TASK_CRASHED_ID, CRASHED_PART_OF_TASK, MF_PERIOD, FIXATOR_TIME, GRAPH_INITIAL_APP, MAP_PARTITION_TASK, MAP_WINDOW_PARTITION):
    config = configparser.ConfigParser()
    config.read('example.ini')

    TASK_CRASHED_ID = int(config["INIT_DATA"]["task_crashed_id"])
    CRASHED_PART_OF_TASK = int(config["INIT_DATA"]["crashed_part_of_task"])
    MF_PERIOD = int(config["INIT_DATA"]["mf_period"])
    FIXATOR_TIME = int(config["INIT_DATA"]["fixator_time"])

    edges=eval(config["GRAPH_VERTEX"]["messages"])

    GRAPH_INITIAL_APP = ig.Graph(n=int(config["GRAPH_VERTEX"]["quantity"]), edges=eval(config["GRAPH_VERTEX"]["messages"]))
    GRAPH_INITIAL_APP.vs["duration"] = list(map(lambda x: int(x), eval(config["GRAPH_VERTEX"]["duration"])))

    MAP_PARTITION_TASK = eval(config["MAP_PARTITION_TASK"]["dict"])
    MAP_WINDOW_PARTITION = eval(config["MAP_WINDOW_PARTITION"]["dict"])

    return TASK_CRASHED_ID, CRASHED_PART_OF_TASK, MF_PERIOD, FIXATOR_TIME, GRAPH_INITIAL_APP, MAP_PARTITION_TASK, MAP_WINDOW_PARTITION
    
