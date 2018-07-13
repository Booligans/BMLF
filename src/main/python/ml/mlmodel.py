from abc import ABC,abstractmethod
from sklearn.base import clone

class MLModel(ABC):

    """
    Abstract model which defines the general structure.
    """

    @abstractmethod
    def __init__(self, type_='auto', X=None, y=None, avoid_overfitting=True, *args, **kwargs):
        pass

    
    def __init__(self, supported_models, type_='auto', X=None, y=None, avoid_overfitting=True, *args, **kwargs):
        """
        General constructor with specified supported models

        The type_ parameter defines which model will be chosen, the default will be an
        automated crossvalidation over all supported models. If the type_ is set to 'auto',
        it will be ingored.

        Additional parameters for the initialization of the model can be specified
        in order or as keyword arguments whose names must match those of the parameters
        in the sklearn library.

        When X and y are provided, the model will be directly trained using it.

        :param type_: The type_ of the model
        :param X: data
        :param y: target values
        :param avoid_overfitting: avoid overfitting
        :param supported_models: data of supported models
        :type type_: str
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type avoid_overfitting: boolean
        :type supported_models: dictionary
        """
        
        self._type = type_
        
        if type_ == 'auto':
            self._model = None
            self.choose_model(X,y)
            
        elif type_ in supported_models.keys():
            #Select the model from __supported_models and get the data from kwargs into parameters
                        
            model = supported_models[type_]['class']

            try:
                self._model = model(*args, **kwargs)
            except TypeError as err:
                raise TypeError('Unexpected argument for ' + type_ + ' : \n' + err.args)

            #Train the model
            if X is not None and y is not None:
                if avoid_overfitting:
                    self.scores = self.fit(X,y,n_splits=10)
                else:
                    self.scores = self.fit(X,y)

        else:
            raise ValueError('Unsupported model: ' + type_)
            
            
    def fit(self, X, y, test_size=0.25, random_state=0, n_splits=1):
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
        models_scores = [[clone(self._model),0] for i in range(n_splits)]
        best_score = 0
        best_model = 0
        
        #Generate the splits with constant relative category fequency
        split = self.split(X, y, test_size, random_state, n_splits)

        #Fit and score for each split
        for i, (train, test) in enumerate(split):
            X_train, y_train = zip(*[(X[i],y[i]) for i in train])
            X_test, y_test = zip(*[(X[i],y[i]) for i in test])
        
            model = models_scores[i][0].fit(X_train, y_train)
    
            #The scores are evaluated with the test samples
            models_scores[i][1] = model.score(X_test, y_test)
            if models_scores[i][1] > best_score:
                best_score = models_scores[i][1]
                best_model = i

        #Use the best model found
        self._model = models_scores[best_model][0]

        #Return the list of scores
        return list(zip(*models_scores))[1]

    def score(self, X, y):
        """
        Returns a score obtained by the model on the given data.
        The metric used depends on the type_ of model.

        :param X: data
        :param y: labels
        :type X: array-like, shape = (n_samples, n_features)
        :type y: array-like, shape = (n_samples) or (n_samples, n_outputs)
        """
        return self._model.score(X, y)

    @abstractmethod
    def choose_model(self, X, y):
        pass
    
    @abstractmethod
    def compare(self, model, X, y):
        pass

    @abstractmethod
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
        pass

    def predict(self, X):
        """Perform classification on given samples.
        :param X: Samples to classify
        :type X: ndarray, shape = (n_samples, n_features)
        """
        return self._model.predict(X)

    def set_params(self, *args, **kwargs):
        """Sets the parameters of a model.
        :param parameters: parameters of the underlying model
        :type parameters: keyword arguments
        """
        self._model.set_params(*args, **kwargs)

    def get_params(self):
        """Gets the parameters of the model."""
        return self._model.get_params()
            
    def get_model(self):
        """Returns the sklearn model being used as classifier."""
        return self._model
    
