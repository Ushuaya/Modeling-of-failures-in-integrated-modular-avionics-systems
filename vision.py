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

    def visualise(self, dict_inter, windws, filename = "graph.out", MF_period = 240):
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

            
            for p in begins:
                ax.annotate(i, (p, 0.5), xytext=((p+2)/MF_period, 0.7 + y_offset[j%len(y_offset)]), 
                            textcoords='axes fraction', 
                            arrowprops=dict(shrink=0.0001))

        #windws = list(map(int, list(np.arange(0, 240, 20))))
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

    def visualise_nvp_2(self, dict_inter, windws, filename = "graph.out", MF_period = 240):
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

            
            for p in begins:
                ax.annotate(i, (p, 0.5), xytext=((p+2)/MF_period, 0.25 + y_offset[j%len(y_offset)]), 
                            textcoords='axes fraction', 
                            arrowprops=dict(shrink=0.0001))

        #windws = list(map(int, list(np.arange(0, 240, 20))))
        begins = []
        ends = []

        for i in windws:
            begins.append(i)
            ends.append(i+0.5)

        

            
        df = pd.DataFrame({"begin": begins, "end" : ends})
        ax.broken_barh(list(zip(df["begin"].values, 
                        (df["end"] - df["begin"]).values)), 
                        (0, 1), facecolors='black')
        ax.set_ylim(0, 2)
        ax.set_xlim(0, MF_period)
        ax.set_yticks([1, 2], labels=['core1', 'core2']) 
        plt.xticks(np.arange(0, MF_period+1, 10.0))
        # plt.yticks([])
        ax.grid(True)
        #fig.set_size_inches(20, 1 * 5, forward=True)

   
        plt.savefig("tmp1.png")
        plt.clf()
        plt.cla()

        df = pd.DataFrame({"begin": [], "end" : []})
        ax.broken_barh(list(zip(df["begin"].values, 
                        (df["end"] - df["begin"]).values)), 
                        (0, 1), facecolors='black')
        ax.set_ylim(0, 1)
        ax.set_xlim(0, MF_period)
        plt.xticks(np.arange(0, MF_period+1, 10.0))
        plt.yticks([])
        ax.grid(True)

        plt.savefig("tmp2.png")

        self.create_nvp_vis(PICTURE_FILENAME_INITIAL_APP="tmp1.png", PICTURE_FILENAME_NVP="tmp2.png", TASK_CRASHED_ID=-1)


