import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn import svm, datasets
from sklearn.utils import shuffle

#load data and transform (must mach the transform done in pre-processing, 
#	consider making this a feature)

f = open('mining_data/train.csv')
t = open('mining_data/target.csv')
f.readline()
t.readline()
data = np.loadtxt(f, delimiter=',')
target = np.loadtxt(t, delimiter=',')



X = data
X_scaled = preprocessing.scale(X)

y = target[:, 1:].ravel()


#first load the preprocessing model

d = open('dimension_reduction.txt', 'rb')
clf = pickle.load(d)

#Transform the feature vectos
X_new = clf.transform(X)

#Create train/test data sets
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
	X_new, y, test_size=0.3, random_state=0)

#build a simple svm model (takes about an hour to train on 3k recrods and 13 features)
#note - buy a faster computer, or rent some ec2 processing time if dealing with more data
svmm = svm.SVC(kernel='linear', probability=True, random_state=0)
svmm.fit(X_train, y_train)


#score new data - need to write a Roc function to evaulate the model performance....
print svmm.score(X_test, y_test)

#save the model 

m = open('qad_model.txt', 'wb')

pickle.dump(svmm, m)
