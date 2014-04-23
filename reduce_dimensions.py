import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.decomposition import FastICA
import pickle


#preprocess data
rng = np.random.RandomState(42)

#Load  data and scale

f = open('mining_data/train.csv')
t = open('mining_data/target.csv')
f.readline()
t.readline()
data = np.loadtxt(f, delimiter=',')
target = np.loadtxt(t, delimiter=',')

#print data

X = data
X_scaled = X


#transform the target as necessary
y = target[:, 1:].ravel()


ica = FastICA(random_state = rng)

ica.fit(X_scaled)
X_new = ica.transform(X_scaled)

c1 = open('ica_s1.txt', 'wb')

pickle.dump(ica, c1)

# ica_1 = FastICA(random_state = rng)
# ica_1.fit(X_ica)	

# X_ica_1 = ica_1.transform(X_ica)

# print X_ica_1

# c2 = open('ica_s2.txt', 'wb')

# pickle.dump(ica, c2)






#use a simple tree classifire to identify important features
clf = ExtraTreesClassifier()
clf.fit(X_scaled, y)

X_new = clf.transform(X_scaled)
print X_new.shape

#save the model in a a presistent file to transform new data
d = open('dimension_reduction.txt', 'wb')
pickle.dump(clf, d)





