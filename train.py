import numpy as np
import os

from sklearn.cross_validation import KFold, train_test_split
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.externals import joblib
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def test(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


def save_model(model, model_name):
    if not os.path.isdir('models/{}'.format(model_name)):
        os.mkdir('models/{}'.format(model_name))
    joblib.dump(model, 'models/{}/model.pkl'.format(model_name))


def down_sample(X, y, n):
    negative_index = np.where(y == 0)[0]
    positive_index = np.where(y == 1)[0]
    positive_num = sum(y == 1)
    negative_index_sample = np.random.choice(
        negative_index,
        positive_num * n,
        replace=False
    )
    sample = np.concatenate((negative_index_sample, positive_index))
    return X[sample, :], y[sample]


X = np.load('dataset/X.npy')
y = np.load('dataset/y.npy')

X, y = down_sample(X, y, 3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# Scale features
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Logistic Regression
model = LogisticRegression()
print 'Logistic Regresion = {}'.format(test(model, X_train, y_train, X_test, y_test))
save_model(model, 'logistic_regression')

# SVM
model = SVC()
print 'SVC = {}'.format(test(model, X_train, y_train, X_test, y_test))
save_model(model, 'svm')

# AdaBoost
model = AdaBoostClassifier()
print 'AdaBoost = {}'.format(test(model, X_train, y_train, X_test, y_test))
save_model(model, 'adaboost')

# Random Forest
model = RandomForestClassifier()
print 'Random Forest = {}'.format(test(model, X_train, y_train, X_test, y_test))
save_model(model, 'random_forest')
