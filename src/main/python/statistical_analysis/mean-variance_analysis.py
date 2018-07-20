import ml_analysis
import numpy as np
class MeanVarianceAnalysis(MLAnalysis):
    """Class encapsulating mean-variance analysis over a dataset."""
    
    def __init__(self,model, data):
        super().__init__(model, data)
    
	def mean(list):
		"""acumulator_mean=0
		for user in data:
			acumulator_mean= acumulator_mean+user[column]
		"""
		return sum(list)/float(len(list))
		
	def variance(list):
		return np.var(list)
		
	def create_list(self,column):
		list=[]
		for i from 0 to len(data)-1:
			list.append(self.data[i][column])
		return list
	def mode(list)
		""" This is a prototype function. It could be more efficient."""
		return max(set(list), key=list.count)
		
	def max(list):
		return max(list)
		
	def min(list)
		return min(list)
		
	def analyze():
		super().analyze()
		mean_list=[]
		variance_list=[]
		mode_list=[]
		max_list=[]
		min_list=[]
		""" It is supposed that there is any user to check data[0]. """
		for i from 0 to len(data[0])-1:
			list=create_list(i)
			if type(data[0][i]) is float:
				mean_list.append(mean(list))
				variance_list.append(variance(list))
			else:
				mode_list.append(mode(list))
			max_list.append(max(list))
			min_list.append(min(list))
				
		self.text.append('Mean of quantitative characteristics:',mean_list)
		self.text.append('Variance of quantitative characteristics:',variance_list)
		self.text.append('Mode of qualitative characteristics',mode_list)
		self.text.append('Maximun of characteristics',max_list)
		self.text.append('Minimun of characteristics',min_list)