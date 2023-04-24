import igraph as ig
import os
import re
import parser_
import vision
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pickle

from reader import read_data

# DEFINING SOME VARAIBLES TO MAKE MODELLING SYSTEM ABLE TO RUN 
# ----------------------------------------------------------------------
TASK_CRASHED_ID = 0
# use it only in a case when task is separated on two part in different partitions (0 or 1 means left or right)
CRASHED_PART_OF_TASK = 0
MF_PERIOD = 100
FIXATOR_TIME = 1

GRAPH_INITIAL_APP = ig.Graph(n=22, edges=[ ])
GRAPH_INITIAL_APP.vs["duration"] = [8, 8, 8] + [random.randint(3,5) for _ in range(len(GRAPH_INITIAL_APP.vs) - 3)]

# Partition numbers sequence must start from 0 
MAP_PARTITION_TASK = {0: (0, 1, 2), 1: (3, 4, 5), 2: (6, 7, 8, 9, 10)}
MAP_WINDOW_PARTITION = {(0, 20): 0, (20, 40): 0, (40, 80): 2, (80, 100): 1}
#MAP_WINDOW_PARTITION = dict((v,k) for k,v in MAP_PARTITION_WINDOW.items())
#MAP_PARTITION_WINDOW = {0: (0, 20), 1: (20, 40), 2: (40, 80), 0: (80, 100)}

# -------- OR ---------

# INPUT FROM EXTERNAL FILE
# --------------------------------------------------------------------------------------------------------------
TASK_CRASHED_ID, CRASHED_PART_OF_TASK, MF_PERIOD, FIXATOR_TIME, GRAPH_INITIAL_APP, MAP_PARTITION_TASK, MAP_WINDOW_PARTITION = read_data(TASK_CRASHED_ID, CRASHED_PART_OF_TASK, MF_PERIOD, FIXATOR_TIME, GRAPH_INITIAL_APP, MAP_PARTITION_TASK, MAP_WINDOW_PARTITION)
# --------------------------------------------------------------------------------------------------------------


# Hense we can create: 
# --------------------------------------------------------------------------------------------------------------
MAP_WINDOWSTARTTIME_PARTITION = dict((k[0] ,v) for k,v in MAP_WINDOW_PARTITION.items())


WINDOWS = [i for i in MAP_WINDOW_PARTITION]
PICTURE_FILENAME_INITIAL_APP = "initial_app"
PICTURE_FILENAME_NVP = "nvp_fault"
# ----------------------------------------------------------------------



class Window_elem():
    application = None
    time = None
    partition_number = None

    def __init__(self, application, time, partition_number = None):
        self.application = application
        self.time = time
        self.partition_number = partition_number

    def new_elem(self, application, time, partition_number = None):
        self.application = application
        self.time = time
        self.partition_number = partition_number

    def __str__(self) -> str:
        return "Window:\n" + "\tapp: " + str(self.application) + "\n" + "\tTime: " + str(self.time) + "\n" + "\tNumber: " + str(self.partition_number)


def rename_separate_tasks(DICT):
    DICT_NEW = DICT.copy()
    for tsk in DICT:
        if len(DICT[tsk]) == 4:
            DICT_NEW[tsk + "__p1"] = DICT_NEW[tsk][0:2]
            DICT_NEW[tsk + "__p2"] = DICT_NEW[tsk][2:4]
            
            del DICT_NEW[tsk]
    return DICT_NEW


def create_map_window_to_task_name(DICT, TASK_INTERVALS, WINDOWS_SCHEDULE) -> None:
    set_of_sep_tsk = set()

    for tsk in TASK_INTERVALS:
        SEPARATE_TASK = False
        if len(TASK_INTERVALS[tsk]) > 2: 
            SEPARATE_TASK = True
            set_of_sep_tsk.add(tsk)
        if SEPARATE_TASK:  
            t_begin_1 = TASK_INTERVALS[tsk][0]
            t_begin_2 = TASK_INTERVALS[tsk][2]
            fst_found = False
            for num_win in range(len(WINDOWS_SCHEDULE)):
                if not fst_found:
                    if int(t_begin_1) >= int(WINDOWS_SCHEDULE[num_win][0]) and int(t_begin_1) < int(WINDOWS_SCHEDULE[num_win][1]):
                        if WINDOWS_SCHEDULE[num_win] not in DICT:
                            DICT[WINDOWS_SCHEDULE[num_win]] = [tsk]
                        else:
                            DICT[WINDOWS_SCHEDULE[num_win]].append(tsk)
                        fst_found = True
                else:
                    if int(t_begin_2) >= int(WINDOWS_SCHEDULE[num_win][0]) and int(t_begin_2) < int(WINDOWS_SCHEDULE[num_win][1]):
                        if WINDOWS_SCHEDULE[num_win] not in DICT:
                            DICT[WINDOWS_SCHEDULE[num_win]] = [tsk]
                        else:
                            DICT[WINDOWS_SCHEDULE[num_win]].append(tsk)
                        break
        else:
            t_begin = TASK_INTERVALS[tsk][0]
            t_end = TASK_INTERVALS[tsk][1]
            for num_win in range(len(WINDOWS_SCHEDULE)):
                if int(t_begin) >= int(WINDOWS_SCHEDULE[num_win][0]) and int(t_begin) < int(WINDOWS_SCHEDULE[num_win][1]):
                    if WINDOWS_SCHEDULE[num_win] not in DICT:
                        DICT[WINDOWS_SCHEDULE[num_win]] = [tsk]
                    else:
                        DICT[WINDOWS_SCHEDULE[num_win]].append(tsk)
                    break
    return set_of_sep_tsk
                    

def create_double_visualization(filename1, filename2, task_crasshed_id): 
    img = Image.new('RGB', (256*8, 256*4))
    img1 = Image.open(filename1 + ".png")
    img2 = Image.open(filename2 + ".png")
    img.paste(img1, (0,0))
    img.paste(img2, (0,256*2))
    print("dir: ", dir(img))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font="./open-sans/OpenSans-ExtraBold.ttf", size=40)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((250, 10),"No fault",(0,0,0), font=font )
    draw.text((40, 256*2 + 10),"Crashed task: " + str(task_crasshed_id) + "; Part of crashed task: " + ("Left" if CRASHED_PART_OF_TASK == 0 else "Right"),(0,0,0), font=font )
    with open("num_test.pkl", "rb") as file:
        next_test = pickle.load(file)
        try: 
            os.mkdir("./tests_nvp_2/test{}".format(next_test))
        except:
            pass
        img.show()
        img.save("./tests_nvp_2/test{}/RESULT.png".format(next_test))
        next_test += 1
    with open("num_test.pkl", "wb") as file:
        pickle.dump(next_test, file)
    
def Write_xml_first_iter(filename, MF_PERIOD, GRAPH_INITIAL_APP, windows, MAP_TASK_PARTITION, WINDOW_PARTITION):
    with open(filename, "w") as file: 
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<system>\n")
        file.write("\t<module major_frame=\"{}\" name=\"core1\">\n".format(MF_PERIOD))

        for i in MAP_TASK_PARTITION: 
            file.write("\t\t<partition id=\"{}\" name=\"part{}\" scheduler=\"FPPS\">\n".format(i,i,))
            for j in MAP_TASK_PARTITION[i]:
                file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, j, j, MF_PERIOD, GRAPH_INITIAL_APP.vs[j]["duration"]))
            file.write("\t\t</partition>\n")

        for i in WINDOW_PARTITION:
            #file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(i, PARTITION_WINDOW[i][0], PARTITION_WINDOW[i][1]))
            file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(WINDOW_PARTITION[i], i[0], i[1]))

        file.write("\t</module>\n")
        for e in GRAPH_INITIAL_APP.es:
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0], e.tuple[1]))
        file.write("</system>\n")


def Find_carsh_window_crash_set(filename, TASK_CRASHED_ID, windows, SET_OF_SEPARATED_TASKS, CRASHED_PART_OF_TASK,):
    with open(filename) as file:
        txt = file.read().split("\n")
        #print(txt)
        crashed_task_pos = -1
        time_task_crash_start = -1
        time_task_crash_finish = -1

        if TASK_CRASHED_ID in SET_OF_SEPARATED_TASKS:
            if CRASHED_PART_OF_TASK == 1:
                for txt_line_num in range(len(txt)):
                    if (crashed_task_pos := txt[txt_line_num].find("task id=\"{}\"".format(TASK_CRASHED_ID))) != -1: 
                        time_task_crash_start = txt[txt_line_num + 4].find("time")
                        time_task_crash_finish = txt[txt_line_num + 5].find("time")
                        if (time_task_crash_start != -1):
                            time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 4])[0])
                            time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 5])[0])

                        break 
            else:
                for txt_line_num in range(len(txt)):
                    if (crashed_task_pos := txt[txt_line_num].find("task id=\"{}\"".format(TASK_CRASHED_ID))) != -1: 
                        time_task_crash_start = txt[txt_line_num + 2].find("time")
                        time_task_crash_finish = txt[txt_line_num + 3].find("time")
                        if (time_task_crash_start != -1):
                            time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                            time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])

                        break 
        else:
            for txt_line_num in range(len(txt)):
                if (crashed_task_pos := txt[txt_line_num].find("task id=\"{}\"".format(TASK_CRASHED_ID))) != -1: 
                    time_task_crash_start = txt[txt_line_num + 2].find("time")
                    time_task_crash_finish = txt[txt_line_num + 3].find("time")
                    if (time_task_crash_start != -1):
                        time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                        time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])

                    break 

        
        if crashed_task_pos != -1 and time_task_crash_start != -1 and time_task_crash_finish != -1:
            window_crashed = [i for i in [i if (time_task_crash_start_num >= i[0] and time_task_crash_finish_num >= i[0] and time_task_crash_start_num <= i[1] and time_task_crash_finish_num <= i[1]) else None for i in windows] if i is not None][0]
            window_crashed = {"window_time": window_crashed, "window_number": windows.index(window_crashed)}
        else: 
            raise "didn't find broken task number {} in xml".format(TASK_CRASHED_ID)
        # in window_crashed there is time and number in sequense, of a window where error happend

        # Searching for a set of tasks in window where error happend
        window_crash_task_set = []
        for txt_line_num in range(len(txt)):
            if (crashed_task_pos := txt[txt_line_num].find("task id=")) != -1: 
                task_id = int(re.findall(r'\d+', txt[txt_line_num])[0])
                if task_id in SET_OF_SEPARATED_TASKS:
                    time_task_crash_start_1 = txt[txt_line_num + 2].find("time")
                    time_task_crash_finish_1 = txt[txt_line_num + 3].find("time")
                    time_task_crash_start_2 = txt[txt_line_num + 4].find("time")
                    time_task_crash_finish_2 = txt[txt_line_num + 5].find("time")

                    if (time_task_crash_start_1 != -1):
                        time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                    if (time_task_crash_finish_1 != -1):
                        time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])
                    if (time_task_crash_start_num >= window_crashed["window_time"][0] and time_task_crash_finish_num >= window_crashed["window_time"][0] and time_task_crash_start_num <= window_crashed["window_time"][1] and time_task_crash_finish_num <= window_crashed["window_time"][1]):
                        window_crash_task_set += [task_id]

                    if (time_task_crash_start_2 != -1):
                        time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 4])[0])
                    if (time_task_crash_finish_2 != -1):
                        time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 5])[0])
                    if (time_task_crash_start_num >= window_crashed["window_time"][0] and time_task_crash_finish_num >= window_crashed["window_time"][0] and time_task_crash_start_num <= window_crashed["window_time"][1] and time_task_crash_finish_num <= window_crashed["window_time"][1]):
                        window_crash_task_set += [task_id]
    
                else:
                    time_task_crash_start = txt[txt_line_num + 2].find("time")
                    time_task_crash_finish = txt[txt_line_num + 3].find("time")
                    if (time_task_crash_start != -1):
                        time_task_crash_start_num = int(re.findall(r'\d+', txt[txt_line_num + 2])[0])
                    if (time_task_crash_finish != -1):
                        time_task_crash_finish_num = int(re.findall(r'\d+', txt[txt_line_num + 3])[0])
                    if (time_task_crash_start_num >= window_crashed["window_time"][0] and time_task_crash_finish_num >= window_crashed["window_time"][0] and time_task_crash_start_num <= window_crashed["window_time"][1] and time_task_crash_finish_num <= window_crashed["window_time"][1]):
                        window_crash_task_set += [int(re.findall(r'\d+', txt[txt_line_num])[0])]
    
    return window_crashed, window_crash_task_set 

def write_nvp_xml_no_fault(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP, CRASHED_PART_OF_TASK, window_crash_task_set):
    return_val = None
    with open("test_nvp.xml", "w") as file: 
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<system>\n")
        file.write("\t<module major_frame=\"{}\" name=\"core1\">\n\n".format(MF_PERIOD))

        graph_reserve_window = graph_main_crash.copy() 
        graph_fixator = ig.Graph(n = len(windows_nvp)//2 - 1)
        graph_fixator.vs["duration"] = [FIXATOR_TIME for _ in range(len(windows_nvp)//2 - 1)]
        graph_fixator.vs["name"] = [str(i) for i in graph_fixator.vs.indices]


        # case with separated tasks -- we eliminate right part of task, bcs whole task will be in reserve
        # --------------------------------------------------------------------------------------------------------------
        if CRASHED_PART_OF_TASK == 0:
            for i in graph_main_crash.vs.indices:
                if i in SET_OF_SEPARATED_TASKS and i in window_crash_task_set and i == TASK_CRASHED_ID:
                    tmp_lst = list(map(int ,inter_int[i][0:2]))
                    graph_main_crash.vs[i]["duration"] = tmp_lst[1] - tmp_lst[0]
        else: 
            for i in graph_main_crash.vs.indices:
                tmp = graph_main_crash.vs[i]["name"]
                if tmp in SET_OF_SEPARATED_TASKS and tmp in window_crash_task_set and tmp == TASK_CRASHED_ID:
                    tmp_lst = list(map(int ,inter_int[tmp][2:4]))
                    tmp_durat = graph_main_crash.vs[i]["duration"]
                    graph_main_crash.vs[i]["duration"] = tmp_lst[1] - tmp_lst[0]
                    # in the case when right part of the separated task has an error -- we must remeber, that on the reserve core whole task must be restarted. 
                    # We must save this info -- task, it's time of performing on both of cores
                    return_val = {"task_id" : tmp, "old_time": tmp_durat, "new_time": tmp_lst[1] - tmp_lst[0]}

        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
       
       
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
        
        # All_win_dict = {"Main": 0, "Main_crash": 1, "Reserve_crash": 2, "Fixator": 3,  "Reserve": 4}
        # CREATING MAP FROM PARTITION TO IT'S ID
        # --------------------------------------------------------------------------------------------------------------
        Map_partition_id = {}
        counter = 0
        for i in windows_nvp:
            if i.application not in Map_partition_id:
                if i.partition_number != None:
                    Map_partition_id[i.application] = i.partition_number
                    counter += 1

        #Map_partition_id["Reserve_crash"] = len(Map_partition_id)
        Map_partition_id["Fixator"] = len(Map_partition_id)
        #Map_partition_id["Reserve"] = len(Map_partition_id)
        # --------------------------------------------------------------------------------------------------------------


        # Writing file 
        # --------------------------------------------------------------------------------------------------------------
        Task_id_cout = 0 # Varaible to create unique numeric ids of tasks
        tmp_count = 0
        been_wrote = set()
        for q_partition in Map_partition_id:
            if True: #Map_partition_id[q_partition] not in been_wrote:
                been_wrote.add(Map_partition_id[q_partition])
                
                if q_partition == "Fixator":
                    Map_partition_id["Fixator"] = tmp_count

                file.write("\t\t<partition id=\"{}\" name=\"part_{}\" scheduler=\"FPPS\">\n".format(Map_partition_id[q_partition], q_partition ))
               
                if q_partition.startswith("Main_part"):
                    for i in range(len(All_graphs_nvp_dict["Main"].vs)):
                        tmp1 = int(All_graphs_nvp_dict["Main"].vs[i]["name"])
                        tmp2 = MAP_PARTITION_TASK[Map_partition_id[q_partition]]
                        if tmp1 in tmp2:
                            if tmp1 == TASK_CRASHED_ID:
                                tmp_name = "_ERR"
                            else:
                                tmp_name = ""
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, str(int(All_graphs_nvp_dict["Main"].vs[i]["name"])), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict["Main"].vs[i]["duration"]))
                            MAP__NAMES_IN_FILE__ID__NO_ERR[q_partition + str(i) + tmp_name] = tmp1

                elif q_partition == "Main_crash":
                    for i in range(len(All_graphs_nvp_dict[q_partition].vs)):
                        if int(All_graphs_nvp_dict[q_partition].vs[i]["name"]) == TASK_CRASHED_ID:
                            tmp_name = "_ERR"
                        else:
                            tmp_name = ""
                        if i in SET_OF_SEPARATED_TASKS: 
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, Task_id_cout + len(GRAPH_INITIAL_APP.vs), q_partition + str(i), MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                        else:
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, str(int(All_graphs_nvp_dict[q_partition].vs[i]["name"])), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                        MAP__NAMES_IN_FILE__ID__NO_ERR[q_partition + str(i) + tmp_name] = int(All_graphs_nvp_dict[q_partition].vs[i]["name"])

                else:
                    if q_partition != "Reserve_crash":
                        for i in range(len(All_graphs_nvp_dict[q_partition].vs)):
                            if int(All_graphs_nvp_dict[q_partition].vs[i]["name"]) == TASK_CRASHED_ID and q_partition != "Fixator":
                                tmp_name = "_ERR"
                            else:
                                tmp_name = ""
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, Task_id_cout + len(GRAPH_INITIAL_APP.vs), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                            MAP__NAMES_IN_FILE__ID__NO_ERR[q_partition + str(i) + tmp_name] = int(All_graphs_nvp_dict[q_partition].vs[i]["name"])
                            Task_id_cout += 1
                file.write("\t\t</partition>\n\n")
                tmp_count += 1
        

        Map_partition_id["Reserve"] = len(Map_partition_id)

        for i in range(len(windows_nvp)):
            #Window_elem("Main", [cur_time, win[1] - win[0] + cur_time])
            file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(Map_partition_id[windows_nvp[i].application], windows_nvp[i].time[0], windows_nvp[i].time[1]))
        file.write("\t</module>\n")

        for e in GRAPH_INITIAL_APP.es:
            # _res indicates, that message must be sent to or from the other version of the task
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0], e.tuple[1] ))

        for e in graph_reserve_window.es:
            # _res indicates, that message must be sent to or from the other version of the task
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0] + len(GRAPH_INITIAL_APP.vs), e.tuple[1] + len(GRAPH_INITIAL_APP.vs)))

        file.write("</system>\n")
        # --------------------------------------------------------------------------------------------------------------
        
        return return_val


def write_nvp_xml(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP, CRASHED_PART_OF_TASK, window_crash_task_set):
    with open("test_nvp.xml", "w") as file: 
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<system>\n")
        file.write("\t<module major_frame=\"{}\" name=\"core1\">\n\n".format(MF_PERIOD))

        graph_reserve_window = graph_main_crash.copy() 
        graph_fixator = ig.Graph(n = len(windows_nvp)//2 - 1)
        graph_fixator.vs["duration"] = [FIXATOR_TIME for _ in range(len(windows_nvp)//2 - 1)]
        graph_fixator.vs["name"] = [str(i) for i in graph_fixator.vs.indices]


        # case with separated tasks -- we eliminate right part of task, bcs whole task will be in reserve
        # --------------------------------------------------------------------------------------------------------------
        if CRASHED_PART_OF_TASK == 0:
            for i in graph_main_crash.vs.indices:
                if i in SET_OF_SEPARATED_TASKS and i in window_crash_task_set and i == TASK_CRASHED_ID:
                    tmp_lst = list(map(int ,inter_int[i][0:2]))
                    graph_main_crash.vs[i]["duration"] = tmp_lst[1] - tmp_lst[0]
        else: 
            for i in graph_main_crash.vs.indices:
                if i in SET_OF_SEPARATED_TASKS and i in window_crash_task_set and i == TASK_CRASHED_ID:
                    tmp_lst = list(map(int ,inter_int[i][2:4]))
                    graph_main_crash.vs[i]["duration"] = tmp_lst[1] - tmp_lst[0]
        # --------------------------------------------------------------------------------------------------------------

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
        
        # All_win_dict = {"Main": 0, "Main_crash": 1, "Reserve_crash": 2, "Fixator": 3,  "Reserve": 4}
        # CREATING MAP FROM PARTITION TO IT'S ID
        Map_partition_id = {}
        counter = 0
        for i in windows_nvp:
            if i.application not in Map_partition_id:
                if i.partition_number != None:
                    Map_partition_id[i.application] = i.partition_number
                    counter += 1

        Map_partition_id["Fixator"] = len(Map_partition_id)


        # Writing file 
        # --------------------------------------------------------------------------------------------------------------
        Task_id_cout = 0 # Varaible to create unique numeric ids of tasks
        tmp_count = 0
        been_wrote = set()
        for q_partition in Map_partition_id:
            if True: #Map_partition_id[q_partition] not in been_wrote:
                been_wrote.add(Map_partition_id[q_partition])
                
                if q_partition == "Fixator":
                    Map_partition_id["Fixator"] = tmp_count

                file.write("\t\t<partition id=\"{}\" name=\"part_{}\" scheduler=\"FPPS\">\n".format(Map_partition_id[q_partition], q_partition ))
               
                if q_partition.startswith("Main_part"):
                    for i in range(len(All_graphs_nvp_dict["Main"].vs)):
                        tmp1 = int(All_graphs_nvp_dict["Main"].vs[i]["name"])
                        tmp2 = MAP_PARTITION_TASK[Map_partition_id[q_partition]]
                        if tmp1 in tmp2:
                            if tmp1 == TASK_CRASHED_ID:
                                tmp_name = "_ERR"
                            else:
                                tmp_name = ""
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, str(int(All_graphs_nvp_dict["Main"].vs[i]["name"])), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict["Main"].vs[i]["duration"]))
                            MAP__NAMES_IN_FILE__ID__ERR[q_partition + str(i) + tmp_name] = tmp1

                elif q_partition == "Main_crash":
                    for i in range(len(All_graphs_nvp_dict[q_partition].vs)):
                        if int(All_graphs_nvp_dict[q_partition].vs[i]["name"]) == TASK_CRASHED_ID:
                            tmp_name = "_ERR"
                        else:
                            tmp_name = ""
                        if i in SET_OF_SEPARATED_TASKS: 
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, Task_id_cout + len(GRAPH_INITIAL_APP.vs), q_partition + str(i), MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                        else:
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, str(int(All_graphs_nvp_dict[q_partition].vs[i]["name"])), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                        MAP__NAMES_IN_FILE__ID__ERR[q_partition + str(i) + tmp_name] = int(All_graphs_nvp_dict[q_partition].vs[i]["name"])

                else:
                    if q_partition != "Reserve_crash":
                        for i in range(len(All_graphs_nvp_dict[q_partition].vs)):
                            if int(All_graphs_nvp_dict[q_partition].vs[i]["name"]) == TASK_CRASHED_ID and q_partition != "Fixator":
                                tmp_name = "_ERR"
                            else:
                                tmp_name = ""
                            file.write("\t\t\t<task deadline=\"{}\" id=\"{}\" name=\"task_{}\" offset=\"0\" period=\"{}\" prio=\"1\" wcet=\"{}\"/>\n".format(MF_PERIOD - 1, Task_id_cout + len(GRAPH_INITIAL_APP.vs), q_partition + str(i) + tmp_name, MF_PERIOD, All_graphs_nvp_dict[q_partition].vs[i]["duration"]))
                            MAP__NAMES_IN_FILE__ID__ERR[q_partition + str(i) + tmp_name] = int(All_graphs_nvp_dict[q_partition].vs[i]["name"])
                            Task_id_cout += 1
                file.write("\t\t</partition>\n\n")
                
                tmp_count += 1


        Map_partition_id["Reserve"] = len(Map_partition_id)


        for i in range(len(windows_nvp)):
            file.write("\t\t<window partition=\"{}\" start=\"{}\" stop=\"{}\"/>\n".format(Map_partition_id[windows_nvp[i].application], windows_nvp[i].time[0], windows_nvp[i].time[1]))
        file.write("\t</module>\n")

        for e in GRAPH_INITIAL_APP.es:
            # _res indicates, that message must be sent to or from the other version of the task
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0], e.tuple[1] ))

        for e in graph_reserve_window.es:
            # _res indicates, that message must be sent to or from the other version of the task
            file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0] + len(GRAPH_INITIAL_APP.vs), e.tuple[1] + len(GRAPH_INITIAL_APP.vs)))

        # for e in second_main_app_graph.es:
        #     # _res indicates, that message must be sent to or from the other version of the task
        #     file.write("\t<link delay=\"0\" dst=\"{}\" src=\"{}\"/>\n".format(e.tuple[0], e.tuple[1] ))


        file.write("</system>\n")
        # --------------------------------------------------------------------------------------------------------------

# CHECKING FOR VALID INPUT
# --------------------------------------------------------------------------------------------------------------
# for i in WINDOWS: 
#     if i[1] - i[0] <= 0:
#         raise "window size <= 0"
#     for j in GRAPH_INITIAL_APP.vs["duration"]:
#         if j > (i[1] - i[0]):
#             raise "to big task {}".format(j)
#         if (i[1] - i[0])%j != 0:
#             raise "Invalid task duration. Must be mupliple of window size, to aviod task preemt.".format(j)
# --------------------------------------------------------------------------------------------------------------





# CREATING XML FILE FOR FIRST ITERATION OF ALGORYTHM 
# --------------------------------------------------------------------------------------------------------------
Write_xml_first_iter("test.xml", MF_PERIOD, GRAPH_INITIAL_APP, WINDOWS, MAP_PARTITION_TASK, MAP_WINDOW_PARTITION)
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
inter, inter_int = parsing.create_int("result.txt")
parsing.print_intervals()



# CREATING MAP FROM WINDOW AS TIME INTERVAL TO THE NAME OF THE TASK (HERE LLEFT PARTS RENAME TO <tsk_name>__p1 and RIGHT to <tsk_name>__p2)
# --------------------------------------------------------------------------------------------------------------

# here we separate tasks with two parts to the new two tasks
# separate_tak_intervals = rename_separate_tasks(inter)
# --------------------------------------------------------------------------------------------------------------
separate_tak_intervals = inter_int

MAP_WINDOW_TASK = {}
SET_OF_SEPARATED_TASKS = create_map_window_to_task_name(DICT=MAP_WINDOW_TASK, TASK_INTERVALS=separate_tak_intervals, WINDOWS_SCHEDULE=WINDOWS)
# --------------------------------------------------------------------------------------------------------------

# FINDING A SET OF TASKS IN WINDOW WITH ERROR OCCURED
# --------------------------------------------------------------------------------------------------------------
window_crashed, window_crash_task_set = Find_carsh_window_crash_set("./result.txt", TASK_CRASHED_ID, WINDOWS, SET_OF_SEPARATED_TASKS, CRASHED_PART_OF_TASK)
# --------------------------------------------------------------------------------------------------------------


# creating window sequence
# we must remember, as it is discribed in the article, that length of reserve window equal to the summ of the all tasks time in prev
# window, including separated -- we summ both parts of it
# --------------------------------------------------------------------------------------------------------------
windows_nvp = []
cur_time = 0
for win in WINDOWS: 
    if win[0] != window_crashed["window_time"][0]:
        windows_nvp += [Window_elem("Main" + "_part_" + str(MAP_WINDOWSTARTTIME_PARTITION[win[0]]), [cur_time, win[1] - win[0] + cur_time], MAP_WINDOWSTARTTIME_PARTITION[win[0]])]
        cur_time += win[1] - win[0]
        windows_nvp += [Window_elem("Fixator", [cur_time, cur_time + FIXATOR_TIME])]
        cur_time += FIXATOR_TIME
        
    else: # create window with crashed task and it's reserve
        windows_nvp += [Window_elem("Main_crash", [cur_time, win[1] - win[0] + cur_time], window_crashed["window_number"])]
        cur_time += win[1] - win[0]
        windows_nvp += [Window_elem("Fixator", [cur_time, cur_time + FIXATOR_TIME])]
        cur_time += FIXATOR_TIME

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

print("\n------------")
print(graph_main_crash)
for i in graph_main_crash.vs: 
    print(i)
print("------------\n")

# --------------------------------------------------------------------------------------------------------------

# CREATING GRAPH FOR RESERVE WINDOW 
# --------------------------------------------------------------------------------------------------------------
second_main_app_graph = GRAPH_INITIAL_APP.copy()
second_main_app_graph.vs["name"] = [str(i) for i in range(len(GRAPH_INITIAL_APP.vs))]
for i in window_crash_task_set:
    if i not in SET_OF_SEPARATED_TASKS:
        second_main_app_graph.delete_vertices(str(i))
# --------------------------------------------------------------------------------------------------------------

# WRITING XML FOR MODELLING NVP 
# --------------------------------------------------------------------------------------------------------------
MAP__NAMES_IN_FILE__ID__NO_ERR = {}
info_task_err_right_prt = write_nvp_xml_no_fault(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP=GRAPH_INITIAL_APP, CRASHED_PART_OF_TASK=CRASHED_PART_OF_TASK, window_crash_task_set=window_crash_task_set)
# --------------------------------------------------------------------------------------------------------------

# RUNNING MODELLING SYSTEM FOR CASE WITHOUT FAULT
# --------------------------------------------------------------------------------------------------------------
os.system("cp test_nvp.xml  MCSSim/generator/model_builder") 
os.system("cd ./MCSSim/generator/model_builder; ./model_builder test_nvp.xml > result_nvp.txt; cd -")
os.system("cp ./MCSSim/generator/model_builder/result_nvp.txt .") 
# --------------------------------------------------------------------------------------------------------------

# visualazing nvp
parsing = parser_.INTERVAL()
"""Here specify input file."""
inter2, inter2_int = parsing.create_int("result_nvp.txt")

visioner2 = vision.VISUALISER()
"""Here you can specify name of output file."""

merge_file_2 = visioner2.visualise_nvp_2_no_fault(inter2, [i.time[0] for i in windows_nvp] + [windows_nvp[-1].time[1] + 1], PICTURE_FILENAME_NVP, MF_PERIOD, window_crashed, FIXATOR_TIME, MAP__NAMES_IN_FILE__ID__NO_ERR)


# WRITING XML FOR MODELLING NVP 
# --------------------------------------------------------------------------------------------------------------
MAP__NAMES_IN_FILE__ID__ERR = {}
write_nvp_xml(graph_main_crash, MF_PERIOD, windows_nvp, second_main_app_graph, GRAPH_INITIAL_APP=GRAPH_INITIAL_APP, CRASHED_PART_OF_TASK=CRASHED_PART_OF_TASK, window_crash_task_set=window_crash_task_set)
# --------------------------------------------------------------------------------------------------------------

# RUNNING MODELLING SYSTEM FOR CASE WITH FAULT
# --------------------------------------------------------------------------------------------------------------
os.system("cp test_nvp.xml  MCSSim/generator/model_builder") 
os.system("cd ./MCSSim/generator/model_builder; ./model_builder test_nvp.xml > result_nvp.txt; cd -")
os.system("cp ./MCSSim/generator/model_builder/result_nvp.txt .") 
# --------------------------------------------------------------------------------------------------------------



# visualazing nvp# --------------------------------------------------------------------------------------------------------------
parsing = parser_.INTERVAL()
"""Here specify input file."""
inter2, inter2_int = parsing.create_int("result_nvp.txt")
parsing.print_intervals()



merge_file_1 = visioner2.visualise_nvp_2(inter2, [i.time[0] for i in windows_nvp] + [windows_nvp[-1].time[1] + 1], PICTURE_FILENAME_NVP, MF_PERIOD, window_crashed, FIXATOR_TIME, MAP__NAMES_IN_FILE__ID__ERR, info_task_err_right_prt)
# --------------------------------------------------------------------------------------------------------------




create_double_visualization(merge_file_2, merge_file_1, TASK_CRASHED_ID)


