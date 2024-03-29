"""This is visualizer of NVP with one kernel mechanism. You must run the parser cell before running this cell. 
Visualizer works with no more than 240 seconds programm."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pickle
import os

class VISUALISER:
    """Class, that visualise given dict with time intervals."""
    
    colours = ['#eaaaff', 'blue', 'orange', 'green', 'purple', 'red', 'brown', 'pink', 'gray', 'olive', 'cyan']

    def visualise(self, dict_inter, windws, filename = "graph.out", MF_period = 240, MAP__NAMES_IN_FILE__ID__ERR = {}):
        """Visualisation using matplotlib."""
        begins = []
        ends = []
        fig, ax = plt.subplots()
        j = 0
        y_offset = [0.03*j for j in range(8)]
        for i in dict_inter: 
            begins =list(map(int, dict_inter[i][::2]))
            ends =list(map(int, dict_inter[i][1::2]))
            df = pd.DataFrame({"begin": begins, "end" : ends})
            colour = self.colours[j%len(self.colours)]
            ax.broken_barh(list(zip(df["begin"].values, 
                            (df["end"] - df["begin"]).values)), 
                            (0, 0.5), facecolors=(colour))
            j+=1

            if "_ERR" in i:
                stp_lst = [0 + (j * 0.5)/20 for j in range(20)]
                for step in stp_lst:
                    l_p = step
                    r_p = step + 0.00625
                    ax.broken_barh(list(zip(df["begin"].values, 
                            (df["end"] - df["begin"]).values)), 
                            (l_p, 0.0125), facecolors=(['black']))

            count_index = 0
            for p in begins:
                if MAP__NAMES_IN_FILE__ID__ERR and "Fixator" not in i:
                    ax.annotate(str(MAP__NAMES_IN_FILE__ID__ERR[i[5:]]), (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/MF_period, 0.7 + y_offset[j%len(y_offset)]), 
                            textcoords='axes fraction', fontsize=16, 
                            arrowprops=dict(shrink=0.0001))
                else:
                    ax.annotate(i, (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/MF_period, 0.8 + y_offset[j%len(y_offset)]), 
                            textcoords='axes fraction', fontsize=16,
                            arrowprops=dict(shrink=0.0001))
                count_index += 1
            

        begins = []
        ends = []

        for i in windws:
            begins.append(i)
            ends.append(i+0.5)

        

            
        df = pd.DataFrame({"begin": begins, "end" : ends})
        ax.broken_barh(list(zip(df["begin"].values, 
                        (df["end"] - df["begin"]).values)), 
                        (0, 1), facecolors='black')
        ax.set_ylim(0, 1)
        ax.set_xlim(0, MF_period)
        plt.xticks(np.arange(0, MF_period+1, 10.0))
        plt.yticks([])
        ax.grid(True)
        fig.set_size_inches(20, 1 * 5, forward=True)
        plt.savefig(filename.split(".")[0] + ".png")

    def create_nvp_vis(self, PICTURE_FILENAME_INITIAL_APP="tmp1.png", PICTURE_FILENAME_NVP="tmp2.png", TASK_CRASHED_ID=-1):
        img = Image.new('RGB', (256*10, 256*4))
        img1 = Image.open(PICTURE_FILENAME_INITIAL_APP)
        img2 = Image.open(PICTURE_FILENAME_NVP)
        img.paste(img1, (0,0))
        img.paste(img2, (0,256*3))
        print("dir: ", dir(img))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="./open-sans/OpenSans-ExtraBold.ttf", size=40)
        #draw.text((x, y),"Sample Text",(r,g,b))
        #draw.text((10, 10),"Crashed task: " + str(task_crasshed_id) + "; Part of crashed task: " + str(CRASHED_PART_OF_TASK),(0,0,0), font=font )
        with open("num_test_nvp_2.pkl", "rb") as file:
            next_test = pickle.load(file)
            try: 
                os.mkdir("./tests_nvp_2/test{}".format(next_test))
            except:
                pass
            img.show()
            img.save("./tests_nvp_2/test{}/RESULT.png".format(next_test))
            next_test += 1
        # with open("num_test.pkl", "wb") as file:
        #     pickle.dump(next_test, file)

    def visualise_nvp_2_no_fault(self, dict_inter, windws, filename = "graph.out", MF_period = 240, NUM_WINDOW_CRASHED=-1, FIXATOR_TIME=0, MAP__NAMES_IN_FILE__ID__ERR = {}):
        """Visualisation using matplotlib."""
        begins = []
        ends = []
        fig, ax = plt.subplots()
        j = 0
        y_offset = [0.03*j for j in range(8)]


        # find biggest window time period 
        MAX_WIN_TIME = 0
        for i in range(len(windws) - 1):
            if (wind_diff := (windws[i + 1] - windws[i])) > MAX_WIN_TIME:
                MAX_WIN_TIME = wind_diff

        MAX_WIN_TIME += 2 * FIXATOR_TIME

        for i in dict_inter: 
            begins =list(map(int, dict_inter[i][::2]))
            ends =list(map(int, dict_inter[i][1::2]))
            df = pd.DataFrame({"begin": begins, "end" : ends})
            colour = self.colours[j%len(self.colours)]

            for lft, rgt in list(zip(df["begin"].values, 
                            (df["end"] - df["begin"]).values)):
                ax.broken_barh([(lft, rgt)], 
                            (0, 0.5), facecolors=(colour))

            # ax.broken_barh(list(zip(df["begin"].values, 
            #                 (df["end"] - df["begin"]).values)), 
            #                 (0, 0.5), facecolors=(colour))
            j+=1

            # if "_ERR" in i:
            #     stp_lst = [0 + (j * 0.5)/20 for j in range(20)]
            #     for step in stp_lst:
            #         l_p = step
            #         r_p = step + 0.00625
            #         ax.broken_barh(list(zip(df["begin"].values, 
            #                 (df["end"] - df["begin"]).values)), 
            #                 (l_p, 0.0125), facecolors=(['black']))

            count_index = 0
            for p in begins:
                if MAP__NAMES_IN_FILE__ID__ERR and "Fixator" not in i:
                    ax.annotate(str(MAP__NAMES_IN_FILE__ID__ERR[i[5:]]), (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/(MF_period * 1.3), 0.7 + y_offset[j%len(y_offset)]), 
                            textcoords='axes fraction', fontsize=16, 
                            arrowprops=dict(shrink=0.0001))
                else:
                    if "Reserve" not in i:
                        ax.annotate(i, (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/(MF_period * 1.3), 0.8 + y_offset[j%len(y_offset)]), 
                                textcoords='axes fraction', fontsize=16,
                                arrowprops=dict(shrink=0.0001))
                count_index += 1

        #windws = list(map(int, list(np.arange(0, 240, 20))))
        begins = []
        ends = []

        for i in windws:
            begins.append(i)
            ends.append(i+0.5)


        # window line separators  
        df = pd.DataFrame({"begin": begins, "end" : ends})
        ax.broken_barh(list(zip(df["begin"].values, 
                        (df["end"] - df["begin"]).values)), 
                        (0, 1), facecolors='black')

    
        ax.broken_barh(list(zip(
                        list(map(lambda x: x + MAX_WIN_TIME, df["begin"].values)), 
                        list(map(lambda x: x + 0, (df["end"] - df["begin"]).values))
                        )), 
                        (1, 2), facecolors='black')
        
        ax.set_ylim(0, 2)
        ax.set_xlim(0, MF_period + MAX_WIN_TIME)
        ax.set_yticks([1, 2], labels=['core1', 'core2']) 
        plt.xticks(np.arange(0, MF_period+1 + MAX_WIN_TIME, 10.0))
        # plt.yticks([])
        ax.grid(True)
        fig.set_size_inches(20, 1 * 5, forward=True)



        plt.savefig("tmp1.png")

        return "tmp1"


    def visualise_nvp_2(self, dict_inter, windws, filename = "graph.out", MF_period = 240, NUM_WINDOW_CRASHED=-1, FIXATOR_TIME=0, MAP__NAMES_IN_FILE__ID__ERR = {}, info_task_err_right_prt = None):
        """Visualisation using matplotlib."""
        begins = []
        ends = []
        fig, ax = plt.subplots()
        j = 0
        y_offset = [0.03*j for j in range(8)]


        # find biggest window time period 
        MAX_WIN_TIME = 0
        for i in range(len(windws) - 1):
            if (wind_diff := (windws[i + 1] - windws[i])) > MAX_WIN_TIME:
                MAX_WIN_TIME = wind_diff

        MAX_WIN_TIME += 2 * FIXATOR_TIME

        for i in dict_inter: 
            begins =list(map(int, dict_inter[i][::2]))
            ends =list(map(int, dict_inter[i][1::2]))
            df = pd.DataFrame({"begin": begins, "end" : ends})
            colour = self.colours[j%len(self.colours)]

            for lft, rgt in list(zip(df["begin"].values, 
                            (df["end"] - df["begin"]).values)):
                
                # this is broken window -- we need to dublicate it on the reserver window
                if (lft >= windws[NUM_WINDOW_CRASHED["window_number"]*2]) and (lft + rgt <= windws[NUM_WINDOW_CRASHED["window_number"]*2 + 1]):
                    if info_task_err_right_prt != None:
                        ax.broken_barh([(lft + MAX_WIN_TIME, info_task_err_right_prt["old_time"])], 
                                (1, 0.5), facecolors=(colour))
                        ax.broken_barh([(lft, info_task_err_right_prt["new_time"])], 
                                (0, 0.5), facecolors=(colour))
                    else:
                        ax.broken_barh([(lft + MAX_WIN_TIME, rgt)], 
                                (1, 0.5), facecolors=(colour))
                        ax.broken_barh([(lft, rgt)], 
                                (0, 0.5), facecolors=(colour))

                elif lft >= windws[NUM_WINDOW_CRASHED["window_number"]*2 + 1]:
                    ax.broken_barh([(lft + MAX_WIN_TIME, rgt)], 
                            (1, 0.5), facecolors=(colour))

                else: 
                    ax.broken_barh([(lft, rgt)], 
                            (0, 0.5), facecolors=(colour))

            # ax.broken_barh(list(zip(df["begin"].values, 
            #                 (df["end"] - df["begin"]).values)), 
            #                 (0, 0.5), facecolors=(colour))
            j+=1

            if "_ERR" in i:
                stp_lst = [0 + (j * 0.5)/20 for j in range(20)]
                for step in stp_lst:
                    l_p = step
                    r_p = step + 0.00625
                    ax.broken_barh(list(zip(df["begin"].values, 
                            (df["end"] - df["begin"]).values)), 
                            (l_p, 0.0125), facecolors=(['black']))

            count_index = 0
            for p in begins:
                if MAP__NAMES_IN_FILE__ID__ERR and "Fixator" not in i:
                    if "Reserve" not in i:
                        if p >= windws[NUM_WINDOW_CRASHED["window_number"]*2 + 1]:
                            ax.annotate(MAP__NAMES_IN_FILE__ID__ERR[i[5:]], (p + MAX_WIN_TIME + (ends[count_index] - begins[count_index])/2, 1.5), xytext=((p+2)/ (MF_period * 0.9), 0.9 + y_offset[j%len(y_offset)]), 
                                    textcoords='axes fraction', fontsize=16,
                                    arrowprops=dict(shrink=0.0001))
                        else:
                            ax.annotate(MAP__NAMES_IN_FILE__ID__ERR[i[5:]], (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/(MF_period * 1.3), 0.75 + y_offset[j%len(y_offset)]), 
                                    textcoords='axes fraction', fontsize=16,
                                    arrowprops=dict(shrink=0.0001))

                    # ax.annotate(str(MAP__NAMES_IN_FILE__ID__ERR[i[5:]]), (p, 0.5), xytext=((p+2)/MF_period, 0.7 + y_offset[j%len(y_offset)]), 
                    #         textcoords='axes fraction', fontsize=16, 
                    #         arrowprops=dict(shrink=0.0001))
                else:
                    if "Reserve" not in i:
                        if p >= windws[NUM_WINDOW_CRASHED["window_number"]*2 + 1]:
                            ax.annotate(i, (p + MAX_WIN_TIME + (ends[count_index] - begins[count_index])/2, 1.5), xytext=((p-5)/MF_period, 0.75 + y_offset[j%len(y_offset)]), 
                                    textcoords='axes fraction', fontsize=16,
                                    arrowprops=dict(shrink=0.0001))
                        else:
                            ax.annotate(i, (p + (ends[count_index] - begins[count_index])/2, 0.5), xytext=((p+2)/(MF_period * 1.3), 0.25 + y_offset[j%len(y_offset)]), 
                                    textcoords='axes fraction', fontsize=16,
                                    arrowprops=dict(shrink=0.0001))
            count_index += 1

        #windws = list(map(int, list(np.arange(0, 240, 20))))
        begins = []
        ends = []

        for i in windws:
            begins.append(i)
            ends.append(i+0.5)


        # window line separators  
        df = pd.DataFrame({"begin": begins, "end" : ends})
        ax.broken_barh(list(zip(df["begin"].values, 
                        (df["end"] - df["begin"]).values)), 
                        (0, 1), facecolors='black')

        ax.broken_barh(list(zip(
                        list(map(lambda x: x + MAX_WIN_TIME, df["begin"].values)), 
                        list(map(lambda x: x + 0, (df["end"] - df["begin"]).values))
                        )), 
                        (1, 2), facecolors='black')
        
        ax.set_ylim(0, 2)
        ax.set_xlim(0, MF_period + MAX_WIN_TIME)
        ax.set_yticks([1, 2], labels=['core1', 'core2']) 
        plt.xticks(np.arange(0, MF_period+1 + MAX_WIN_TIME, 10.0))
        # plt.yticks([])
        ax.grid(True)
        fig.set_size_inches(20, 1 * 5, forward=True)

        plt.savefig("tmp2.png")

        return "tmp2"

        #self.create_nvp_vis(PICTURE_FILENAME_INITIAL_APP="tmp1.png", PICTURE_FILENAME_NVP="tmp2.png", TASK_CRASHED_ID=-1)


