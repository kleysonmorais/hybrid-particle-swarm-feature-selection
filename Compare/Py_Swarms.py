from sklearn.datasets import make_classification
from sklearn import linear_model    
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Import modules
import numpy as np
import seaborn as sns
import pandas as pd

# Import PySwarms
import pyswarms as ps

# X, y = make_classification(n_samples=100, n_features=13, n_classes=3,
#                            n_informative=4, n_redundant=1, n_repeated=2,
#                            random_state=1)

nome = "wine"
nomeBase = "../datasets/"+nome+"/"+nome+".csv"
data = pd.read_csv(nomeBase)
y = data.classe
list = ['classe']
X = data.drop(list, axis=1)

X = np.asarray(X)
print(X.shape)
# Create an instance of the classifier
# classifier = linear_model.LogisticRegression()
classificador = KNeighborsClassifier()

# x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# X = x_train

# Define objective function
def f_per_particle(m, alpha):
    """Computes for the objective function per particle

    Inputs
    ------
    m : numpy.ndarray
        Binary mask that can be obtained from BinaryPSO, will
        be used to mask features.
    alpha: float (default is 0.5)
        Constant weight for trading-off classifier performance
        and number of features

    Returns
    -------
    numpy.ndarray
        Computed objective function
    """
    total_features = 13
    # Get the subset of the features from the binary mask
    if np.count_nonzero(m) == 0:
        X_subset = X
    else:
        X_subset = X[:,m==1]

    classificador.fit(X_subset, y)
    predict = classificador.predict(X_subset)
    return accuracy_score(y, predict)

    # Perform classification and store performance in P
    # classifier.fit(X_subset, y)
    # P = (classifier.predict(X_subset) == y).mean()
    # Compute for the objective function
    # j = (alpha * (1.0 - P)
    #     + (1.0 - alpha) * (1 - (X_subset.shape[1] / total_features)))

    # return j

def f(x, alpha=0.88):
    """Higher-level method to do classification in the
    whole swarm.

    Inputs
    ------
    x: numpy.ndarray of shape (n_particles, dimensions)
        The swarm that will perform the search

    Returns
    -------
    numpy.ndarray of shape (n_particles, )
        The computed loss for each particle
    """
    n_particles = x.shape[0]
    j = [f_per_particle(x[i], alpha) for i in range(n_particles)]
    return np.array(j)

# Initialize swarm, arbitrary
options = {'c1': 0.5, 'c2': 0.5, 'w':0.9, 'k': 30, 'p':2}

# Call instance of PSO
dimensions = 13 # dimensions should be the number of features
# optimizer.reset()
optimizer = ps.discrete.BinaryPSO(n_particles=100, dimensions=dimensions, options=options)

# Perform optimization
cost, pos = optimizer.optimize(f, print_step=10, iters=100, verbose=2)
print(pos)

classificador = KNeighborsClassifier()
X_selected_features = X[:,pos==1]  # subset
classificador = classificador.fit(X_selected_features, y)
predict = classificador.predict(X_selected_features)

acuracia = accuracy_score(y, predict)
print('Acurácia: ', acuracia)

# Create two instances of LogisticRegression
# classfier = linear_model.LogisticRegression()

# # Get the selected features from the final positions
# X_selected_features = X[:,pos==1]  # subset

# # Perform classification and store performance in P
# c1 = classifier.fit(X_selected_features, y)

# # Compute performance
# subset_performance = (c1.predict(X_selected_features) == y).mean()


# print('Subset performance: %.3f' % (subset_performance))