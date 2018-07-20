import ml_analysis
class MeanVarianceAnalysis(MLAnalysis):
    """Class encapsulating mean-variance analysis over a dataset."""
    
    def __init__(self,model, data):
        super().__init__(model, data)
    
	def mean(column):
		"""acumulator_mean=0
		for user in data:
			acumulator_mean= acumulator_mean+user[column]
		"""
		list=create_list(column)
		return sum(list)/float(len(list))
		
	def variance(column):
		
		acumulator_variance=0
		for user in data:
			acumulator_variance= acumulator_variance+(user[column]*user[column])
			
		return acumulator_variance/float(len(data))
		
	def create_list(column):
		list=[]
		for user in data:
			list.append(user[column])
		return list
	def mode(column)
		""" This is a prototype function. It could be more efficient."""
		list=create_list(column)
		return max(set(list), key=list.count)
		
	def max(column):
		list=create_list(column)
		return max(list)
		
	def min(column)
		list=create_list(column)
		return min(list)
		
    def analyze():
        super().analyze()
		mean_list=[]
		variance_list=[]
		mode_list=[]
		max_list=[]
		min_list=[]
		""" It is supposed that there is any user to check data[0]. """
		for i in range(0,len(data[0])):
			if type(data[0][i]) is float:
				mean_list.append(mean(i))
				variance_list.append(variance(i))
			else:
				mode_list.append(mode(i))
			max_list.append(max(i))
			min_list.append(min(i))
				
		self.text.append('Mean of quantitative characteristics:',mean_list)
		self.text.append('Variance of quantitative characteristics:',variance_list)
		self.text.append('Mode of qualitative characteristics',mode_list)
		self.text.append('Maximun of characteristics',max_list)
		self.text.append('Minimun of characteristics',min_list)