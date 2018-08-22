from abc import ABC, abstractmethod

class Data:
    def __init__(self, data, headers=None, **metadata):
        self.complete_data = {'data':data}
        if headers is not None:
            self.complete_data['headers'] = headers
        for key in metadata.keys():
            self.complete_data[key] = metadata[key]

    def get_data(self):
        return self.complete_data['data']

    def set_data(self, data):
        self.complete_data['data'] = data

    def get_headers(self):
        return self.get_field('headers')

    def set_headers(self, headers):
        self.set_field('headers', headers)

    def get_field(self, key):
        return self.complete_data[key] if key in self.complete_data.keys() else None

    def set_field(self, key, val):
        self.complete_data[key] = val

    
                
    

class DataMedium(ABC):
    """
    Abstract data medium for storing, saving, and displaying data.
    """
    #The main subclass here is TableWidget, needed for other widgets to manipulate its data

    @abstractmethod
    def store_data(self, data, *args, **kwargs):
        """
        Store data into the medium.
        :param data: Data to store.
        :type data: Data
        """
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        """
        Retrieve data from the medium.
        """
        pass

    
class Clipboard:
    """
    Clipboard for storing and manipulating data from a medium
    """
    def __init__(self, medium):
        self.medium = medium
        self.data = {}
        
    
    def store_data(self, data, key=''):
        """
        Store generated data into the toolbar.
        :param data: Data to store.
        :type data: Data
        """
        self.data[key] = data

    def get_data(self, key=''):
        """
        Retrieve selected data from the toolbar.
        """
        if key in self.data.keys():
            return self.data[key]
        else:
            raise KeyError(key)

    def save_to_medium(self, *args, key='', **kwargs):
        """
        Save stored data to the medium
        """
        if key in self.data.keys():
            self.medium.store_data(self.data[key], *args, **kwargs)
        else:
            raise KeyError(key)

    def load_from_medium(self, *args, key='', **kwargs):
        """
        Load data from the medium and store it
        """
        self.data[key] = self.medium.get_data(*args, **kwargs)

    def get_keys(self):
        return self.data.keys()
        
