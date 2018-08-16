
class Workspace:
    
    def __init__(self, path):
        self.path = path
        
    def switch_workspace(self, path):
        #Close all projects
        self.path = path