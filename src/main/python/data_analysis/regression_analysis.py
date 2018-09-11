from .ml_analysis import MLAnalysis

class RegressionAnalysis(MLAnalysis):
    """Class encapsulating regression analysis over certain data"""
    
    
    def __init__(self, model, data):
        """Initializes the class with the model and data.
        
        :param model: Regression model used.
        :param data: Testing data.
        """
        super().__init__(model, data)
    
    def analyze(self):
        """Analyzes results and indicatews the regression line."""
        super().analyze()
        self.params = [model.coef_, model.intercept_]
        