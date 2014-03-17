import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, datasets
from sklearn.utils import shuffle
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
from sklearn import preprocessing

import pickle

random_state = np.random.RandomState(0)



f = open('mining_data/train.csv')
t = open('mining_data/target.csv')
f.readline()
t.readline()
data = np.loadtxt(f, delimiter=',')
target = np.loadtxt(t, delimiter=',')



X = data
X_scaled = preprocessing.scale(X)

y = target[:, 1:].ravel()

clf = ExtraTreesClassifier()
clf.fit(X_scaled, y)
d = open('dimension_reduction.txt', 'wb')
pickle.dump(clf, d)


d = open('dimension_reduction.txt', 'rb')
clf = pickle.load(d)

X_new = clf.transform(X)
print X_new.shape


X_train, X_test, y_train, y_test = cross_validation.train_test_split(
	X_new, y, test_size=0.3, random_state=0)

svmm = svm.SVC(kernel='linear', probability=True, random_state=0)
svmm.fit(X_train, y_train)

 


 print svmm.score(X_test, y_test)

#f = open('first_model.txt', 'rb')
#svm2 = pickle.load(f)

#svm2.predict(X_scaled)

pickle.dump(svmm, f)















# fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
# roc_auc = auc(fpr,tpr)

# print("Area under the ROC curve : %f" % roc_auc)


# pl.clf()
# pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
# pl.plot([0, 1], [0, 1], 'k--')
# pl.xlim([0.0, 1.0])
# pl.ylim([0.0, 1.0])
# pl.xlabel('False Positive Rate')
# pl.ylabel('True Positive Rate')
# pl.title('Receiver operating characteristic example')
# pl.legend(loc="lower right")
# pl.show()


# with open("epl.dot", "w") as f:
# 	f = tree.export_graphviz(clf, out_file=f)
