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
        self.dpi = self.screenSize[0]*269/(10*320)
        self.tight_layout = {'pad':0, 'h_pad':0.5, 'w_pad':0.5, 'rect':(0,0,1,1)}
        self.canvas = FigureCanvas(Figure(figsize=(10, 10), dpi=self.dpi, tight_layout=self.tight_layout))
        self.multiplot = MultiPlot('Multiplot')
        self.axes = []
        self.plot_size = 4
        self.setWidget(self.canvas)
        
    def plot_changed(self):

        while len(self.multiplot) > self.plot_size-2:
            self.plot_size = 2*self.plot_size

        self.canvas = FigureCanvas(Figure(figsize=(10, max(10,5*self.plot_size)), dpi=self.dpi, tight_layout = self.tight_layout))
        for i,plot in enumerate(self.multiplot.plots):
            plot.plot(self.canvas.figure.add_subplot(self.plot_size,2,i+1))

        self.setWidget(self.canvas)
        self.canvas.draw()

        
            
