from abc import ABC, abstractmethod

class DataAnalysis(ABC):

    def analyze(self, data):
        self.text = []
        self.text.append('Number of items: ', len(data)) #rows of data matrix
        self.text.append('Number of features: ', len(data[0])) #columns of data matrix, assumes non-empty data