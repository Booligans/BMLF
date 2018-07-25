from sklearn import linear_model
from sklearn.model_selection import ShuffleSplit, cross_val_predict, cross_val_score, cross_validate
from mlmodel import MLModel
from sklearn import metrics

"""
Implementing Polynomial regression as Linear regression: https://stats.stackexchange.com/questions/58739/polynomial-regression-using-scikit-learn
"""

class LinearModel(MLModel):
    """This class encapsulates a linear model."""

    #Maps type parameter to sklearn classes and other information. Only for internal use
    #This is basically a facade pattern in dict form
    #class: sklearn class
    #params: names of the parameters supported in the sklearn class constructor
    
    _supported_models = {'linear':{'class':linear_model.LinearRegression},
                          
                          'elasticnet':{'class':linear_model.ElasticNet},
                          
                          'elasticnetcv':{'class':linear_model.ElasticNetCV},
                          
                          'bayes_ridge':{'class':linear_model.BayesianRidge},
                          
                          'orthogonal':{'class':linear_model.OrthogonalMatchingPursuit},
                          
                          'orthogonalcv':{'class':linear_model.OrthogonalMatchingPursuitCV},
                          
                          'theil':{'class':linear_model.TheilSenRegressor},
                          
                          'sgd':{'class':linear_model.SGDRegressor},
                          
                          'perceptron':{'class':linear_model.Perceptron},
                          
                          'passive-agressive':{'class':linear_model.PassiveAggressiveRegressor}}
    

    def __init__(self, type_='auto', X=None, y=None, avoid_overfitting=True, *args, **kwargs):
        """ Initiates the Regression class.
        
        The type_ parameter defines which model will be chosen, the default will be an
        automated crossvalidation over all supported linear models. If the type_ is set to 'auto',
        it will be ingored.
        
        Additional parameters for the initialization of the model can be specified
        in order or as keyword arguments whose names must match those of the parameters
        in the sklearn library.

        When X and y are provided, the model will be directly trained using it.

        :param type: The type of the model. Supports {'linear', 'polynomial',logistic','logisticcv','elasticnet','elasticnetcv','orthogonal','orthogonalcv','theil','sgd','perceptron','passive_aggressive'}
        :param X: data
        :param y: target values
        :param avoid_overfitting: avoid overfitting
        :type type: str
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type avoid_overfitting: boolean

        :Example:
        >>> model = LinearModel('linear', fit_intercept=True, normalize=True, copy_x=True, n_jobs=1)
        """
        if type_ == 'auto':
                self.choose_model(X,y)
        else:
            super().__init__(self._supported_models, type_, X, y, avoid_overfitting, *args, **kwargs)


    def split(self, X, y, test_size=0.25, random_state=0, n_splits=1):
        """Return n_splits splittings of the data into train and test groups,
        as a list of tuples of lists of indexes in the data

        :param X: data
        :param y: target
        :param test_size: Percentage of the data in the test set
        :param random_state: Seed for the PRNG
        :param n_splits: Number of splits to make
        :type X: array-like, shape = (n_samples, n_features)
        :type y: array-like, shape = (n_samples) or (n_samples, n_outputs)
        :type test_size: float
        :type random_state: int
        :type n_splits: int
        """
        return ShuffleSplit(n_splits, test_size, random_state=random_state).split(X,y)
  
        
    def compare(self, model, X, y):
        """Compares the score of a sample in two models.
        Returns a crossvalidation of metrics, predictions and score.
        
        :param model: model
        :param X: data
        :type model: LinearModel
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        y_pred = self.predict(X)
        other_y_pred = model.predict(X)

        metrics_dict = {}
        metrics_dict['EVS'] = (metrics.explained_variance_score(y, y_pred),
                               metrics.explained_variance_score(y, other_y_pred))
        metrics_dict['MeanAE'] = (metrics.mean_absolute_error(y, y_pred),
                                  metrics.mean_absolute_error(y, other_y_pred))
        metrics_dict['MSE'] = (metrics.mean_squared_error(y, y_pred),
                               metrics.mean_squared_error(y, other_y_pred))
        metrics_dict['MSLE'] = (metrics.mean_squared_log_error(y, y_pred),
                                metrics.mean_squared_log_error(y, other_y_pred))
        metrics_dict['MedAE'] = (metrics.median_absolute_error(y, y_pred),
                                 metrics.median_absolute_error(y, other_y_pred))
        metrics_dict['R2'] = (metrics.r2_score(y, y_pred),
                              metrics.r2_score(y, other_y_pred))
        
        return metrics_dict

    def _choose_model(self, X, y):
        """
        Automatic model chooser.

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
        for name,model in models.items():
            scores[name] = []

        sss = StratifiedShuffleSplit(10, 0.25)
        for train_index, test_index in sss.split(X,y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            for name, model in models:
                mode.fit(X_train,y_train)
                scores[name].append(metrics.mean_squared_error(X_test,y_test))
        
        #Choose http://blog.minitab.com/blog/adventures-in-statistics-2/how-to-choose-the-best-regression-model
        index = None
        for name,model in models:
            min = 10000
            if scores[name][-1] < min:
                min = scores[name][-1]
                _model = model
        
