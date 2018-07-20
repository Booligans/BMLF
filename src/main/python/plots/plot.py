from abc import ABC,abstractmethod

class Plot(ABC):
    """This class represents an abstract plot."""
    
    def __init__(self, name, data, type, x_label=None, y_label=None, *args, **kwargs):
        """Class constructor.
        
        :param name
        :type name: str
        :param data
        :type data: ndarray
        :param type
        :type type: str
        :param x_label
        :type x_label: str
        :param y_label
        :type y_label: str 
        """
        self.name = name
        self.data = data
        self.type = type
        self.x_label = x_label
        self.y_label = y_label
        self.args = args
        slef.kwargs = kwargs
        
    @abstractmethod
    def plot(self, axes):
        """Draws the plot."""
        pass
        

class MultiPlot:
    """This class represents a plot with multiple subplots."""
    
    def __init__(self, name, plots=[], *args, **kwargs):
        """Class constructor.
        
        :param name: name of the MultiPlot
        :param plots: array of plots to initialize
        :type name: str
        :type plots: array
        """
        self.name = name
        self.plots = plots
        self.args = args
        self.kwargs = kwargs
        
    def add_plot(self,plot):
        """Adds a plot to the current MultiPlot.
        
        :param plot: plot to add
        :type plot: Plot
        """
        self.plots.append(plot)
        
    def remove_plot(self,index):
        """Removes a plot from the current MultiPlot.
        
        :param index: index of the plot to remove
        :type index: int
        """
        self.plots.pop(index)
        
    def plot(self, axes):
        """Draws the MultiPlot."""
        pass #Requires format specification
