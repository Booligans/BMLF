from statsmodels.multivariate.manova import MANOVA
from data_analysis.manova_analysis import MANOVAAnalysis

class MANOVAAnalyzer:
"""Multivariate ANOVA analyzer class"""
    
    def __init__(self, independent_variables, dependent_variables):
        self.model = MANOVA(dependent_variables, independent_variables)
        self.model.fit()
    
    def analyze(self):
        #self.model.mv_test() is of type MultivariateTestResults
        return MANOVAAnalysis(self.model.mv_test()) 