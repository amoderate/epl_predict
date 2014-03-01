import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn import svm, datasets
from sklearn.utils import shuffle
import csv

import pandas as pd

#score new data - first load and transform...seriosly, don't be lazy, make this shit a class already 

f = open('mining_data/train.csv')
t = open('mining_data/target.csv')
a =open('mining_data/full_feature.csv')

f.readline()
t.readline()
a.readline()


reader= csv.reader(a)

features = []
for row in reader:
	features.append(row)


full_feature = np.loadtxt(a, delimiter=',')
data = np.loadtxt(f, delimiter=',')
target = np.loadtxt(t, delimiter=',')

#print full_feature



X = data
X_scaled = preprocessing.scale(X)

y = target[:, 1:].ravel()


#first load the preprocessing model

d = open('dimension_reduction.txt', 'rb')
clf = pickle.load(d)

#Transform the feature vectos
X_new = clf.transform(X)

#load the qad model

m = open('qad_model.txt', 'rb')
svmm = pickle.load(m)

#score new data!
score =  svmm.predict_proba(X_new)

score_list = [i for (i,j) in score]

scores_and_features =[]

for i in range(len(score_list)):
	aux_list = []
	aux_list.extend(features[i][1:4])
	aux_list.extend(score[i])
	scores_and_features.append(aux_list)


#print score_list, y
#print scores_and_features
def confusion(predict, actual):
	tpr =[0.0]
	fpr = [0.0]

	w = len([i for i in predict if i == 1])
	l = len([i for i in predict if i == 2])

	ranges = 0.0
	metrics = []
	
	while ranges <= 1.0:
		tp = 0.0
		fp = 0.0
		tn = 0.0
		fn = 0.0

		hit = 0.0
		
		for i in range(len(predict)):
			confusion = []
			tp = 0.0
			fp = 0.0
			tn = 0.0
			fn = 0.0


			hit = 0.0

			if predict[i] >= ranges:
				hit = 1.0

			if hit == 1.0 and actual[i] == 1:
				tp = 1.0
			if hit == 1.0 and actual[i] == 2:
				fp = 1.0
			if hit == 0.0 and actual[i] == 2:
				tn = 1.0
			if hit == 0.0 and actual[i] == 1:
				fn = 1.0

			confusion = [ranges, hit, predict[i], actual[i], tp,fp,tn,fn]
			metrics.append(confusion)

		ranges += .02



	return metrics


check = confusion(score_list, y)

def rates(confusion_data, header):
	
	# new_list = []
	# for i in range(len(scores_and_features)):
	# 	aux_list = []
	# 	aux_list.extend(scores_and_features[i])
	# 	aux_list.extend(confusion_data[i])
	# 	new_list.append(aux_list)

	#print new_list
		
	df1 = pd.DataFrame(confusion_data, columns = header)
	df2 = df1.groupby(['ranges'], sort=True).sum()
	
	fpr_tpr = df2

	fpr_tpr['tpr'] = df2['tp'] / (df2['tp'] + df2['fn'])
	fpr_tpr['fpr'] = df2['fp'] / (df2['fp'] + df2['tn'])
	

	#fpr_tpr.plot(x='fpr', y='tpr')
	return fpr_tpr

labels_f = ['date', 'home_team', 'away_team', 'score_for', 'score_against', 'ranges', 'hit', 'predict', 'actual', 'tp', 'fp', 'tn', 'fn']
labels_m = ['ranges', 'hit', 'predict', 'actual', 'tp', 'fp', 'tn', 'fn']



roc = rates(check, labels_m)

print roc
roc.to_csv('mining_data/roc.csv')




