from matplotlib import pyplot as plt
import numpy as np
from .plot import Plot

class BarPlot(Plot):
    """Class encapsulating a BarPlot."""
    
    def __init__(self, name, data, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,type,x_label,y_label, *args, **kwargs)

    def plot(self, axes):
        axes.set_title(self.name)
        axes.set_xlabel(self.x_label)
        axes.set_ylabel(self.y_label)
        axes.bar(np.arange(len(self.data)), self.data, *self.args, **self.kwargs)

class PieChart(Plot):
    """Class encapsulating a PieChart."""
    def __init__(self, name, data, type, *args, **kwargs):
        super().__init__(name,data,type, *args, **kwargs)
                
    def plot(self, axes):
        axes.set_title(self.name)
        axes.pie(self.data, *self.args, **self.kwargs)

class LinePlot(Plot):
    """Class encapsulating a LinePlot."""
    def __init__(self, name, data, type, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,type,x_label,y_label, *args, **kwargs)

    def plot(self, axes):
        axes.set_title(self.name)
        axes.plot(self.data[0], self.data[1], *self.args, **self.kwargs)
