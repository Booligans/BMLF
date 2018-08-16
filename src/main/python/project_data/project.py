from ..plots.plot import Multiplot

class Project:
    
    def __init__(self, name):
        self.name = name
        self.analysis = []
        self.datasets = []
        self.plots = Multiplot(name)
    
    def rename(self, name):
        self.name = name
        #Also change name in path
    
    def add_dataset(self, dataset):
        self.datasets.append(dataset)
    
    def add_analysis(self, analysis):
        self.analysis.append(analysis)
    
    def remove_dataset(self, index):
        self.datasets.pop(index)
    
    def remove_analysis(self, index):
        self.analysis.pop(index)
        
    def save(self):
        #Save into files, needs implementation