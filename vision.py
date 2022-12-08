"""This is visualizer of NVP with one kernel mechanism. You must run the parser cell before running this cell. 
Visualizer works with no more than 240 seconds programm."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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


