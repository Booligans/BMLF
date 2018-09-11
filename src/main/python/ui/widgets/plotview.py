from PyQt5 import QtCore, QtWidgets
from plots.plot import MultiPlot

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class PlotView(QtWidgets.QScrollArea):

    PLOT_WIDTH = 1
    PLOT_HEIGHT = 1
    
    
    def __init__(self, *args, parent = None, res=None, **kwargs):
        super().__init__(*args, **kwargs)
        if parent is not None:
            self.setParent(parent)
        if res is not None:
            self.screenSize = (res.width(), res.height())
        else:
            self.screenSize = (1920, 1080)
        self.dpi = self.screenSize[0]/16
        self.canvas = FigureCanvas(Figure(figsize=(16, 16), dpi=self.dpi, constrained_layout=True))
        self.multiplot = MultiPlot('Multiplot')
        self.axes = []
        self.plot_size = 4
        self.setWidget(self.canvas)
        
    def plot_changed(self):

        while len(self.multiplot) > self.plot_size-2:
            self.plot_size = 2*self.plot_size

        self.canvas = FigureCanvas(Figure(figsize=(18, max(16,8*self.plot_size)), dpi=self.dpi, constrained_layout=True))
        for i,plot in enumerate(self.multiplot.plots):
            plot.plot(self.canvas.figure.add_subplot(self.plot_size,2,i+1))

        self.setWidget(self.canvas)
        self.canvas.draw()

        
            
