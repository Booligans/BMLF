from unittest import TestCase
from sklearn import linear_model
import numpy as np

from ml.regression.regression import LinearModel

class TestLinearModel(TestCase):

    X = np.array([-5, -3, -1, 1, 3, 5]).reshape(-1,1)
    y = np.array([1, 2, 3, 4, 5, 6])

    X_test = np.array([-4, -2, 2, 4]).reshape(-1,1)
    y_test = np.array([1.5, 2.5, 4.5, 5.5])

    def test_init(self):
        #Test initialization for each model
        linear = LinearModel('linear')
        eln = LinearModel('elasticnet')                          
        elncv = LinearModel('elasticnetcv')
        bayes = LinearModel('bayes_ridge')                          
        orth = LinearModel('orthogonal')                          
        orthcv = LinearModel('orthogonalcv')                         
        theil = LinearModel('theil')                          
        sgd = LinearModel('sgd')
        pct = LinearModel('perceptron')
        p_a = LinearModel('passive-agressive')

        self.assertIsInstance(linear.get_model(), linear_model.LinearRegression)
        self.assertIsInstance(eln.get_model(), linear_model.ElasticNet)
        self.assertIsInstance(elncv.get_model(), linear_model.ElasticNetCV)
        self.assertIsInstance(bayes.get_model(), linear_model.BayesianRidge)
        self.assertIsInstance(orth.get_model(), linear_model.OrthogonalMatchingPursuit)
        self.assertIsInstance(orthcv.get_model(), linear_model.OrthogonalMatchingPursuitCV)
        self.assertIsInstance(theil.get_model(), linear_model.TheilSenRegressor)
        self.assertIsInstance(sgd.get_model(), linear_model.SGDRegressor)
        self.assertIsInstance(pct.get_model(), linear_model.Perceptron)
        self.assertIsInstance(p_a.get_model(), linear_model.PassiveAggressiveRegressor)
        
    
    def test_params(self):
        linear = LinearModel('linear', n_jobs=1, normalize=False)
        
        params = linear.get_params()
        self.assertEqual(params['n_jobs'], 1)
        self.assertEqual(params['normalize'], False)
        
        params['n_jobs'] = 5

        linear.set_params(**params)

        self.assertEqual(linear.get_params()['n_jobs'], 5)
    
    def test_linear(self):
        linear = LinearModel('linear', X=self.X, y=self.y)

        #Test predictions in training set
        self.assertEqual(linear.get_model().predict(5), 6)
        self.assertEqual(linear.get_model().predict(-5), 1)


    def test_scores_compare(self):
        print("Comparing linear and elastic net")
        
        linear = LinearModel('linear', X=self.X, y=self.y)
        eln = LinearModel('elasticnet', X=self.X, y=self.y)

        score_linear = linear.score(self.X_test, self.y_test)
        score_eln = eln.score(self.X_test, self.y_test)

        print("Average accuracy:")

        print('linear: ' + str(score_linear), end=' ')
        print('eln: ' + str(score_eln))
        
        comparison = linear.compare(eln, self.X_test, self.y_test)

        print("Multiple metrics\nmetric | linear | eln")

        for metric, (linear, eln) in comparison.items():
            print(metric + ' ' + str(linear) + ' ' + str(eln))
        
