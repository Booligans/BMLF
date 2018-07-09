from matplotlib import pyplot as plt
import numpy as np
import plot
#Obs: matplotlib interactive mode should be on for plotting via plt.ion()

class BarPlot(Plot):
    """Class encapsulating a BarPlot."""
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot(self):
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.bar(np.arange(len(data), data)


class PieChart(Plot):
    """Class encapsulating a PieChart."""
    def __init__(self, name, data, type):
        super().__init__(name,data,type)
    
    def plot(self):
        plt.pie(self.data)


class LinePlot(Plot):
    """Class encapsulating a LinePlot."""
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot(self):
        plt.plot(self.data[0], self.data[1])