from .data_analysis import DataAnalysis

def MeanVarianceAnalysis(DataAnalysis):
    
    #__init__() doesn't need to do anything
    
    def analyze(self, features, max_list, min_list, mean_list, variance_list):
        """Initializes the analysis text indicating maximum values, minimum
        values and means and variances.
        """
        #Needs proper formatting
        self.text.append('Feature' + ' ' + 'Max' + ' ' + 'Min' + ' ' + 'Mean' + ' ' + 'Variance')
        for i in range(0, len(features)):
            text = features[i] + ' '
            text += str(max_list[i]) + ' '
            text += str(min_list[i]) + ' '
            text += str(mean_list[i]) + ' '
            text += str(variance_list[i])
            self.text.append(text)