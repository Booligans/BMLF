from unittest import TestCase
import numpy as np

from ml.classifier.classifier import MultiModelClassifier

class TestMultiModelClassifier(TestCase):

    X = np.array([-5, -3, -1, 1, 3, 5]).reshape(-1,1)
    y = np.array([0, 0, 0, 1, 1, 1])
    
    def test_svm(self):
        mmc_svm = MultiModelClassifier('svm', X=self.X, y=self.y)

        #Test predictions
        self.assertEqual(mmc_svm.get_model().predict(5), 1)
        self.assertEqual(mmc_svm.get_model().predict(-5), 0)
        print(mmc_svm.scores_)
