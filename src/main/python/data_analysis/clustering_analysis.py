from .ml_analysis import MLAnalysis

class ClusteringAnalysis(MLAnalysis):
    """Class encapsulating clustering analysis over a dataset."""
    
    def __init__(self,model, data):
        super().__init__(model, data)
    
    def analyze(self):
        super().analyze()
        #needs clustering module to be defined