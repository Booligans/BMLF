import numbers
import numpy as np
from scipy.stats import mode
from data_analysis.mean_variance_analysis import MeanVarianceAnalysis

class MeanVarianceAnalyzer:
    """Class encapsulating mean-variance analysis over a dataset."""

    def __init__(self, data):
        """Initializes the class with the given data.
        
        :param data: data from dataset.
        """
        self.data=data
    
    def create_list(self,column):
        """Creates a list from the indicated column.
        
        :param column: Column from which to create the list.
        """
        list=[]
        for i in (0, len(self.data)):
            list.append(self.data[i][column])
        return list

    def analyze(self):
        """Computes means, variances, maximums, minimums and modes; and 
        returns the corresponding analysis."""
        mean_list=[]
        variance_list=[]
        mode_list=[]
        max_list=[]
        min_list=[]
        #We suppose data is non-empty
        for i in range(0, len(data[0])):
            list=create_list(i)
            if isinstance(type(data[0][i]), numbers.Real) :
                mean_list.append(np.mean(list))
                variance_list.append(np.var(list))
            else:
                mean_list.append('-')
                variance_list.append('-')
                mode_list.append(mode(list))
                
            max_list.append(max(list))
            min_list.append(min(list))
            
        return MeanVarianceAnalysis(max_list, min_list, mean_list, variance_list)