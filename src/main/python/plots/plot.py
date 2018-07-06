class Plot:
    
    def __init__(self, name, data, type, x_label=None, y_label=None):
        self.name = name
        self.data = data
        self.type = type
        self.x_label = x_label
        self.y_label = y_label
        
    #defined in subclass?
    def plot():
        pass
        

class MultiPlot:
    
    def __init__(self, name):
        self.plots = []
        
    def add_plot(self,plot):
        self.plots.append(plot)
        
    def remove_plot(self,index):
        self.plots.pop(index)