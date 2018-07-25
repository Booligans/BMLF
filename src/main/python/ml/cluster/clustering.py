from sklearn import cluster
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
from copy import copy, deepcopy
from sklearn import metrics
from mlmodel import MLModel


"""
http://web.engr.oregonstate.edu/~xfern/classes/cs534/notes/Unsupervised-model-11.pdf
"""
class Clustering(MLModel):
    """This class encapsulates a linear model."""
    self.model_ = None
    self.suported_models_ = models = {'kmeans':{'class':cluster.KMeans},
                  'affinity':{'class':cluster.AffinityPropagation},
                  'mean_shift':{'class':cluster.MeanShift},
                  #'spectral':{'class':cluster.SpectralClustering},
                  'agglomerative':{'class':cluster.AgglomerativeClustering},
                  'dbscan':{'class':cluster.DBSCAN},
                  'birch':{'class':cluster.Birch}}

    def __init__(self, type_='auto', X=None, y=None, avoid_overfitting=True, *args, **kwargs):
        """ Initiates the Clustering class.
        
        The type parameter defines which model will be chosen, the default will be an automated crossvalidation over all supported linear models.
        The params parameter is a dictinary that contains all the parameters required for the initialization of the lineal model using the format {'name' : value}, in which the names must match the names of the parameters in the sklearn library (in lower case).
        If the type is set to 'auto', it will be ingored.

        X and y are provided, the model will be directly trained using it.

        More info about the clustering models: http://scikit-learn.org/stable/modules/clustering.html

        :param type: The type of the model. Supports {'kmeans','affinity',mean_shift','spectral','agglomerative','dbscan','birch'}
        :param ini_params: The parameters of the model
        :param X: data
        :param y: target values
        :param avoid_overfitting: avoid overfitting
        :type type: str
        :type ini_params: dictionary
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type avoid_overfitting: boolean

        :Example:
        >>> clustering = Clustering('birch', {'threshold':0.5, 'branching_factor':50, 'n_clusters':3, 'compute_labels':True, 'copy':True})
        """
        if type_ == 'auto':
            self._choose_model(X,y)
        else:
           super().__init__(self.supported_models_,X,y,avoid_overfitting,args,kwargs)

    def compare(self, model : Clustering, X, y = None):
        """
        Compares the score of a sample in two models.
        Returns a crossvalidation of metrics, predictions and score.
        
        More info: https://machinelearningmastery.com/compare-machine-learning-algorithms-python-scikit-learn/
        
        :param model: model
        :param X: data
        :type model: LinearModel
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        metrict_dict = {} #Adjusted Rand Index, Mutual Information
        labels_true = y
        labels_pred = self.model_.predict(X)
        labels_pred_other = model.predict(X)

        labels_other = model.get_model().labels_
        labels = model_.labels_

        if y != None:
            #These metrics require the knowledge of the ground truth classes
            metrict_dict['ARI'] = (metrics.adjusted_rand_score(labels_true, labels_pred), metrics.adjusted_rand_score(labels_true, labels_pred_other))
            metrict_dict['MIS'] = (metrics.adjusted_mutual_info_score(labels_true, labels_pred), metrics.adjusted_mutual_info_score(labels_true, labels_pred_other))
            metrict_dict['homogeneity'] = (metrics.homogeneity_score(labels_true, labels_pred),metrics.homogeneity_score(labels_true, labels_pred_other))
            metrict_dict['completeness'] = (metrics.completeness_score(labels_true, labels_pred),metrics.completeness_score(labels_true, labels_pred_other))
            metrict_dict['v_measure'] = (metrics.v_measure_score(labels_true, labels_pred),metrics.v_measure_score(labels_true, labels_pred_other))
            metrict_dict['FMS'] = (metrics.fowlkes_mallows_score(labels_true, labels_pred),metrics.fowlkes_mallows_score(labels_true, labels_pred_other))

        #These metrics DON'T require the knowledge of the ground truth classes
        metrict_dict['SS'] = (metrics.silhouette_score(X, labels, metric='euclidean'),metrics.silhouette_score(X, labels_other, metric='euclidean'))
        metrict_dict['CHI'] = (metrics.calinski_harabaz_score(X, labels),metrics.calinski_harabaz_score(X, labels_other))
        return metrict_dict

    def _choose_model(self,X,y = None, crossvalidation = 'silhouette'):
        """
        Automatic model chooser.

        :param X: data
        :param y: target

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        """

        scores = {}
        min = 1
        
        for name,model in self._get_initiated_models(X,y,'silhouette'):
            score = metrics.silhouette_score(X, model.labels_, metric='euclidean')
            if score < min:
                min = score
                self._model = model
        

    def get_metrics(self, X, y = None):
        """
        Returns a dictionary of the metrics of the model. If y is not provided, no metrics that require the true labels will be provided.
        More info:http://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation
        
        :param X: data
        :param y: target

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)

        """
        metrict_dict = {} #Adjusted Rand Index, Mutual Information
        labels_true = y
        labels_pred = self.model_.predict(X)
        labels = self.model_.labels_

        if y != None:
            #These metrics require the knowledge of the ground truth classes
            metrict_dict['ARI'] = metrics.adjusted_rand_score(labels_true, labels_pred)
            metrict_dict['MIS'] = metrics.adjusted_mutual_info_score(labels_true, labels_pred)
            metrict_dict['homogeneity'] =  metrics.homogeneity_score(labels_true, labels_pred)
            metrict_dict['completeness'] =  metrics.completeness_score(labels_true, labels_pred)
            metrict_dict['v_measure'] =  metrics.v_measure_score(labels_true, labels_pred)
            metrict_dict['FMS'] = metrics.fowlkes_mallows_score(labels_true, labels_pred)

        #These metrics DON'T require the knowledge of the ground truth classes
        metrict_dict['SS'] = metrics.silhouette_score(X, labels, metric='euclidean')
        metrict_dict['CHI'] = metrics.calinski_harabaz_score(X, labels) 

        return metrict_dict

    def _get_initiated_models(self, X, y, method : 'silhouette'):
        """
        (Far from finished)

        Sets the best k for the k-means model in the supported models.
        The supported methods include 'silhouette', 'calinski' and 'elbow', which requires the user's final decision.

        https://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set
        """
        aggmax = -1
        aggind = 0

        kmax = -1
        kind = 0

        bmax = -1
        bind = 0

        fin_models = {}

        if method == 'silhouette' or method == 'calinski':
            fin_models['dbscan'] = cluster.DBSCAN()
            fin_models['affinity'] = cluster.AffinityPropagation()
            fin_models['mean_shift'] = cluster.MeanShift()

            sss = StratifiedShuffleSplit(10, 0.25)
            for train_index, test_index in sss.get_n_splits(X,y):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                kmodels = {}
                aggmodels = {}
                for i in range(1,30):
                    kmodels[i] = self.suported_models_['kmeans']['class'](i)
                    aggmodels[i] = self.supported_models_['aglomerative']['class'](i,linkage='average')
                    birchmodels[i] = self.supported_models_['birch']['class'](n_clusters=i)

                for name,model in fin_models:
                    model.fit(X_train,y_train)
            
            for i in range(30):
                coeff = silhouette_score(X, kmodels[i].labels_, metric='euclidean') if method == 'silhouette' else metrics.calinski_harabaz_score(X, kmodels[i].labels_) 
                if coeff > kmax:
                    kmax = coeff
                    kind = i
                coeff = silhouette_score(X, aggmodels[i].labels_, metric='euclidean') if method == 'silhouette' else metrics.calinski_harabaz_score(X, aggmodels[i].labels_) 
                if coeff > aggmax:
                    aggmax = coeff
                    aggind = i
                coeff = silhouette_score(X, birchmodels[i].labels_, metric='euclidean') if method == 'silhouette' else metrics.calinski_harabaz_score(X, birchmodels[i].labels_) 
                if coeff > birchmax:
                    birchmax = coeff
                    birchind = i

            fin_models['kmeans'] = kmodels[kind]
            fin_models['agglomerative'] = aggmodels[aggind]

        else:
            pass

        return fin_models

        

       
    #def fit(self, X, y = None, test_size = 0.25, random_state = 0, n_splits = 1):
    #    """
    #    Fits the sample splitting the sample to avoid overfitting.
    #    Returns the scores of each iteration.

    #    :param X: data
    #    :param y: target
    #    :param test_size: size of the test, must be between 0 and 1

    #    :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
    #    :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
    #    :type test_size: float
        
    #    """
    #    #https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
    #    scores = []
    #    sss = StratifiedShuffleSplit(n_iterations, test_size, random_state)
    #    for train_index, test_index in sss.get_n_splits(X,y):
    #        X_train, X_test = X[train_index], X[test_index]
    #        y_train, y_test = y[train_index], y[test_index]
    #        model_.fit(X_train,y_train)
    #        scores.append(model_.score(X_test, y_test))
    #    return scores

    #def score(self, X):
    #    """
    #    Returns the R^2 coefficient of the prediction.

    #    :param X: data
    #    :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
    #    """
    #    self.model_.score(X)

    #def set_parameters(self,parameters):
    #    """Sets the parameters of a model."""
    #    return self.model_.set_paraeters(parameters)

    #def get_params(self):
    #    """Gets the parameters of the model."""
    #    self.model_.get_params()