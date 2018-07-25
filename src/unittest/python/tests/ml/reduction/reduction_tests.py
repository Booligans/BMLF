from unittest import TestCase
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA
import numpy as np
from numpy.ma.testutils import assert_equal

from ml.reduction.pca_reductor import PCAReductor

class TestPCAReductor(TestCase):
    
    X = np.array([[0,-5], [0,6], [0,-1], [1,1], [1,3], [1,5]]).reshape(-1,2)
    X_test = np.array([[0,-4], [0,2], [1,2], [1,4]]).reshape(-1,2)
    
    def test_init(self):
        self.assertIsInstance(PCAReductor().model, PCA)
        self.assertIsInstance(PCAReductor(type='incremental').model, IncrementalPCA)
        self.assertIsInstance(PCAReductor(type='kernel').model, KernelPCA)
        
    def test_reduction(self):
        print("... PCA TESTING ...")
        reductor = PCAReductor(n_components=1)
        control = PCA(n_components=1)
        assert_equal(reductor.fit_transform(self.X), control.fit_transform(self.X))
        #print(self.X_test)
        #print("TEST TRANSFORM:", reductor.transform(self.X_test))
        #print(self.X_test)
        #print("TEST CONTROL:", control.transform(self.X_test))
        
        assert_equal(reductor.transform(self.X_test), control.transform(self.X_test))