from abc import ABC, abstractmethod

class DataAnalysis(ABC):

    @abstractmethod
    def draw(self):
        pass