
class RegressionAnalysis:
    """Class encapsulating regression analysis over certain data"""
    
    
    def __init__(self, model):
        super().__init__(model)
        self.params = [model.coef_, model.intercept_]
    
    def draw(self):
        """Draw regression analysis info."""
        pass