class project:
    
    def __init__(self, name="New Project"):
        self.name = name
        analysis = []
    
    
    def rename(self, name):
        self.name = name
    
    def load_data(self, source):
        #Requires implementation (pandas)
        #Read into numpy array
        #Previous analysis must be reset
        self.analysis = []
    
    def add_analysis(self, analysis):
        self.analysis.append(analysis)
    
    def delete_analysis(self, index):
        self.analysis.pop(index)
        
    def save(self):
        #Save into files, needs implementation
    
    #A load method is also necessary