from matplotlib import pyplot as plt
from .plot import Plot

class Histogram(Plot):
    """Class encapsulating a Histogram."""
    
    def __init__(self, name, data, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,x_label,y_label, *args, **kwargs)
    
    def plot(self, axes):
        axes.hist(self.data, *self.args, **self.kwargs)

class BoxPlot(Plot):
    """Class encapsulating a Box/Box and Whiskers plot."""
    
    def __init__(self, name, data, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,x_label,y_label, *args, **kwargs)
    
    def plot(self, axes):
        axes.boxplot(self.data, *self.args, **self.kwargs)

class ScatterPlot(Plot):
    """Class ecnapsulating a Scatter plot."""
    
    def __init__(self, name, data, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,x_label,y_label)
    
    def plot(self, axes):
        axes.scatter(self.data[0], self.data[1], *self.args, **self.kwargs)

class Histogram2D(Plot):
    """Class encapsulating a heatmap representing a 2D histogram."""
    
    def __init__(self, name, data, x_label=None, y_label=None, *args, **kwargs):
        super().__init__(name,data,x_label,y_label, *args, **kwargs)
    
    def plot(self, axes):
        axes.hist2d(self.data[0],self.data[1], *self.args, **self.kwargs)
        
