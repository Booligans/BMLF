import numpy as np

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
        """ It is supposed that there is any user to check data[0]. """
        for i in range(0, len(data[0])):
            list=create_list(i)
            if type(data[0][i]) is float:
                mean_list.append(np.mean(list))
                variance_list.append(np.var(list))
            else:
                mode_list.append(mode(list))
                
            max_list.append(max(list))
            min_list.append(min(list))
            
        #Following text corresponds to an analysis
        #self.text.append('Mean of quantitative characteristics:',mean_list)
        #self.text.append('Variance of quantitative characteristics:',variance_list)
        #self.text.append('Mode of qualitative characteristics',mode_list)
        #self.text.append('Maximun of characteristics',max_list)
        #self.text.append('Minimun of characteristics',min_list)