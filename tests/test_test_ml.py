import numpy as np
import pytest
from materialscoord.ml import CoordinationClassifier

def test_classifier_init():
    clf = CoordinationClassifier(hidden_layer_sizes=(8,))
    assert clf.clf.hidden_layer_sizes == (8,)

def test_classifier_fit_predict():
    clf = CoordinationClassifier(hidden_layer_sizes=(4,))
    
    # Create synthetic data for 4 classes
    # 4 features, 4 classes
    X_train = np.array([
        [1, 0, 0, 0], [1, 0.1, 0, 0],  # Class T-4
        [0, 1, 0, 0], [0, 0.9, 0, 0],  # Class SP-4
        [0, 0, 1, 0], [0, 0, 0.8, 0],  # Class SPY-4
        [0, 0, 0, 1], [0, 0, 0, 1.1]   # Class SS-4
    ])
    y_train = ['T-4', 'T-4', 'SP-4', 'SP-4', 'SPY-4', 'SPY-4', 'SS-4', 'SS-4']
    
    clf.train(X_train, y_train)
    
    # Test prediction
    X_test = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
    predictions, probs = clf.predict(X_test)
    
    assert len(predictions) == 2
    assert predictions[0] == 'T-4'
    assert predictions[1] == 'SP-4'
    assert probs.shape == (2, 4)
