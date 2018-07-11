from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn import metrics
from ml.ml_model import MlModel

"""
Support Vector Machine
Multilayer Perceptron
Naive Bayes (Gaussian, Multinomial, Bernoulli)
"""

class MultiModelClassifier(MlModel):
    """A general classifier capable of using different models."""
    
    #Maps type parameter to sklearn classes and other information. Only for internal use
    #This is basically a facade pattern in dict form
    #class: sklearn class
    #params: names of the parameters supported in the sklearn class constructor
    #pred_prob: probability prediction or decision function of the class
    
    __supported_models = {'svm':{'class':svm.SVC,
                               'params':svm.SVC.get_params(svm.SVC).keys(),
                               'pred_prob':svm.SVC.decision_function},
                        
                        'mlp':{'class':MLPClassifier,
                               'params':MLPClassifier.get_params(MLPClassifier).keys(),
                               'pred_prob':MLPClassifier.predict_proba},
                        
                        'gaussian_nb':{'class':GaussianNB,
                                       'params':GaussianNB.get_params(GaussianNB).keys(),
                                       'pred_prob':GaussianNB.predict_proba},

                          
                        'multinomial_nb':{'class':MultinomialNB,
                                          'params':MultinomialNB.get_params(MultinomialNB).keys(),
                                          'pred_prob':MultinomialNB.predict_proba},
                                          
                        'bernoulli_nb':{'class':BernoulliNB,
                                        'params':BernoulliNB.get_params(BernoulliNB).keys(),
                                        'pred_prob':BernoulliNB.predict_proba}
                        }

    
    def __init__(self, type = 'auto', X = None, y = None, avoid_overfitting = True, **ini_params):
        """Initializes the class.

        The type parameter defines which model will be chosen, the default will be an
        automated crossvalidation over all supported models. If the type is set to 'auto',
        it will be ingored.

        The ini_params parameter is a dictinary that contains all the parameters required for
        the initialization of the model using the format name=value, in which the names
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
        
        if type == 'auto':
            super().__init__('auto', None)
            self.choose_model(X,y)
            
        elif type in self.__supported_models.keys():
            #Select the model from __supported_models and get the data from ini_params into parameters
                        
            model = self.__supported_models[type]['class']
            param_tags = self.__supported_models[type]['params']
            parameters = {key:ini_params.get(key) for key in param_tags if key in ini_params.keys()}

            super().__init__(type, model(**parameters))

            #Train the model
            if not X is None and not y is None:
                if avoid_overfitting:
                    self.scores_ = self.fit(X,y,n_splits=10)
                else:
                    self.scores_ = self.fit(X,y)

        else:
            print('Unsupported model: ' + type)
            
    def score(self, X, y):
        """
        Returns the mean accuracy on the given data.

        :param X: data
        :param y: labels
        :type X: array-like, shape = (n_samples, n_features)
        :type y: array-like, shape = (n_samples) or (n_samples, n_outputs)
        """
        return super().score(X, y)
            
    def compare(self, model, X, y):
        """Compares the score of a sample in two models.
        Returns a crossvalidation of metrics, predictions and score.
        
        :param model: model
        :param X: data
        :type model: MultiModelClassifier
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        scores = {}
        y_pred = self.predict(X)
        y_pred_prob = self.__predict_prob(X)

        other_y_pred = model.predict(X)
        other_y_pred_prob = model.__predict_prob(X)
        
        self.__guess_problem(y)
        
        if self.__problem == 'binary':
            #Binary-only metrics
                        
            scores['PreRec'] = (metrics.precision_recall_curve(y, y_pred_prob),
                                metrics.precision_recall_curve(y, other_y_pred_prob))
            
            scores['ROC'] = (metrics.roc_curve(y, y_pred_prob),
                             metrics.roc_curve(y, other_y_pred_prob))
            
        scores['Kappa'] = (metrics.cohen_kappa_score(y, y_pred),
                           metrics.cohen_kappa_score(y, other_y_pred))
        scores['Confusion'] = (metrics.confusion_matrix(y, y_pred),
                               metrics.confusion_matrix(y, other_y_pred))
        scores['HL'] = (metrics.hinge_loss(y, y_pred_prob),
                        metrics.hinge_loss(y, other_y_pred_prob))
        scores['MCC'] = (metrics.matthews_corrcoef(y, y_pred),
                         metrics.matthews_corrcoef(y, other_y_pred))

        return scores

    
    def choose_model(self, X, y):
        pass
    
    def __guess_problem(self, y):
        #Guess the type of classification problem from the given labels.
        n_classes = len(set(y))
        if n_classes == 2:
            self.__problem = 'binary'
        elif n_classes > 2:
            self.__problem = 'multiclass'
        else:
            raise ValueError('Expected at least two different labels')

    def __predict_prob(self, X):
        #Probability/decision function for the given data
        result = self.__supported_models[self._MlModel__type]['pred_prob'](self._MlModel__model, X)
        return result if len(result.shape) == 1 else result.max(1)
        
