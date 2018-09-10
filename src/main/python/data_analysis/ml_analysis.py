from data_analysis import DataAnalysis

class MLAnalysis(DataAnalysis):
    """This class encapsulates the analysis of the model for some test data."""
    
    def __init__(self, model, test_data):
        """Class constructor.
        
        :param model: predictive model.
        :type model: MlModel
        """
        super.__init__(test_data)
        self.model = model
        self.to_predict = test_data
        self.predictions = self.model.predict(test_data)
        self.analyze()
    
    def analyze(self):
        """Indicates the model used. """
        #Model
        self.text.append('Model: ', self.model)
        