from ..plots.plot import Multiplot
import os
import datetime

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
        save()
    
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
        with open('.prj', 'w+') as file:
            file.write('BMLF project')
            file.write(self.name)
            file.write('Last modified at' + datetime.datetime.now())
            
        #Save dataset references
        with open('datasets.ref', 'w+') as file:
            for ref in self.dataset_paths:
                file.write(ref)
        
        #Save analysis in PATH/analysis/
        #How to handle name is yet to determine
        for analysis in self.analysis:
            with open('??', 'w+') as file:
                file.write(analysis)
        
        