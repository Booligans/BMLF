import os

class Workspace:
    
    def __init__(self, path):
        self.path = path
        
    def switch_workspace(self, path):
        #Close all projects
        close_project()
        self.path = path
        
    def add_project(self, name):
        new_path = os.path.join(self.path, name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        else:
            raise ValueError('There is already a file with this name.')
           
    def open_project(self, name):
        os.chdir(os.path.join(self.path, name))
        
    def close_project(self):
        os.chdir(self.path)
        
    def rename_project(self, name, new_name):
        #Closing renaming and opening should work, but slow
        close_project()
        os.rename(name, new_name)
        open_project(new_name)