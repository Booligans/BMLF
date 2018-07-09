from sklearn import svm
from sklearn.base import clone
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.model_selection import StratifiedShuffleSplit

"""
Support Vector Machine
Multilayer Perceptron
Naive Bayes (Gaussian, Multinomial, Bernoulli)
"""

class MultiModelClassifier:
    """A general classifier capable of using different models."""

    #Maps type parameter to sklearn classes and parameter lists
    supported_models = {'svm':(svm.SVC, svm.SVC.get_params(svm.SVC).keys()),
                        'mlp':(MLPClassifier, MLPClassifier.get_params(MLPClassifier).keys()),
                        'gaussian_nb':(GaussianNB, GaussianNB.get_params(GaussianNB).keys()),
                        'multinomial_nb':(MultinomialNB,
                                          MultinomialNB.get_params(MultinomialNB).keys()),
                        'bernoulli_nb':(BernoulliNB, BernoulliNB.get_params(BernoulliNB).keys())}

    
    def __init__(self, type = 'auto', X = None, y = None, avoid_overfitting = True, **ini_params):
        """Initializes the class.

        The type parameter defines which model will be chosen, the default will be an
        automated crossvalidation over all supported models. If the type is set to 'auto',
        it will be ingored.

        The ini_params parameter is a dictinary that contains all the parameters required for
        the initialization of the model using the format name=value}, in which the names
        must match the names of the parameters in the sklearn library (in lower case).
        
        X and y are provided, the model will be directly trained using it.

        :param type: The type of the model. Supports {'svm', 'mlp', 'gaussian_nb',
        'multinomial_nb','bernoulli_nb'}
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
        >>> model = MultiModelClassifier('svm', {'kernel':'rbf'})
        """

        self._type = type

        if type == 'auto':
            self.choose_model(X,y)
            
        elif type in self.supported_models.keys():
            #Select the model from supported_models and get the data from ini_params into parameters
                        
            (model, param_tags) = self.supported_models[type]
            parameters = {key:ini_params.get(key) for key in param_tags if key in ini_params.keys()}
            
            self.model_ = model(**parameters)

            #Train the model
            if avoid_overfitting:
                self.scores_ = self.fit(X,y,n_splits=10)
            else:
                self.scores_ = self.fit(X,y)

        else:
            print('Unsupported model: ' + type)


    def fit(self, X, y = None, test_size = 0.25, random_state = 0, n_splits = 1):
        """Fits the sample splitting it to avoid overfitting.
        Returns the scores of each iteration.
         
        :param X: data
        :param y: target
        :param test_size: size of the test, must be between 0 and 1
         
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type test_size: float
        """

        #We will fit and store the model and its score for each train/test split,
        models_scores = [[clone(self.model_),0] for i in range(n_splits)]
        best_score = 0
        best_model = 0
        
        #Generate the splits with constant relative category fequency
        sss = StratifiedShuffleSplit(n_splits, test_size, random_state=random_state)
        
        for i, (train, test) in enumerate(sss.split(X,y)):
            X_train, y_train = zip(*[(X[i],y[i]) for i in train])
            X_test, y_test = zip(*[(X[i],y[i]) for i in test])
        
            model = models_scores[i][0].fit(X_train, y_train)
    
            #The scores are evaluated with the test samples
            models_scores[i][1] = model.score(X_test, y_test)
            if models_scores[i][1] > best_score:
                best_score = models_scores[i][1]
                best_model = i

        #Use the best model found
        self.model_ = models_scores[best_model][0]

        #Return the list of scores
        return [e for e in zip(*models_scores)][1]
        
         
    def score(self, X):
        pass

    def set_parameters(self, parameters):
        """Sets the parameters of a model."""
        self.model_.set_parameters(parameters)

    def get_params(self):
        """Gets the parameters of the model."""
        return self.model_.get_params()

    def get_model(self):
        """Returns the sklearn model being used as classifier."""
        return self.model_
        
    def compare(self, model, X, y = None):
        pass

    def choose_model(self, X, y = None):
        pass

    
