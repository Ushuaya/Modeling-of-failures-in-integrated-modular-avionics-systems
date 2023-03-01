"""This is parser for creating in input for visualizer from output of system of imitation modelling. 
You have to specify the output file to run parser."""

class INTERVAL:
    task_intervals = {}
    task_intervals_int = {}
    def create_int(self, filename):
        self.task_intervals = {}
        with open(filename, "r") as file:
            txt_list = file.read().split()
            for i in range(len(txt_list)): 
                if txt_list[i] == "<task":
                    this_name = txt_list[i+2].split('\"')[-2]
                    this_id = int(txt_list[i+1].split('\"')[-2])
                    self.task_intervals[this_name] = []
                    self.task_intervals_int[this_id] = []
                    while True:
                        while txt_list[i].split("=")[0] != "time" and txt_list[i] != "</task>":
                            i+=1
                        if txt_list[i].split("=")[0] == "time":
                            this_time = txt_list[i].split("\"")[-2]
                            self.task_intervals[this_name].append(this_time)
                            self.task_intervals_int[this_id].append(this_time)
                            i+=1
                        else:
                            break
        return self.task_intervals, self.task_intervals_int

    def print_intervals(self):
        print(self.task_intervals)
        print(self.task_intervals_int)
