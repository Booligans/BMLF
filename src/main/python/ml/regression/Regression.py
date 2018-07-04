
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from copy import copy, deepcopy

"""
    Linear Regression
    Logistic Regression
    Polynomial Regression

    x Ridge Regression
    x Lasso Regression
    ->ElasticNet Regression

    x Jacknife Regression

    Implementing Polynomial regression as Linear regression: https://stats.stackexchange.com/questions/58739/polynomial-regression-using-scikit-learn
"""

class LinearModel:
    self.model_ = None

    def __init__(self, type = 'auto', params = {}):
        """ Initiates the Regression class.
        The type sets defines which model will be chosen, the default will be an automated crossvalidation over all supported linear models.
        """
        self._type = type
        self.model_ = None
        
        if type == 'linear' or type == 'polynomial':
            model_ = linear_model.LinearRegression(params['fit_intercept'],params['normalize'],params['copy_x'],params['n_jobs']) 
        elif type == 'logistic':
            model_ = linear_model.LogisticRegression(params['penalty'],params['dual'],params['tolerance'],params['c'],params['fit_intercept'],params['class_weight'],params['seed'],params['solver'],params['max_iterations'],params['multi_class'],params['verbose'],params['warm_start'],params['n_jobs'])
        elif type == 'logisticcv':
            model_ = linear_model.LogisticRegressionCV(params['cs'],params['fit_intercept'],params['cv'],params['dual'],params['penalty'],params['scoring'],params['solver'],params['tol'],params['max_iter'],params['class_weight'],params['n_jobs'],params['verbose'],params['refit'],params['intercept_scaling'],params['multi_class'],params['seed'])
        elif type == 'elasticnet':
            model_ = linear_model.ElasticNet(params['alpha'],params['l1_ratio'],params['fit_intercept'],params['normalize'],params['precompute'],params['max_iter'],params['copy_x'],params['tol'],params['warm_start'],params['positive'],params['seed'],params['selection']) 
        elif type == 'elasticnetcv':
            model_ = linear_model.ElasticNetCV(params['l1_ratio'],params['eps'],params['n_alphas'],params['alphas'],params['fit_intercept'],params['normalize'],params['precompute'],params['max_iter'],params['tol'],params['cv'],params['copy_c'],params['verbose'],params['n_jobs'],params['positive'],params['seed'],params['selection'])
        elif type == 'bayesian':
            model_ = linear_model.BayesianRidge(params['n_iter'],params['tol'],params['alpha_1'],params['alpha_2'],params['lambda_1'],params['lambda_2'],params['compute_score'],params['fit_intercept'],params['normalize'],params['copy_x'],params['verbose'])
        elif type == 'orthogonal':
            model_ = linear_model.OrthogonalMatchingPursuit(params['n_nonzero_coefs'],params['tol'],params['fit_intercept'],params['normalize'], params['precompute']) 
        elif type == 'orthogonalcv':
            model_ = linear_model.OrthogonalMatchingPursuitCV(params['copy'],params['fit_intercept'],params['true'],params['max_iter'],params['cv'],params['n_jobs'],params['verbose'])
        elif type == 'theil':
            model_ = linear_model.TheilSenRegressor(params['fit_intercept'],params['copy_x'],params['max_population'],params['n_subsamples'],params['max_iter'],params['tol'],params['seed'],params['n_jobs'],params['verbose'])
        elif type == 'sgd':
            model_ = linear_model.SGDRegressor(params['loss'],params['penalty'],params['alpha'],params['l1_ratio'],params['fit_intercept'],params['max_iter'],params['tol'],params['shuffle'],params['verbose'],params['epsilon'],params['seed'],params['learning_rate'],params['eta0'],params['power_t'],params['warm_start'],params['average'],params['n_iter'])
        elif type == 'perceptron':
            model_ = linear_model.Perceptron(params['penalty'],params['alpha'],params['fit_intercept'],params['max_iter'],params['tol'],params['shuffle'],params['verbose'],params['eta0'],params['n_jobs'],params['seed'],params['class_weight'],params['warm_start'],params['n_iter'])
        elif type == 'passive_aggressive':
            model_ = linear_model.PassiveAggressiveRegressor(params['c'],params['fit_intercept'],params['max_iter'],params['tol'],params['shuffle'],params['verbose'],params['loss'],params['epsilon'],params['seed'],params['warm_start'],params['average'],params['n_iter'])

    def fit_and_evaluate(X, y = None, test_size = 0.25, seed = 0):
        #https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        model_.fit(X_train,y_train)
        score = model.score(X_test, y_test)
        return score

    def get_params():
        self.model_.get_params()

    def score():
        self.model_.score(X)

    def set_parameters(parameters):
        return self.model_.set_paraeters(parameters)

    def choose_model(X,y = None):
        #Not implemented