from abc import ABC, abstractmethod

class DataAnalysis(ABC):
    
    def __init__(self, model):
    """Class constructor.
        
        :param model: predictive model.
        :type model: MlModel
        """
        self.model = model
        self.to_predict = []
        self.predictions = []
        #is score assignment uniform across models?
    
    def predict(self, data):
    """Calculate predictions over certain data and add them to
        the object's data.
        
        :param data: data to make predictions on.
        :type data: ndarray
        """
        self.to_predict.append(data)
        self.predictions.append(self.model.predict(data))
    
    @abstractmethod
    def draw(self):
        pass