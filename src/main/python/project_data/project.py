from ..plots.plot import Multiplot
import os

class Project:
    
    def __init__(self, name):
        self.name = name
        self.analysis = []
        self.datasets = []
        self.dataset_paths = []
        self.plots = Multiplot(name)
        #Create .prj file
        open('.prj', 'w+')
        #Create datasets.ref file
        open('datasets.ref', 'w+')
        os.makedirs('analysis')
    
    def rename(self, name):
        self.name = name
        #Also change name in path
    
    def add_dataset(self, dataset, path):
        self.datasets.append(dataset)
        self.dataset_paths.append(path)
    
    def add_analysis(self, analysis):
        self.analysis.append(analysis)
    
    def remove_dataset(self, index):
        self.datasets.pop(index)
        self.dataset_paths.pop(index)
    
    def remove_analysis(self, index):
        self.analysis.pop(index)
        
    def save(self):
        #Save into files, needs implementation
        #Set path to WORKSPACE_PATH/PROJECT_NAME/
        #Save new data to .prj
        #Save dataset references
        #Save analysis in PATH/analysis/
        pass
        