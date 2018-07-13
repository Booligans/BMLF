import statistical_plots
import basic_plots

class PlottingService:
    """Class that acts as a Plot factory in the BMLF framework."""
    
    def __init__(self):
        """Class constructor"""
        pass
        
    def build_plot(project, type, *args, **kwargs):
        """Builds a plot of the indicated type from the given data.
        
        :param project: current project
        :type project: Project
        :param type: type of plot
        :type type: str
        :param *args: Variable length argument list
        :param **kwargs: Arbitrary keyword arguments
        """
                         
        if type=='Bar':
            ret = BarPlot(args,kwargs)
        elif type=='Pie':
            ret = PieChart(args,kwargs)
        elif type=='Line':
            ret = LinePlot(args,kwargs)
        elif type=='Hist':
            ret = ScatterPlot(args,kwargs)
        elif type=='Box':
            ret = BoxPlot(args,kwargs)
        elif type=='Scatter':
            ret = ScatterPlot(args,kwargs)
        elif type=='Hist2D':
            ret = Histogram2D(args,kwargs)
        else:
            raise ValueError('There is no plot type ', type, '.')
            
        return ret