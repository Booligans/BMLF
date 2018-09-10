from .ml_analysis import MLAnalysis
import numpy as np

class ClusteringAnalysis(MLAnalysis):
    """Class encapsulating clustering analysis over a dataset."""
    
    def __init__(self,model, data):
        super().__init__(model, data)
        self.n_clusters = self.model.model_.n_clusters
    
    def analyze(self):
        super().analyze()
        #needs clustering module to be defined
        self.text.append("Number of clusters, ", self.n_clusters)
        self.text.append("Cluster centers")
        #Loop through
        i = 1
        for center in self.model.model_.cluster_centers_:
            self.text.append("Cluster " + str(i) + ": " + str(center))
            i += 1
        self.text.append("Cluster data")
        #Create and loop through dict
        clusters = {i : np.where(self.model.model_.labels_ == i) for i in range(self.n_clusters)}
        for k,v in clusters:
            self.text.append("Cluster " + str(k) + ": " + str(clusters))