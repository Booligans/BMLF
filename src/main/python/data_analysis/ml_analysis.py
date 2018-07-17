import data_analysis

class MLAnalysis(DataAnalysis):

    def __init__(self, model, data):
        """Class constructor.
        
        :param model: predictive model.
        :type model: MlModel
        """
        self.model = model
        self.to_predict = data
        self.predictions = self.model.predict(data)
        #is score assignment uniform across models?
        self.analyze()
    
    def analyze():
        self.text = []
        #self.append('Number of items: ', len(data)) #rows of data matrix
        #self.append('Number of features: ', len(data[0])) #columns of data matrix 
        #accuracy, f1, precision, confusion matrix and other metrics report here