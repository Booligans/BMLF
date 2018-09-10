from .ml_analysis import MLAnalysis

class RegressionAnalysis(MLAnalysis):
    """Class encapsulating regression analysis over certain data"""
    
    
    def __init__(self, model, data):
        """Initializes the class with the model and data"""
        super().__init__(model, data)
    
    def analyze(self):
        """"""
        super().analyze()
        self.params = [model.coef_, model.intercept_]
        