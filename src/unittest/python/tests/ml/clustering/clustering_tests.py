from unittest import TestCase
from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, AgglomerativeClustering, DBSCAN, Birch
import numpy as np

#from ml.clustering.clustering import ClusteringModel

class TestClustering(TestCase):
    
    X = np.array([[1,0], [0,0], [-1,0], [10, 10], [10,11], [9,11]]).reshape(-1,2)
    
    #Pending clustering module polishing
    #On pause while errors are corrected
    """def test_init(self):
        self.assertIsInstance(ClusteringModel(type='kmeans').model_, KMeans)
        self.assertIsInstance(ClusteringModel(type='affinity').model_, AffinityPropagation)
        self.assertIsInstance(ClusteringModel(type='mean_shift').model_, MeanShift)
        #Spectral? When support is added
        self.assertIsInstance(ClusteringModel(type='agglomerative').model_, AgglomerativeClustering)
        self.assertIsInstance(ClusteringModel(type='dbscan').model_, DBSCAN)
        self.asserIsInstance(ClusteringModel(type='birch').model_, Birch)
    
    def test_clustering(self):
        pass #Needs defining general purpose test with self.X
        
    #Pending cross-validation testing"""