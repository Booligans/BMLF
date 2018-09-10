from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn import metrics
from sklearn.model_selection import StratifiedShuffleSplit
from ..mlmodel import MLModel

"""
Support Vector Machine
Multilayer Perceptron
Naive Bayes (Gaussian, Multinomial, Bernoulli)
"""

class MultiModelClassifier(MLModel):
    """A general classifier capable of using different models."""
    
    #Maps type parameter to sklearn classes and other information. Only for internal use
    #This is basically a facade pattern in dict form
    #class: sklearn class
    #params: names of the parameters supported in the sklearn class constructor
    #pred_prob: probability prediction or decision function of the class
    
    _supported_models = {'svm':{'class':svm.SVC,
                               'pred_prob':svm.SVC.decision_function},
                        
                        'mlp':{'class':MLPClassifier,
                               'pred_prob':MLPClassifier.predict_proba},
                        
                        'gaussian_nb':{'class':GaussianNB,
                                       'pred_prob':GaussianNB.predict_proba},
                          
                        'multinomial_nb':{'class':MultinomialNB,
                                          'pred_prob':MultinomialNB.predict_proba},
                                          
                        'bernoulli_nb':{'class':BernoulliNB,
                                        'pred_prob':BernoulliNB.predict_proba}
                        }

    
    def __init__(self, type_='auto', X=None, y=None, avoid_overfitting=True, *args, **kwargs):
        """Initializes the class.

        The type_ parameter defines which model will be chosen, the default will be an
        automated crossvalidation over all supported models. If the type is set to 'auto',
        it will be ingored.

        Additional parameters for the initialization of the model can be specified
        in order or as keyword arguments whose names must match those of the parameters
        in the sklearn library.
        
        When X and y are provided, the model will be directly trained using it.

        :param type_: The type of the model. Supports {'svm', 'mlp', 'gaussian_nb',
        'multinomial_nb','bernoulli_nb'}
        :param X: data
        :param y: target values
        :param avoid_overfitting: avoid overfitting
        :type type_: str
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type avoid_overfitting: boolean

        :Example:
        >>> model = MultiModelClassifier('svm', kernel='linear')
        """

        super().__init__(self._supported_models, type_, X, y, avoid_overfitting, *args, **kwargs)
        
                
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
        y_pred_prob = self._predict_prob(X)

        other_y_pred = model.predict(X)
        other_y_pred_prob = model._predict_prob(X)
        
        self._guess_problem(y)
        
        if self._problem == 'binary':
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

    def split(self, X, y, test_size=0.25, random_state=0, n_splits=1):
        """Return n_splits stratified splittings of the data into train and test groups,
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
        return StratifiedShuffleSplit(n_splits, test_size, random_state=random_state).split(X,y)
    
    def _guess_problem(self, y):
        """Finds out whether classification is binary or multiclass.
        
        :param y: tags
        """
        #Guess the type of classification problem from the given labels.
        n_classes = len(set(y))
        if n_classes == 2:
            self._problem = 'binary'
        elif n_classes > 2:
            self._problem = 'multiclass'
        else:
            raise ValueError('Expected at least two different labels')

    def _predict_prob(self, X):
        #Probability/decision function for the given data
        result = self._supported_models[self._type]['pred_prob'](self._model, X)
        return result if len(result.shape) == 1 else result.max(1)
        
    
