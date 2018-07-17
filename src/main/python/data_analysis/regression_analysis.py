import ml_analysis

class RegressionAnalysis(MLAnalysis):
    """Class encapsulating regression analysis over certain data"""
    
    
    def __init__(self, model, data):
        super().__init__(model, data)
    
    def analyze():
        super().analyze()
        self.params = [model.coef_, model.intercept_]
        