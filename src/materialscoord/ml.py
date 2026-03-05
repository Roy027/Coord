from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import numpy as np
import pandas as pd

class CoordinationClassifier:
    """
    Neural network classifier for 4-coordinate environments.
    """
    def __init__(self, hidden_layer_sizes=(16,), max_iter=10000):
        self.clf = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            max_iter=max_iter,
            solver='lbfgs',
            alpha=0.01,
            random_state=1,
            activation="logistic"
        )
        self.scaler = preprocessing.MinMaxScaler()
        self.label_map = {0: 'T-4', 1: 'SP-4', 2: 'SPY-4', 3: 'SS-4'}
        self.inv_label_map = {v: k for k, v in self.label_map.items()}

    def _prepare_targets(self, labels):
        """
        Convert string labels to one-hot encoding.
        """
        targets = np.zeros((len(labels), 4))
        for i, label in enumerate(labels):
            if label in self.inv_label_map:
                targets[i, self.inv_label_map[label]] = 1
        return targets

    def train(self, X_train, y_train_labels):
        """
        Train the model.
        
        Args:
            X_train: Feature matrix.
            y_train_labels: List of string labels ('T-4', etc.)
        """
        X_scaled = self.scaler.fit_transform(X_train)
        y_train = self._prepare_targets(y_train_labels)
        self.clf.fit(X_scaled, y_train)

    def predict(self, X):
        """
        Predict geometry labels.
        """
        X_scaled = self.scaler.transform(X)
        probs = self.clf.predict_proba(X_scaled)
        
        predictions = []
        for prob in probs:
            idx = np.argmax(prob)
            predictions.append(self.label_map[idx])
        return predictions, probs
