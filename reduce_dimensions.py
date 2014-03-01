import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
import pickle


#preprocess data


#Load  data and scale

f = open('mining_data/train.csv')
t = open('mining_data/target.csv')
f.readline()
t.readline()
data = np.loadtxt(f, delimiter=',')
target = np.loadtxt(t, delimiter=',')


X = data
X_scaled = preprocessing.scale(X)


#transform the target as necessary
y = target[:, 1:].ravel()


#use a simple tree classifire to identify important features
clf = ExtraTreesClassifier()
clf.fit(X_scaled, y)

#save the model in a a presistent file to transform new data
d = open('dimension_reduction.txt', 'wb')
pickle.dump(clf, d)