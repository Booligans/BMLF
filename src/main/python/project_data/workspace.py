import os, shutil

class Workspace:
    """Class representing a workspace, where projects are created and stored."""
    
    def __init__(self, path):
        """Initializes the workspace given the path.
        
        :param path: Absolute path of current workspace.
        """
        self.path = path
        
    def switch_workspace(self, path):
        """Switches workspace to indicated path.
        
        :param path: New path for the workspace.
        """
        #Close all projects
        close_project()
        self.path = path
        
    def add_project(self, name):
        """Adds a project to the current workspace.
        
        :param name: Name of the project.
        """
        new_path = os.path.join(self.path, name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            open_project(name)
        else:
            raise ValueError('There is already a file with this name.')
           
    def open_project(self, name):
        """Opens the project with the given name.
        
        :param name: Name of the project.
        """
        os.chdir(os.path.join(self.path, name))
        
    def close_project(self):
        """Closes currently open project."""
        os.chdir(self.path)
        
    def rename_project(self, name, new_name):
        """Renames a project.
        
        :param name: old name of the project.
        :param new_name: new name for the project.
        """
        #Closing renaming and opening should work, but slow
        close_project()
        os.rename(name, new_name)
        open_project(new_name)
    
    def delete_project(self,name):
        """Deletes the project with the indicated name.
        
        :param name: name of the project to delete.
        """
        #DEBUG PRIOR TO TESTING
        close_project()
        #delete project folder
        #shutil.rmtree(self.path + '/' + name)