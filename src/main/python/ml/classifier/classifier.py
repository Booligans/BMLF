from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

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

    
    def __init__(self, type = 'auto', ini_params = {}, X = None, y = None, avoid_overfitting = True):
        """Initializes the class.

        The type parameter defines which model will be chosen, the default will be an automated crossvalidation over all supported models.
        The params parameter is a dictinary that contains all the parameters required for the initialization of the model using the format {'name' : value}, in which the names must match the names of the parameters in the sklearn library (in lower case).
        If the type is set to 'auto', it will be ingored.

 X and y are provided, the model will be directly trained using it.

        :param type: The type of the model. Supports {'svm', 'mlp', 'gaussian_nb','multinomial_nb','bernoulli_nb'}
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
            parameters = {key:val for (key, val) in
                          zip(param_tags, [ini_params.get(tag) for tag in param_tags])}
            
            self.model_ = model(parameters)

            #Train the model
            if avoid_overfitting:
                self.fit(X,y,n_splits= 10)
            else:
                self.fit(X,y)

        else:
            print('Unsupported model: ' + type)


    def fit(self, X, y = None, test_size = 0.25, random_state = 0, n_splits = 1):
        pass

    def score(self, X):
        pass

    def set_parameters(self,parameters):
        pass

    def get_params(self):
        pass

    def compare(self, model, X, y = None):
        pass

    def choose_model(self, X, y = None):
        pass

    
