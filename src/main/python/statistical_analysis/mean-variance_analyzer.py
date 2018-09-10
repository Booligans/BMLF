import numpy as np
import numbers
from data_analysis.mean_variance_analysis import MeanVarianceAnalysis

class MeanVarianceAnalyzer:
    """Class encapsulating mean-variance analysis over a dataset."""

    def __init__(self, data):
        self.data=data
    
    def create_list(self,column):
        list=[]
        for i in (0, len(self.data)):
            list.append(self.data[i][column])
        return list
        
    def mode(list):
        return max(set(list), key=list.count)

    def analyze(self):
        super().analyze()
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