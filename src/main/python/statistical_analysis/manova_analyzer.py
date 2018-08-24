from statsmodels.multivariate.manova import MANOVA

class MANOVAAnalyzer:
"""Multivariate ANOVA analyzer class"""
    
    def __init__(self, independent_variables, dependent_variables):
        self.model = MANOVA(dependent_variables, independent_variables)
        self.model.fit()
    
    def analyze(self):
        results = self.model.mv_test() #Of type MultivariateTestResults