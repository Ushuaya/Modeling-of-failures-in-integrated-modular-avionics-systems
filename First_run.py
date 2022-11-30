import igraph as ig
import os
import re
import parser_
import vision
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pickle

# DEFINING SOME VARAIBLES TO MAKE MODELLING SYSTEM ABLE TO RUN 
# ----------------------------------------------------------------------
TASK_CRASHED_ID = 0
MF_PERIOD = 120
FIXATOR_TIME = 1

GRAPH_INITIAL_APP = ig.Graph(n=12, edges=[[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [1, 3], [1, 4], [9, 10], [10, 11]])
GRAPH_INITIAL_APP.vs["duration"] = [5 for _ in range(len(GRAPH_INITIAL_APP.vs))]

# Partition numbers sequence must start from 0 
MAP_PARTITION_TASK = {0: (0, 1, 2), 1: (3, 4, 5), 2: (6, 7, 8), 3: (9, 10, 11)}
MAP_PARTITION_WINDOW = {0: (0, 20), 1: (20, 40), 2: (40, 60), 3: (60, 80)}
# hense we can create:
# ---
MAP_WINDOW_PARTITION = dict((v,k) for k,v in MAP_PARTITION_WINDOW.items())
MAP_WINDOWSTARTTIME_PARTITION = dict((v[0] ,k) for k,v in MAP_PARTITION_WINDOW.items())
# ---

WINDOWS = [MAP_PARTITION_WINDOW[i] for i in MAP_PARTITION_WINDOW]
PICTURE_FILENAME_INITIAL_APP = "initial_app"
PICTURE_FILENAME_NVP = "nvp_fault"
# ----------------------------------------------------------------------



class Window_elem():
    application = None
    time = None
    def __init__(self, application, time):
        self.application = application
        self.time = time

    def new_elem(self, application, time):
        self.application = application
        self.time = time

    def __str__(self) -> str:
        return "Window:\n" + "\tapp: " + str(self.application) + "\n" + "\tTime: " + str(self.time)

def create_double_visualization(filename1, filename2, task_crasshed_id): 
    img = Image.new('RGB', (256*10, 256*4))
    img1 = Image.open(filename1 + ".png")
    img2 = Image.open(filename2 + ".png")
    img.paste(img1, (0,0))
    img.paste(img2, (0,256*2))
    print("dir: ", dir(img))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font="./open-sans/OpenSans-ExtraBold.ttf", size=40)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((10, 10),"Crashed task: " + str(task_crasshed_id),(0,0,0), font=font )
    with open("num_test.pkl", "rb") as file:
        next_test = pickle.load(file)
        try: 
            os.mkdir("./tests/test{}".format(next_test))
        except:
            pass
        img.show()
        img.save("./tests/test{}/RESULT.png".format(next_test))
        next_test += 1
    with open("num_test.pkl", "wb") as file:
        pickle.dump(next_test, file)
    
def Write_xml_first_iter(filename, MF_PERIOD, GRAPH_INITIAL_APP, windows, MAP_TASK_PARTITION, PARTITION_WINDOW):
    with open(filename, "w") as file: 
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<system>\n")
        file.write("\t<module major_frame=\"{}\" name=\"core1\">\n".format(MF_PERIOD))

        for i in MAP_TASK_PARTITION: 
            file.write("\t\t<partition id=\"{}\" name=\"part{}\" scheduler=\"FPPS\">\n".format(i,i,))
            for j in MAP_TASK_PARTITION[i]:
                file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, j, j, MF_PERIOD, GRAPH_INITIAL_APP.vs[i]["duration"]))
            file.write("\t\t</partition>\n")

        # file.write("\t\t<partition id=\"0\" name=\"part1\" scheduler=\"FPPS\">\n")
        # for i in range(len(GRAPH_INITIAL_APP.vs)):
        #     file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, i, i, MF_PERIOD, GRAPH_INITIAL_APP.vs[i]["duration"]))
        # file.write("\t\t</partition>\n")


        for i in PARTITION_WINDOW:
            file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(i, PARTITION_WINDOW[i][0], PARTITION_WINDOW[i][1]))


        # for i in windows:
        #     file.write("\t\t<window partition=\"0\" start=\"{}\" stop=\"{}\"/>\n".format(i[0], i[1]))

        file.write("\t</module>\n")
        # for e in GRAPH_INITIAL_APP.es:
        #     file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[1], e.tuple[0]))
        file.write("</system>\n")


def Find_carsh_window_crash_set(filename, TASK_CRASHED_ID, windows, ):
    with open(filename) as file:
        txt = file.read().split("\n")
        #print(txt)
        crashed_task_pos = -1
        time_task_crash_start = -1
        time_task_crash_finish = -1
        for txt_line_num in range(len(txt)):
            if (crashed_task_pos := txt[txt_line_num].find("task id=\"{}\"".format(TASK_CRASHED_ID))) != -1: 
                time_task_crash_start = txt[txt_line_num + 2].find("time")
                time_task_crash_finish = txt[txt_line_num + 3].find("time")
                if (time_task_crash_start != -1):
                    time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                    time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])

                break 

        
        if crashed_task_pos != -1 and time_task_crash_start != -1 and time_task_crash_finish != -1:
            #print(crashed_task_pos, time_task_crash_start_num, time_task_crash_finish_num, i[0], i[1])
            window_crashed = [i for i in [i if (time_task_crash_start_num >= i[0] and time_task_crash_finish_num >= i[0] and time_task_crash_start_num <= i[1] and time_task_crash_finish_num <= i[1]) else None for i in windows] if i is not None][0]
            window_crashed = {"window_time": window_crashed, "window_number": windows.index(window_crashed)}
        else: 
            raise "didn't find broken task number {} in xml".format(TASK_CRASHED_ID)
        # in window_crashed there is time and number in sequense, of a window where erroe happend

        # Searching for a set of tasks in window where error happend
        window_crash_task_set = []
        for txt_line_num in range(len(txt)):
            if (crashed_task_pos := txt[txt_line_num].find("task id=")) != -1: 
                time_task_crash_start = txt[txt_line_num + 2].find("time")
                time_task_crash_finish = txt[txt_line_num + 3].find("time")
                if (time_task_crash_start != -1):
                    time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                if (time_task_crash_finish != -1):
                    time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])
                if (time_task_crash_start_num >= window_crashed["window_time"][0] and time_task_crash_finish_num >= window_crashed["window_time"][0] and time_task_crash_start_num <= window_crashed["window_time"][1] and time_task_crash_finish_num <= window_crashed["window_time"][1]):
                    window_crash_task_set += [int(re.findall(r'\d+', txt[txt_line_num])[0])]
    
    return window_crashed, window_crash_task_set 


def write_nvp_xml(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP):
    with open("test_nvp.xml", "w") as file: 
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<system>\n")
        file.write("\t<module major_frame=\"{}\" name=\"core1\">\n\n".format(MF_PERIOD))

        graph_reserve_window = graph_main_crash.copy() 
        graph_fixator = ig.Graph(n=len(windows_nvp)//3)
        graph_fixator.vs["duration"] = [FIXATOR_TIME for _ in range(len(windows_nvp)//3)]
        graph_fixator.vs["name"] = [str(i) for i in graph_fixator.vs.indices]


        # So now we have 4 graphs for:
        # 1) Graph for main applicaton (excludes window with crash)
        # 2) Graph for window with crash
        # 3) Graph for reserve window where error occured 
        # 4) Graph for fixator window

        # _res indicates, that message must be sent to or from the other version of the task
        # _fix indicates, that that it is one of fixator task 
        second_main_app_graph["non_task_from_initial_app"] = ""
        graph_main_crash["non_task_from_initial_app"] = ""
        graph_reserve_window["non_task_from_initial_app"] = "_res"
        graph_fixator["non_task_from_initial_app"] = "_fix"

        All_graphs_nvp_dict = {"Main": second_main_app_graph, "Main_crash": graph_main_crash, "Reserve_crash": graph_reserve_window, "Fixator": graph_fixator}
        All_win_dict = {"Main": 0, "Main_crash": 1, "Reserve_crash": 2, "Fixator": 3,  "Reserve": 4}



        # Writing file 
        Task_id_cout = 0 # Varaible to create unique numeric ids of tasks
        tmp_count = 0
        for q_partition in All_graphs_nvp_dict:
            file.write("\t\t<partition id=\"{}\" name=\"part_{}\" scheduler=\"FPPS\">\n".format(All_win_dict[q_partition], q_partition ))
            for i in range(len(All_graphs_nvp_dict[q_partition].vs)):
                # if q_partition != "Fixator":
                #     file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_period - 1, str(All_graphs_nvp_dict[q_partition].vs[i]["name"]), q_partition + str(i), MF_period, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                # else: 
                #     file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_period - 1, str(int(All_graphs_nvp_dict[q_partition].vs[i]["name"]) + len(g.vs.indices)), q_partition + str(i), MF_period, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                if q_partition != "Main" and q_partition != "Main_crash":
                    file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, Task_id_cout, q_partition + str(i), MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                else:
                    file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, str(int(All_graphs_nvp_dict[q_partition].vs[i]["name"])), q_partition + str(i), MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                Task_id_cout += 1
            tmp_count += 1
            file.write("\t\t</partition>\n\n")

        file.write("\t\t<partition id=\"4\" name=\"part_Reserve\" scheduler=\"FPPS\">\n")
        #file.write("\t\t\t<task deadline=\"299\" id=\"reserve\" name=\"reserve\" offset=\"0\" period=\"300\" prio=\"1\" wcet=\"100\"/>\n")
        file.write("\t\t</partition>\n\n")


        for i in range(len(windows_nvp)):
            #Window_elem("Main", [cur_time, win[1] - win[0] + cur_time])
            file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(All_win_dict[windows_nvp[i].application], windows_nvp[i].time[0], windows_nvp[i].time[1]))
        file.write("\t</module>\n")
        for e in GRAPH_INITIAL_APP.es:
            # _res indicates, that message must be sent to or from the other version of the task
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[1], e.tuple[0] ))
        file.write("</system>\n")


        # print("Id of crashed task: ", task_crasshed_id)
        # print("Window with crash", window_crashed)
        # print ("Set of tasks in window with crash: ", window_crash_task_set)

# CHECKING FOR VALID INPUT
# --------------------------------------------------------------------------------------------------------------
for i in WINDOWS: 
    if i[1] - i[0] <= 0:
        raise "window size <= 0"
    for j in GRAPH_INITIAL_APP.vs["duration"]:
        if j > (i[1] - i[0]):
            raise "to big task {}".format(j)
        if (i[1] - i[0])%j != 0:
            raise "Invalid task duration. Must be mupliple of window size, to aviod task preemt.".format(j)
# --------------------------------------------------------------------------------------------------------------

# CREATING XML FILE FOR FIRST ITERATION OF ALGORYTHM 
# --------------------------------------------------------------------------------------------------------------
Write_xml_first_iter("test.xml", MF_PERIOD, GRAPH_INITIAL_APP, WINDOWS, MAP_PARTITION_TASK, MAP_PARTITION_WINDOW)
# --------------------------------------------------------------------------------------------------------------


# RUNNING MODELLING SYSTEM ON FIRST ITERATION 
# --------------------------------------------------------------------------------------------------------------
os.system("cp test.xml  MCSSim/generator/model_builder") 
os.system("cd ./MCSSim/generator/model_builder; ./model_builder test.xml > result.txt; cd -")
os.system("cp ./MCSSim/generator/model_builder/result.txt  .") 
# --------------------------------------------------------------------------------------------------------------

# VISUALIZING FIRST ITERATION APPLICATION 
# --------------------------------------------------------------------------------------------------------------
parsing = parser_.INTERVAL()
"""Here specify input file."""
inter = parsing.create_int("result.txt")
parsing.print_intervals()

# 
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------



visioner1 = vision.VISUALISER()
"""Here you can specify name of output file."""
visioner1.visualise(inter, [i[0] for i in WINDOWS], PICTURE_FILENAME_INITIAL_APP, MF_PERIOD)
# --------------------------------------------------------------------------------------------------------------


# FINDING A SET OF TASKS IN WINDOW WITH ERROR OCCURED
# --------------------------------------------------------------------------------------------------------------
window_crashed, window_crash_task_set = Find_carsh_window_crash_set("./result.txt", TASK_CRASHED_ID, WINDOWS, )

# --------------------------------------------------------------------------------------------------------------



# creating window sequence
# --------------------------------------------------------------------------------------------------------------
windows_nvp = []
cur_time = 0
for win in WINDOWS: 
    if win[0] != window_crashed["window_time"][0]:
        windows_nvp += [Window_elem("Main" + "_part_" + str(MAP_WINDOWSTARTTIME_PARTITION[win[0]]), [cur_time, win[1] - win[0] + cur_time])]
        cur_time += win[1] - win[0]
        windows_nvp += [Window_elem("Fixator", [cur_time, cur_time + FIXATOR_TIME])]
        cur_time += FIXATOR_TIME
        windows_nvp += [Window_elem("Reserve", [cur_time, win[1] - win[0] + cur_time])]
        cur_time += win[1] - win[0]
    else: # create window with crashed task and it's reserve
        windows_nvp += [Window_elem("Main_crash", [cur_time, win[1] - win[0] + cur_time])]
        cur_time += win[1] - win[0]
        windows_nvp += [Window_elem("Fixator", [cur_time, cur_time + FIXATOR_TIME])]
        cur_time += FIXATOR_TIME
        windows_nvp += [Window_elem("Reserve_crash", [cur_time, win[1] - win[0] + cur_time])]
        cur_time += win[1] - win[0]
for win in windows_nvp: 
    print(win)
MF_PERIOD = windows_nvp[-1].time[1]
# --------------------------------------------------------------------------------------------------------------



# Creating graphs for all windows
# set a graph for window with crash
# --------------------------------------------------------------------------------------------------------------
main_window_crash_graph_edges = []
for e in GRAPH_INITIAL_APP.es:  
    edge_inside = True
    for task_crash in e.tuple:
        if not (task_crash in window_crash_task_set):
            edge_inside = False
            break
    if edge_inside:
        main_window_crash_graph_edges += [[*e.tuple]]
# --------------------------------------------------------------------------------------------------------------


# GRAPH RE-FORMING:
# graph: 1 3 5 [[1, 3], [3, 5]] to 0 1 2 [[0, 1], [1, 2]] 
# --------------------------------------------------------------------------------------------------------------
graph_main_crash = ig.Graph()
main_window_graph_old_to_new_points = {} # set for mapping an old vertex number to new
for i in range(len(window_crash_task_set)):
    cur_task = window_crash_task_set[i]
    for j in range(len(main_window_crash_graph_edges)): 
        for p in range(len(main_window_crash_graph_edges[j])): 
            if main_window_crash_graph_edges[j][p] == cur_task:
                main_window_graph_old_to_new_points[cur_task] = [i]
                main_window_crash_graph_edges[j][p] = i
    graph_main_crash.add_vertex(cur_task)
# --------------------------------------------------------------------------------------------------------------




# CREATING GRAPH FOR WINDOW WITH CRASH
# --------------------------------------------------------------------------------------------------------------
graph_main_crash.add_edges(main_window_crash_graph_edges)
main_window_crash_task_time = [GRAPH_INITIAL_APP.vs[i]["duration"] for i in range(len(GRAPH_INITIAL_APP.vs)) if i in window_crash_task_set]
graph_main_crash.vs["duration"] = main_window_crash_task_time
# --------------------------------------------------------------------------------------------------------------



# CREATING GRAPH FOR RESERVE WINDOW 
# --------------------------------------------------------------------------------------------------------------
second_main_app_graph = GRAPH_INITIAL_APP.copy()
second_main_app_graph.vs["name"] = [str(i) for i in range(len(GRAPH_INITIAL_APP.vs))]
for i in window_crash_task_set:
    second_main_app_graph.delete_vertices(str(i))
# --------------------------------------------------------------------------------------------------------------


# WRITING XML FOR MODELLING NVP 
# --------------------------------------------------------------------------------------------------------------
write_nvp_xml(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP)
# --------------------------------------------------------------------------------------------------------------

# RUNNING MODELLING SYSTEM FOR 
# --------------------------------------------------------------------------------------------------------------
os.system("cp test_nvp.xml  MCSSim/generator/model_builder") 
os.system("cd ./MCSSim/generator/model_builder; ./model_builder test_nvp.xml > result.txt; cd -")
os.system("cp ./MCSSim/generator/model_builder/result.txt .") 
# --------------------------------------------------------------------------------------------------------------



# visualazing nvp
parsing = parser_.INTERVAL()
"""Here specify input file."""
inter2 = parsing.create_int("result.txt")
parsing.print_intervals()


visioner2 = vision.VISUALISER()
"""Here you can specify name of output file."""
visioner2.visualise(inter2, [i.time[0] for i in windows_nvp], PICTURE_FILENAME_NVP, MF_PERIOD)

create_double_visualization(PICTURE_FILENAME_INITIAL_APP, PICTURE_FILENAME_NVP, TASK_CRASHED_ID)

