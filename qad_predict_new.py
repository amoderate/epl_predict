import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn import svm, datasets
from sklearn.utils import shuffle
import csv

import pandas as pd

#score new data - first load and transform...seriosly, don't be lazy, make this shit a class already 

f = open('mining_data/score_train.csv')
a =open('mining_data/score_data.csv')

f.readline()
a.readline()


reader= csv.reader(a)

features = []
for row in reader:
	features.append(row)



data = np.loadtxt(f, delimiter=',')


#print full_feature



X = data
X_scaled = preprocessing.scale(X)



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

header = ['date', 'home_team', 'away_team', 'predict_home', 'predict_away']

c = csv.writer(open('mining_data/scored_matches.csv', 'wb'))

c.writerow(header)
for row in scores_and_features:
	c.writerow(row)