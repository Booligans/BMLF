
from sklearn.linear_model import ElasticNetCV

class SimplifiedElasticNet(ElasticNetCV):
    def __init__(self, l1_ratio=0.5, fast = False, seed=0):
        super(SimplifiedElasticNet, self).__init__(l1_ratio=l1_ratio, eps=0.001, n_alphas=100, alphas= None, fit_intercept=True, normalize=False, precompute='auto', max_iter=1000, tol=0.0001 if not fast else 0.0005, cv=None, copy_X=True, verbose=0, n_jobs=1, positive=False, random_state=seed, selection= 'random' if random else 'cyclic')