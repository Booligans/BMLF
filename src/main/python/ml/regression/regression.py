from sklearn import linear_model
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
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

class LinearModel(object):
    """This class encapsulates a linear model."""
    self.model_ = None

    def __init__(self, type = 'auto', ini_params = {}, X = None, y = None, avoid_overfitting = True):
        """ Initiates the Regression class.
        
        The type parameter defines which model will be chosen, the default will be an automated crossvalidation over all supported linear models.
        The params parameter is a dictinary that contains all the parameters required for the initialization of the lineal model using the format {'name' : value}, in which the names must match the names of the parameters in the sklearn library (in lower case).
        If the type is set to 'auto', it will be ingored.

        X and y are provided, the model will be directly trained using it.

        :param type: The type of the model. Supports {'linear', 'polynomial',logistic','logisticcv','elasticnet','elasticnetcv','orthogonal','orthogonalcv','theil','sgd','perceptron','passive_aggressive'}
        :param ini_params: The parameters of the model
        :param X: data
        :param y: target values
        :param avoid_overfitting: avoid overfitting
        :type type: str
        :type ini_params: dictionary
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type avoid_overfitting: boolean

        :Example:
        >>> model = LinearModel('linear', {'fit_intercept':True,'normalize':True,'copy_x':True,'n_jobs':1})
        """
        self._type = type
        self.model_ = None
        
        if type == 'linear' or type == 'polynomial':
            model_ = linear_model.LinearRegression(ini_params['fit_intercept'],
                                                    ini_params['normalize'],
                                                    ini_params['copy_x'],
                                                    ini_params['n_jobs']) 
        elif type == 'logistic':
            model_ = linear_model.LogisticRegression(ini_params['penalty'],
                                                     ini_params['dual'],
                                                     ini_params['tolerance'],
                                                     ini_params['c'],
                                                     ini_params['fit_intercept'],
                                                     ini_params['class_weight'],
                                                     ini_params['random_state'],
                                                     ini_params['solver'],
                                                     ini_params['max_iterations'],
                                                     ini_params['multi_class'],
                                                     ini_params['verbose'],
                                                     ini_params['warm_start'],
                                                     ini_params['n_jobs'])
        elif type == 'logisticcv':
            model_ = linear_model.LogisticRegressionCV(ini_params['cs'],
                                                       ini_params['fit_intercept'],
                                                       ini_params['cv'],ini_params['dual'],
                                                       ini_params['penalty'],ini_params['scoring'],
                                                       ini_params['solver'],ini_params['tol'],
                                                       ini_params['max_iter'],
                                                       ini_params['class_weight'],
                                                       ini_params['n_jobs'],
                                                       ini_params['verbose'],
                                                       ini_params['refit'],
                                                       ini_params['intercept_scaling'],
                                                       ini_params['multi_class'],
                                                       ini_params['random_state'])
        elif type == 'elasticnet':
            model_ = linear_model.ElasticNet(ini_params['alpha'],
                                             ini_params['l1_ratio'],
                                             ini_params['fit_intercept'],
                                             ini_params['normalize'],
                                             ini_params['precompute'],
                                             ini_params['max_iter'],
                                             ini_params['copy_x'],
                                             ini_params['tol'],
                                             ini_params['warm_start'],
                                             ini_params['positive'],
                                             ini_params['random_state'],
                                             ini_params['selection']) 
        elif type == 'elasticnetcv':
            model_ = linear_model.ElasticNetCV(ini_params['l1_ratio'],
                                               ini_params['eps'],
                                               ini_params['n_alphas'],
                                               ini_params['alphas'],
                                               ini_params['fit_intercept'],
                                               ini_params['normalize'],
                                               ini_params['precompute'],
                                               ini_params['max_iter'],
                                               ini_params['tol'],
                                               ini_params['cv'],
                                               ini_params['copy_c'],
                                               ini_params['verbose'],
                                               ini_params['n_jobs'],
                                               ini_params['positive'],
                                               ini_params['random_state'],
                                               ini_params['selection'])
        elif type == 'bayesian':
            model_ = linear_model.BayesianRidge(ini_params['n_iter'],
                                                ini_params['tol'],
                                                ini_params['alpha_1'],
                                                ini_params['alpha_2'],
                                                ini_params['lambda_1'],
                                                ini_params['lambda_2'],
                                                ini_params['compute_score'],
                                                ini_params['fit_intercept'],
                                                ini_params['normalize'],
                                                ini_params['copy_x'],
                                                ini_params['verbose'])
        elif type == 'orthogonal':
            model_ = linear_model.OrthogonalMatchingPursuit(ini_params['n_nonzero_coefs'],
                                                            ini_params['tol'],
                                                            ini_params['fit_intercept'],
                                                            ini_params['normalize'],
                                                            ini_params['precompute']) 
        elif type == 'orthogonalcv':
            model_ = linear_model.OrthogonalMatchingPursuitCV(ini_params['copy'],
                                                              ini_params['fit_intercept'],
                                                              ini_params['true'],
                                                              ini_params['max_iter'],
                                                              ini_params['cv'],
                                                              ini_params['n_jobs'],
                                                              ini_params['verbose'])
        elif type == 'theil':
            model_ = linear_model.TheilSenRegressor(ini_params['fit_intercept'],
                                                    ini_params['copy_x'],
                                                    ini_params['max_population'],
                                                    ini_params['n_subsamples'],
                                                    ini_params['max_iter'],
                                                    ini_params['tol'],
                                                    ini_params['random_state'],
                                                    ini_params['n_jobs'],
                                                    ini_params['verbose'])
        elif type == 'sgd':
            model_ = linear_model.SGDRegressor(ini_params['loss'],
                                               ini_params['penalty'],
                                               ini_params['alpha'],
                                               ini_params['l1_ratio'],
                                               ini_params['fit_intercept'],
                                               ini_params['max_iter'],
                                               ini_params['tol'],
                                               ini_params['shuffle'],
                                               ini_params['verbose'],
                                               ini_params['epsilon'],
                                               ini_params['random_state'],
                                               ini_params['learning_rate'],
                                               ini_params['eta0'],
                                               ini_params['power_t'],
                                               ini_params['warm_start'],
                                               ini_params['average'],
                                               ini_params['n_iter'])
        elif type == 'perceptron':
            model_ = linear_model.Perceptron(ini_params['penalty'],
                                             ini_params['alpha'],
                                             ini_params['fit_intercept'],
                                             ini_params['max_iter'],
                                             ini_params['tol'],
                                             ini_params['shuffle'],
                                             ini_params['verbose'],
                                             ini_params['eta0'],
                                             ini_params['n_jobs'],
                                             ini_params['random_state'],
                                             ini_params['class_weight'],
                                             ini_params['warm_start'],
                                             ini_params['n_iter'])
        elif type == 'passive_aggressive':
            model_ = linear_model.PassiveAggressiveRegressor(ini_params['c'],
                                                             ini_params['fit_intercept'],
                                                             ini_params['max_iter'],
                                                             ini_params['tol'],
                                                             ini_params['shuffle'],
                                                             ini_params['verbose'],
                                                             ini_params['loss'],
                                                             ini_params['epsilon'],
                                                             ini_params['random_state'],
                                                             ini_params['warm_start'],
                                                             ini_params['average'],
                                                             ini_params['n_iter'])
        elif type == 'auto':
            choose_model(X,y)
        else:
            raise NotImplementedError("This type is not implemented")

        if type != 'auto':
            if avoid_overfitting:
                self.fit(X,y,n_splits= 10)
            else:
                fit(X,y)
        
  
    def fit(self, X, y = None, test_size = 0.25, random_state = 0, n_splits = 1):
        """Fits the sample splitting the sample to avoid overfitting.
        Returns the scores of each iteration.

        :param X: data
        :param y: target
        :param test_size: size of the test, must be between 0 and 1

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type test_size: float
        
        """
        #https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
        scores = []
        sss = StratifiedShuffleSplit(n_iterations, test_size, random_state)
        for train_index, test_index in sss.get_n_splits(X,y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            model_.fit(X_train,y_train)
            scores.append(model_.score(X_test, y_test))
        return scores

    def score(self, X):
        """
        Returns the R^2 coefficient of the prediction.

        :param X: data
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        self.model_.score(X)

    def set_parameters(self,parameters):
        """Sets the parameters of a model."""
        return self.model_.set_paraeters(parameters)

    def get_params(self):
        """Gets the parameters of the model."""
        self.model_.get_params()

    def compare(self, model : LinearModel, X, y):
        """Compares the score of a sample in two models.
        Returns a crossvalidation of metrics, predictions and score.
        
        :param model: model
        :param X: data
        :type model: LinearModel
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        y_pred = model_.predict(X)

        metrics_dict = {}
        metrics_dict['EVS'] = metrics.explained_variance_score(y, y_pred)
        metrics_dict['MeanAE'] = metrics.mean_absolute_error(y, y_pred)
        metrics_dict['MSE'] = metrics.mean_squared_error(y, y_pred)
        metrics_dict['MSLE'] = metrics.mean_squared_log_error(y, y_pred)
        metrics_dict['MedAE'] = metrics.median_absolute_error(y, y_pred)
        metrics_dict['R2'] = metrics.r2_score(y, y_pred)
        
        return metrics_dict

    def choose_model(self,X,y = None):
        """Automatic model chooser.

        :param X: data
        :param y: target

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        """

        #{'linear', 'polynomial',logistic','logisticcv','elasticnet','elasticnetcv','orthogonal','orthogonalcv','theil','sgd','perceptron','passive_aggressive'}
        models = {'linear':linear_model.LinearRegression(),
                  'logistic':linear_model.LogisticRegression(),
                  'elasticnet':linear_model.ElasticNet(),
                  'orthogonal':linear_model.OrthogonalMatchingPursuit(),
                  'theil':linear_model.TheilSenRegressor(),
                  'sgd':linear_model.SGDRegressor(),
                  'passive_agressive':linear_model.PassiveAggressiveRegressor()}
        scores = {}
        for name,model in models:
            scores[name] = []

        sss = StratifiedShuffleSplit(10, 0.25)
        for train_index, test_index in sss.get_n_splits(X,y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            for name, model in models:
                mode.fit(X_train,y_train)
                scores[name].append(model.score(X_test,y_test))
        
        #Choose http://blog.minitab.com/blog/adventures-in-statistics-2/how-to-choose-the-best-regression-model
        index = None
        for name,model in models:
            min = 10000
            if scores[name][-1] < min:
                min = scores[name][-1]
                index = name
        _model = models[index]

        
        
