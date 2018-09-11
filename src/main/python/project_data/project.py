import os
import datetime
from ..plots.plot import Multiplot

class Project:
    """Class encapsulating project data."""
    
    def __init__(self): 
        """Empty constructor."""
        pass
    
    def __init__(self, name):
        """Project constructor with name.
        
        :param name: Name of the project.
        """
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
        """Renames current project.
        
        :param name: new name of the project."""
        self.name = name
        #Also change name in path
    
    def add_dataset(self, dataset, path):
        """Adds a dataset to the dataset list.
        
        :param dataset: dataset to add.
        :param path: path to the dataset.
        """
        #Could also do data loading
        self.datasets.append(dataset)
        self.dataset_paths.append(path)
    
    def add_analysis(self, analysis):
        """Adds an analysis to the analysis list.
        
        :param analysis: Analysis to add.
        """
        self.analysis.append(analysis)
    
    def remove_dataset(self, index):
        """Removes a dataset from the dataset list.
        
        :param index: Index of the dataset to remove.
        """
        self.datasets.pop(index)
        self.dataset_paths.pop(index)
    
    def remove_analysis(self, index):
        """Removes an analysis from the analysis list.
        
        :param index: Index of the analysis to remove.
        """
        self.analysis.pop(index)
        
    def save(self):
        """Saves the current project's data into files."""
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
    
    def load_dataset(self,path):
        """Loads a dataset from the given path.
        
        :param path: Path of the dataset.
        """
        pass