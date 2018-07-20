from sklearn import decomposition
#from mlmodel import MLModel

class PCAReductor(object):
    
    def __init__(self, type='auto', *args, **kwargs):
        
        if type=='auto':
            self.model = decomposition.PCA(*args,**kwargs)
        elif type=='incremental':
            self.model = decomposition.IncrementalPCA(*args,**kwargs)
        elif type=='kernel':
            self.model = decomposition.KernelPCA(*args,**kwargs)
        else:
            raise ValueError('The type ', type, ' does not exist.')
            
    def fit(self,data):
        self.model.fit(data)
        
    def transform(self,data):
        return self.model.transform(data)
    
    def fit_transform(self,data):
        return self.model.fit_transform(data)