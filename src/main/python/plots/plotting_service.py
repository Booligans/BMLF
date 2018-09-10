from .statistical_plots import *
from .basic_plots import *

class PlottingService:
    """Class that acts as a Plot factory in the BMLF framework."""
    
    def __init__(self):
        """Class constructor"""
        pass
        
    def build_plot(project, type_, *args, **kwargs):
        """Builds a plot of the indicated type_ from the given data.
        
        :param project: current project
        :type project: Project
        :param type_: type_ of plot
        :type type_: str
        :param *args: Variable length argument list
        :param **kwargs: Arbitrary keyword arguments
        """
                         
        if type_=='Bar':
            ret = BarPlot(*args,**kwargs)
        elif type_=='Pie':
            ret = PieChart(*args,**kwargs)
        elif type_=='Line':
            ret = LinePlot(*args,**kwargs)
        elif type_=='Hist':
            ret = ScatterPlot(*args,**kwargs)
        elif type_=='Box':
            ret = BoxPlot(*args,**kwargs)
        elif type_=='Scatter':
            ret = ScatterPlot(*args,**kwargs)
        elif type_=='Hist2D':
            ret = Histogram2D(*args,**kwargs)
        else:
            raise ValueError('There is no plot type_ ', type_, '.')
            
        return ret
