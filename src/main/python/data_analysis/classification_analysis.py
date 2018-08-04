from .ml_analysis import MLAnalysis
from sklearn.metrics import classification_report, confusion_matrix, log_loss, mean_absolute_error, r2_score

class ClassificationAnalysis(MLAnalysis):
    """Class encapsulating a Classification Analysis on certain data."""
    
    def __init__(self, model, test_data, test_labels):
        super().__init__(model, test_data)
        self.report = classification_report(test_labels, self.predictions) 
        self.confusion_matrix = confusion_matrix(test_labels, self.predictions)
        self.log_loss = log_loss(test_labels, self.predictions)
        self.mean_absolute_error = mean_absolute_error(test_labels, self.predictions)
        self.r2_score = r2_score(test_labels, self.predictions)
        
    def analyze(self):
        super().analyze()
        #Decision boundary analysis
        #------ ?
        #accuracy, f1, precision, confusion matrix and other metrics report here
        self.text.append('Classification report for test data')
        self.text.append(str(self.report))
        self.text.append('Confusion matrix for test data')
        self.text.append(str(self.confusion_matrix))
        self.text.append('Log loss for test data')
        self.text.append(str(self.log_loss))
        self.text.append('Mean Absolute Error for test data')
        self.text.append(str(self.mean_absolute_error))
        self.text.append('r2 score for test data')
        self.text.append(str(self.r2_score))
        
        