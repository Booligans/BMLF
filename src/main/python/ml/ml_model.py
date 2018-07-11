from abc import ABC,abstractmethod
from sklearn.base import clone
from sklearn.model_selection import StratifiedShuffleSplit

class MlModel(ABC):

    """
    Abstract model which defines the general structure.
    """

    @abstractmethod
    def __init__(self, type = 'auto', X = None, y = None, avoid_overfitting = True, **ini_params):
        pass
    
    def __init__(self, type, model):
        """
        Constructor specifying type and model
        """
        #In practice only used by subclasses
        self.__type = type
        self.__model = model
        
    def fit(self, X, y, test_size = 0.25, random_state = 0, n_splits = 1):
        """Fits the sample splitting it to avoid overfitting.
        Returns the scores of each iteration.
         
        :param X: data
        :param y: target
        :param test_size: size of the test, must be between 0 and 1
         
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type test_size: float
        """

        if X is None or y is None:
            raise ValueError("Fit needs data, none given")
        
        #We will fit and store the model and its score for each train/test split

        #Initialize models_scores as an array of copies of the same unfit model with score 0
        models_scores = [[clone(self.__model),0] for i in range(n_splits)]
        best_score = 0
        best_model = 0
        
        #Generate the splits with constant relative category fequency
        sss = StratifiedShuffleSplit(n_splits, test_size, random_state=random_state)

        #Fit and score for each split
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
        self.__model = models_scores[best_model][0]

        #Return the list of scores
        return list(zip(*models_scores))[1]

    def score(self, X, y):
        """
        Returns a score obtained by the model on the given data.
        The metric used depends on the type of model.

        :param X: data
        :param y: labels
        :type X: array-like, shape = (n_samples, n_features)
        :type y: array-like, shape = (n_samples) or (n_samples, n_outputs)
        """
        return self.__model.score(X, y)

    @abstractmethod
    def compare(self, model, X, y):
        pass

    def predict(self, X):
        """Perform classification on given samples.
        :param X: Samples to classify
        :type X: ndarray, shape = (n_samples, n_features)
        """
        return self.__model.predict(X)

    def set_params(self, **parameters):
        """Sets the parameters of a model.
        :param parameters: parameters of the underlying model
        :type parameters: keyword arguments
        """
        self.__model.set_params(**parameters)

    def get_params(self):
        """Gets the parameters of the model."""
        return self.__model.get_params()
            
    def get_model(self):
        """Returns the sklearn model being used as classifier."""
        return self.__model
    
