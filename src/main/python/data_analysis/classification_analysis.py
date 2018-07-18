import ml_analysis
from sklearn.metrics import classification_report, confusion_matrix

class ClassificationAnalysis(MLAnalysis):
    """Class encapsulating a Classification Analysis on certain data."""
    
    def __init__(self, model, test_data, test_labels):
        super().__init__(model, test_data)
        self.report = classification_report(test_labels, self.predictions) 
        self.confusion_matrix = confusion_matrix(test_labels, self.predictions)
        
    def analyze():
        super().analyze()
        #Decision boundary analysis
        #------ ?
        #accuracy, f1, precision, confusion matrix and other metrics report here
        self.text.append('Classification report for test data')
        self.text.append(str(self.report))
        self.text.append('Confusion matrix for test data')
        self.test.append(str(self.confusion_matrix))
        #log loss, Mean Absolute Error, Mean Squared Error, R^2 pending