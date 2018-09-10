from abc import ABC

class DataAnalysis(ABC):
"""Class representing a generic data analysis."""

    def analyze(self, data):
        """Initializes analysis text.
        
        :param data: data used as testing data or for estimator analysis.
        """
        self.text = []
        self.text.append('Number of items: ', len(data)) #rows of data matrix
        self.text.append('Number of features: ', len(data[0])) #columns of data matrix, assumes non-empty data