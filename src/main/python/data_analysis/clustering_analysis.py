import data_analysis

class ClusteringAnalysis(DataAnalysis):
    """Class encapsulating clustering analysis over a dataset."""
    
    def __init__(self,model):
        super().__init__(model)
    
    def draw(self):
        """Draws clustering analysis info."""