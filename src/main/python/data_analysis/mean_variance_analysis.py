from .data_analysis import DataAnalysis

def MeanVarianceAnalysis(DataAnalysis):
    
    def __init__():
        pass
    
    def analyze(self, features, max_list, min_list, mean_list, variance_list):
        #Needs proper formatting
        self.text.append('Feature' + ' ' + 'Max' + ' ' + 'Min' + ' ' + 'Mean' + ' ' + 'Variance')
        for i in range(0, len(features)):
            text = features[i] + ' '
            text += str(max_list[i]) + ' '
            text += str(min_list[i]) + ' '
            text += str(mean_list[i]) + ' '
            text += str(variance_list[i])
            self.text.append(text)