from unittest import TestCase
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
import numpy as np

from ml.classifier.classifier import MultiModelClassifier

class TestMultiModelClassifier(TestCase):

    X = np.array([-5, -3, -1, 1, 3, 5]).reshape(-1,1)
    y = np.array([0, 0, 0, 1, 1, 1])

    X_test = np.array([-4, -2, 2, 4]).reshape(-1,1)
    y_test = np.array([0, 0, 1, 1])

    def test_init(self):
        #Test initialization for each model
        svm = MultiModelClassifier('svm')
        mlp = MultiModelClassifier('mlp')
        gnb = MultiModelClassifier('gaussian_nb')
        mnb = MultiModelClassifier('multinomial_nb')
        bnb = MultiModelClassifier('bernoulli_nb')

        self.assertIsInstance(svm.get_model(), SVC)
        self.assertIsInstance(mlp.get_model(), MLPClassifier)
        self.assertIsInstance(gnb.get_model(), GaussianNB)
        self.assertIsInstance(mnb.get_model(), MultinomialNB)
        self.assertIsInstance(bnb.get_model(), BernoulliNB)
    
    def test_params(self):
        #Test model parameters
        mmc = MultiModelClassifier('svm', C=1.0, kernel='linear', tol=0.1)
        
        params = mmc.get_params()
        self.assertEqual(params['C'], 1.0)
        self.assertEqual(params['kernel'], 'linear')
        self.assertEqual(params['tol'], 0.1)

        params['tol'] = 0.05

        mmc.set_params(**params)

        self.assertEqual(mmc.get_params()['tol'], 0.05)
    
    def test_svm(self):
        mmc_svm = MultiModelClassifier('svm', X=self.X, y=self.y)

        #Test predictions in training set
        self.assertEqual(mmc_svm.get_model().predict(5), 1)
        self.assertEqual(mmc_svm.get_model().predict(-5), 0)


    def test_scores_compare(self):
        #Test comparison functions
        print("Comparing svm and gnb")
        
        mmc_svm = MultiModelClassifier('svm', X=self.X, y=self.y)
        mmc_gnb = MultiModelClassifier('gaussian_nb', X=self.X, y=self.y)

        score_svm = mmc_svm.score(self.X_test, self.y_test)
        score_gnb = mmc_gnb.score(self.X_test, self.y_test)

        print("Average accuracy:")

        print('svm: ' + str(score_svm), end=' ')
        print('gnb: ' + str(score_gnb))
        
        comparison = mmc_svm.compare(mmc_gnb, self.X_test, self.y_test)

        print("Multiple metrics\nmetric | svm | gnb")

        for metric, (svm, gnb) in comparison.items():
            print(metric + ' ' + str(svm) + ' ' + str(gnb))
        
        
