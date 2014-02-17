#import numpy as np
import csv
import pandas as pd

f = open('processed_epl_data.csv')
t = open('processed_epl_data_target.csv')
# features = csv.reader(f)
# target = csv.reader(t)

features = csv.reader(f)
rownum = 0
header = []
for row in features:
	if rownum == 0:
		header = row
	rownum += 1

#print [(x,i) for (x,i) in enumerate(header)]


refined_features = header[3:17]

data = pd.read_csv('processed_epl_data.csv', parse_dates=['Date'], dayfirst=True, keep_date_col = True)

teams = data['HomeTeam'].unique()

def iter_over_groups(data, group,features, key):
	row_num = 0	
	for x in group:

		if row_num == 0:
			data_1 = data[data[key]==x]
			for i in features:
				data_1['avg_' + i.lower() + '_'+ key[0].lower()] = pd.rolling_mean(data_1[i], 3).shift(+1)

		else:
			data_2 = data[data[key]==x]
			for i in features:
				data_2['avg_' + i.lower() + '_' + key[0].lower()] = pd.rolling_mean(data_2[i], 3).shift(+1)


			data_1 = data_1.append(data_2, ignore_index = True)

		row_num += 1
	return data_1


feature_h =  iter_over_groups(data, teams, refined_features, 'HomeTeam')

for name in refined_features:
	del feature_h[name]


feature_a =  iter_over_groups(data, teams, refined_features, 'AwayTeam')

for name in refined_features:
	del feature_a[name]
del feature_a['AwayTeam']

#print feature_h

combined = pd.merge(feature_h, feature_a, on=['Date', 'HomeTeam'], how='outer')
print combined.fillna(combined.mean())

# for name, group in data.groupby(['HomeTeam']):
# 	build_list = []
# 	build_list.extend(group['HomeTeam'])
# 	build_list.extend(pd.rolling_mean(group['FTHG'], 3).shift(-1))
# 	temp_list.append(build_list)



#print temp_list
#print new_dict



#features_list = [row for row in features]
#target_list = [row for row in target]
#print features_list

#X =  np.array(features_list, dtype='f')
#y =  np.array(target_list)

#features need to be calculated first create a measure of each teams performance

#print X

#print np.mean(X, axis=0)



