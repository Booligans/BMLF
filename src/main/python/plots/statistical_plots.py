from matplotlib import pyplot as plt
import plot

class Histogram(Plot):
    """Class encapsulating a Histogram."""
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot(self):
        hist(self.data)

class BoxPlot(Plot):
    """Class encapsulating a Box/Box and Whiskers plot."""
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot():
        pass

class ScatterPlot(Plot):
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot():
        pass


class LogPlot(Plot):
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot():
        pass
        

class Histogram2D(Plot):
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        super().__init__(name,data,type,x_label,y_label)
    
    def plot():
        pass
        