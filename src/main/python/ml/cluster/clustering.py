from sklearn import cluster
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
from copy import copy, deepcopy
from sklearn import metrics

class Clustering(object):
    """This class encapsulates a linear model."""
    self.model_ = None
    self.suported_models = models = {'kmeans':cluster.KMeans(),
                  'affinity':cluster.AffinityPropagation(),
                  'mean_shift':cluster.MeanShift(),
                  'spectral':cluster.SpectralClustering(),
                  'agglomerative':cluster.AgglomerativeClustering(),
                  'dbscan':cluster.DBSCAN(),
                  'birch':cluster.Birch()}

    def __init__(self, type = 'auto', ini_params = {}, X = None, y = None, avoid_overfitting = True):
        """ Initiates the Regression class.
        
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

        if type == 'auto':
            self.choose_model(X,y)
            
        elif type in self.supported_models.keys():
            #Select the model from supported_models and get the data from ini_params into parameters
                        
            (model, param_tags) = self.supported_models[type]
            parameters = {key:val for (key, val) in
                          zip(param_tags, [ini_params.get(tag) for tag in param_tags])}
            
            self.model_ = model(parameters)

            #Train the model
            if avoid_overfitting:
                self.fit(X,y,n_splits= 10)
            else:
                self.fit(X,y)
        
        
  
    def fit(self, X, y = None, test_size = 0.25, random_state = 0, n_splits = 1):
        """
        Fits the sample splitting the sample to avoid overfitting.
        Returns the scores of each iteration.

        :param X: data
        :param y: target
        :param test_size: size of the test, must be between 0 and 1

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        :type test_size: float
        
        """
        #https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
        scores = []
        sss = StratifiedShuffleSplit(n_iterations, test_size, random_state)
        for train_index, test_index in sss.get_n_splits(X,y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            model_.fit(X_train,y_train)
            scores.append(model_.score(X_test, y_test))
        return scores

    def score(self, X):
        """
        Returns the R^2 coefficient of the prediction.

        :param X: data
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        self.model_.score(X)

    def set_parameters(self,parameters):
        """Sets the parameters of a model."""
        return self.model_.set_paraeters(parameters)

    def get_params(self):
        """Gets the parameters of the model."""
        self.model_.get_params()

    def compare(self, model : LinearModel, X, y = None):
        """Compares the score of a sample in two models.
        Returns a crossvalidation of metrics, predictions and score.
        
        More info: https://machinelearningmastery.com/compare-machine-learning-algorithms-python-scikit-learn/
        
        :param model: model
        :param X: data
        :type model: LinearModel
        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        """
        pass
        #metric = cross_validate(estimator=model.model_,X=X,y=y,scoring='r2')
        #predictions = cross_val_predict(model.model_,X=X,y=y)
        #score = cross_val_score(model.model_, X, y)
        #return metric, predictions, score

    def choose_model(self,X,y = None):
        """Automatic model chooser.

        :param X: data
        :param y: target

        :type X: ndarray or scipy.sparse matrix, (n_samples, n_features)
        :type y: ndarray, shape (n_samples,) or (n_samples, n_targets)
        """

        scores = {}
        for name,model in supported_models:
            scores[name] = []

        sss = StratifiedShuffleSplit(10, 0.25)
        for train_index, test_index in sss.get_n_splits(X,y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            for name, model in models:
                mode.fit(X_train,y_train)
                scores[name].append(metrics.accuracy_score(y_true=y_train,y_pred=model.predict(X_test)))
        
        #Choose http://blog.minitab.com/blog/adventures-in-statistics-2/how-to-choose-the-best-regression-model
        index = None
        for name,model in models:
            min = 10000
            if scores[name][-1] < min:
                min = scores[name][-1]
                index = name
        _model = models[index]

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
        labels = model_.labels_

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




    #if type == 'kmeans' or type == 'polynomial':
        #    model_ = cluster.KMeans(ini_params['n_clusters'],
        #                                            ini_params['init'],
        #                                            ini_params['n_init'],
        #                                            ini_params['max_iter'],
        #                                            ini_params['tol'],
        #                                            ini_params['precompute_distances'],
        #                                            ini_params['verbose'],
        #                                            ini_params['random_state'],
        #                                            ini_params['copy_x'],
        #                                            ini_params['n_jobs'],
        #                                            ini_params['algorithm']) 
        #elif type == 'affinity':
        #    model_ = cluster.AffinityPropagation(ini_params['damping'],
        #                                             ini_params['max_iter'],
        #                                             ini_params['convergence_iter'],
        #                                             ini_params['copy'],
        #                                             ini_params['preference'],
        #                                             ini_params['affinity'],
        #                                             ini_params['verbose'])
        #elif type == 'mean_shift':
        #    model_ = cluster.MeanShift(ini_params['bandwidth'],
        #                                               ini_params['seeds'],
        #                                               ini_params['bin_seeding'],
        #                                               ini_params['min_bin_freq'],
        #                                               ini_params['cluster_all'],
        #                                               ini_params['n_jobs'])
        #elif type == 'spectral':
        #    model_ = cluster.SpectralClustering(ini_params['n_clusters'],
        #                                     ini_params['eigen_solver'],
        #                                     ini_params['random_state'],
        #                                     ini_params['n_init'],
        #                                     ini_params['gamma'],
        #                                     ini_params['affinity'],
        #                                     ini_params['n_neighbors'],
        #                                     ini_params['eigen_tol'],
        #                                     ini_params['assign_labels'],
        #                                     ini_params['degree'],
        #                                     ini_params['coef0'],
        #                                     ini_params['kernel_params'],
        #                                     ini_params['n_jobs']) 
        #elif type == 'agglomerative':
        #    model_ = cluster.AgglomerativeClustering(ini_params['n_clusters'],
        #                                        ini_params['affinity'],
        #                                        ini_params['memory'],
        #                                        ini_params['connectivity'],
        #                                        ini_params['compute_full_tree'],
        #                                        ini_params['linkage'],
        #                                        ini_params['pooling_func'])
        #elif type == 'dbscan':
        #    model_ = cluster.DBSCAN(ini_params['eps'],
        #                                        ini_params['min_samples'],
        #                                        ini_params['metric'],
        #                                        ini_params['metric_params'],
        #                                        ini_params['algorithm'],
        #                                        ini_params['leaf_size'],
        #                                        ini_params['n_jobs'])
        #elif type == 'birch':
        #    model_ = cluster.Birch(ini_params['threshold'],
        #                                            ini_params['branching_factor'],
        #                                            ini_params['n_clusters'],
        #                                            ini_params['compute_labels'])
