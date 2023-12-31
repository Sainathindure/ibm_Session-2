import warnings
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn import datasets
from sklearn.exceptions import ConvergenceWarning

# Different learning rate schedules and momentum parameters
params = [
    {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': 0.9, 'learning_rate_init': 0.2},
    {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': 0.9, 'nesterovs_momentum': False, 'learning_rate_init': 0.2},
    {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': 0.9, 'nesterovs_momentum': True, 'learning_rate_init': 0.2},
    {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': 0.9, 'learning_rate_init': 0.2},
    {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': 0.9, 'nesterovs_momentum': True, 'learning_rate_init': 0.2},
    {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': 0.9, 'nesterovs_momentum': False, 'learning_rate_init': 0.2},
    {'solver': 'adam', 'learning_rate_init': 0.01}
]

labels = ["constant learning-rate", "constant with momentum", "constant with Nesterov's momentum",
          "inv-scaling learning-rate", "inv-scaling with Nesterov's momentum", "inv-scaling with momentum", "adam"]

plot_args = [
    {'c': 'red', 'linestyle': '-'},
    {'c': 'green', 'linestyle': '-'},
    {'c': 'blue', 'linestyle': '-'},
    {'c': 'red', 'linestyle': '--'},
    {'c': 'green', 'linestyle': '--'},
    {'c': 'blue', 'linestyle': '--'},
    {'c': 'black', 'linestyle': '-'}
]

def plot_on_dataset(X, y, ax, name):
    print("\nlearning on dataset %s" % name)
    ax.set_title(name)
    
    X = MinMaxScaler().fit_transform(X)
    mlps = []
    
    max_iter = 15 if name == "digits" else 400
    
    for label, param, args in zip(labels, params, plot_args):
        print("training: %s" % label)
        mlp = MLPClassifier(random_state=0, max_iter=max_iter, **param)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ConvergenceWarning, module="sklearn")
            mlp.fit(X, y)
        
        mlps.append(mlp)
        print("Training set score: %f" % mlp.score(X, y))
        print("Training set loss: %f" % mlp.loss_)
        ax.plot(mlp.loss_curve_, label=label, **args)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Load / generate some toy datasets
iris = datasets.load_iris()
X_digits, y_digits = datasets.load_digits(return_X_y=True)
data_sets = [
    (iris.data, iris.target),
    (X_digits, y_digits),
    datasets.make_circles(noise=0.2, factor=0.5, random_state=1),
    datasets.make_moons(noise=0.3, random_state=0)
]

for ax, data, name in zip(axes.ravel(), data_sets, ['iris', 'digits', 'circles', 'moons']):
    plot_on_dataset(*data, ax=ax, name=name)

fig.legend(ax.get_lines(), labels, ncol=3, loc="upper center")
plt.show()
