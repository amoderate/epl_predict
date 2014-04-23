#import numpy as np
import csv
import pandas as pd
import numpy as np



def iter_over_groups(data, group,features, key):
	row_num = 0	
	for x in group:

		if row_num == 0:
			data_1 = data[data[key]==x]
			for i in features:

				data_1['avg_10' + i.lower() + '_'+ key[0].lower()] = pd.rolling_mean(data_1[i], 7).shift(+1)
				data_1['sum_15' + i.lower() + '_'+ key[0].lower()] = pd.rolling_mean(data_1[i], 10).shift(+1)
				data_1['avg_3' + i.lower() + '_'+ key[0].lower()] = pd.rolling_mean(data_1[i], 3).shift(+1)
				data_1['expand' + i.lower() + '_'+ key[0].lower()] = pd.expanding_mean(data_1[i]).shift(+1)	
				data_1['expand_sum' + i.lower() + '_'+ key[0].lower()] = pd.expanding_sum(data_1[i]).shift(+1)		

		else:
			data_2 = data[data[key]==x]
			for i in features:
				data_2['avg_10' + i.lower() + '_' + key[0].lower()] = pd.rolling_mean(data_2[i], 7).shift(+1)
				data_2['sum_15' + i.lower() + '_' + key[0].lower()] = pd.rolling_mean(data_2[i], 10).shift(+1)
				data_2['avg_3' + i.lower() + '_' + key[0].lower()] = pd.rolling_mean(data_2[i],3).shift(+1)
				data_2['expand' + i.lower() + '_'+ key[0].lower()] = pd.expanding_mean(data_1[i]).shift(+1)
				data_2['expand_sum' + i.lower() + '_'+ key[0].lower()] = pd.expanding_sum(data_1[i]).shift(+1)
				


			data_1 = data_1.append(data_2, ignore_index = True)

		row_num += 1
	return data_1

def combine_data(data, target, teams_h, teams_a, refined_features):
	feature_h =  iter_over_groups(data, teams_h, refined_features, 'HomeTeam')

	for name in refined_features:
		del feature_h[name]


	feature_a =  iter_over_groups(data, teams_a, refined_features, 'AwayTeam')

	for name in refined_features:
		del feature_a[name]
	del feature_a['AwayTeam']

	#print feature_h

	combined = pd.merge(feature_h, feature_a, on=['Date', 'HomeTeam'], how='outer')
	combined_filled = combined.fillna(combined.mean())

	combined_target = pd.merge(combined_filled,target, on=['Date', 'HomeTeam'], how='outer')

	return combined_target
def main():
	list_of_years = ['1314', '1213', '1112', '1011','0910','0809', '0708', '0607','0506', '0405', '0304']
	row_num = 0
	for year in list_of_years:
		f = open('processed_data/processed_epl_data_'+year+'.csv')
		t = open('processed_data/processed_epl_data_'+year+'_target.csv')
		
		features = csv.reader(f)


		rownum = 0
		header = []
		for row in features:
			if rownum == 0:
				header = row
			rownum += 1


		refined_features = header[3:17]

		#print refined_features

		data = pd.read_csv('processed_data/processed_epl_data_'+year+'.csv', parse_dates=['Date'], dayfirst=True, keep_date_col = True)
		target = pd.read_csv('processed_data/processed_epl_data_'+year+'_target.csv', parse_dates=['Date'], dayfirst=True, keep_date_col = True)
		
		#merge on the  2013/2014 fixture list
		if year == list_of_years[0]:
			fixtures = pd.read_csv('processed_data/fixtures.csv', parse_dates=['Date'], dayfirst=True, keep_date_col = True)
			fixtures_cut = fixtures[fixtures.Date  > '2014-03-15']
			

			data_3 = pd.merge(data, fixtures_cut, on=['Date', 'HomeTeam', 'AwayTeam'], how='outer')

			#print len(fixtures_cut), len(data), len(data_3)

			#print data_3

			target_3 = pd.merge(target, fixtures_cut, on=['Date', 'HomeTeam'], how='outer')
			del target_3['AwayTeam']
		else:
			data_3 = data
			target_3 = target

		
		

		#combined_3_filled = data_3.fillna(data_3.mean())


		
		
		teams_h = data['HomeTeam'].unique()
		teams_a = data['AwayTeam'].unique()

		if row_num == 0:
			data_1 = combine_data(data_3, target_3, teams_h, teams_a, refined_features)
		else:
			data_2 = combine_data(data_3, target_3, teams_h, teams_a, refined_features)

			data_1 = data_1.append(data_2, ignore_index = True)


		row_num += 1
	
	

	#print combined_3_filled.sort(ascending = False)

	#P W @ H : 1899 / (1899 + 1115)  = .63
	#P L @ H : 1 - .63 = .37

	data_2 = data_1[data_1['FTR'] != 0]

	#create a match ranking
	def goals(row):

		val = 0
		if  abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) > 0  and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .2:
			val = 1
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .2 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .3:
			val = 2
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .3 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .4:
			val = 3
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .4 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .5:
			val = 4
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .5 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .6:
			val = 5
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .6 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .7:
			val = 6
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .7 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .8:
			val = 7
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .8 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .9:
			val = 8
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= .9 and abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) < .10:
			val = 9
		elif abs(row['avg_3fthg_h'] - row['avg_3ftag_a']) >= 1.0:
			val = 10
	
		return val

	def goal_ratio_h(row):
		if abs(row['sum_15fthg_h']) == 0 or abs(row['sum_15ftag_a']) == 0:
			val = 0
		else:
			val = abs(row['sum_15fthg_h']) / abs(row['sum_15ftag_a'])

		return val
	def goal_ratio_a(row):
		if abs(row['sum_15fthg_a']) == 0 or abs(row['sum_15fthg_a']) == 0:
			val = 0
		else:
			val = abs(row['sum_15fthg_a']) / abs(row['sum_15fthg_a'])

		return val

	def exp_goals_dif(row):
		return abs(row['expandfthg_h'] - row['expandftag_a'])



	def exp_away_goals_dif(row):
		return abs(row['expandftag_h'] - row['expandftag_a'])


	def exp_ftr_dif(row):
		if abs(row['expand_sumftr_h']) == 0 or abs(row['expand_sumftr_a']) == 0:
			val = 0
		else:
			val = abs(row['expand_sumftr_h'] / row['expand_sumftr_a'])
		return val
	
	def avg10_goals_dif(row):
		if abs(row['avg_10fthg_h']) == 0 or abs(row['avg_10ftag_h']) == 0:
			val = 0
		else:
			val = abs(row['avg_10fthg_h'] / row['avg_10ftag_h'])
		return val

	def avg10_away_goals_dif(row):
		if abs(row['avg_10ftag_h']) == 0 or abs(row['avg_10fthg_a']) == 0:
			val = 0
		else:
			val = abs(row['avg_10fthg_h'] / row['avg_10fthg_a'])
		return val

	def avg10_home_goals_dif(row):
		if abs(row['avg_10fthg_h']) == 0 or abs(row['avg_10ftag_a']) == 0:
			val = 0
		else:
			val = abs(row['avg_10fthg_h'] / row['avg_10ftag_a'])
		return val


	def avg3_goals_dif(row):
		if abs(row['avg_3fthg_h']) == 0 or abs(row['avg_3ftag_h']) == 0:
			val = 0
		else:
			val = abs(row['avg_3fthg_h'] / row['avg_3ftag_h'])
		return val

	def avg3_away_goals_dif(row):
		if abs(row['avg_3ftag_h']) == 0 or abs(row['avg_3fthg_a']) == 0:
			val = 0
		else:
			val = abs(row['avg_3fthg_h'] / row['avg_3fthg_a'])
		return val

	def avg3_home_goals_dif(row):
		if abs(row['avg_3fthg_h']) == 0 or abs(row['avg_3ftag_a']) == 0:
			val = 0
		else:
			val = abs(row['avg_3fthg_h'] / row['avg_3ftag_a'])
		return val


	#data_2['goals_compare'] = data_2.apply(goals, axis=1)
	#data_2['goals_dif'] = data_2.apply(exp_goals_dif, axis=1)
	#data_2['away_goals_dif'] = data_2.apply(exp_away_goals_dif, axis=1)
	#data_2['exp_home_goals_diff'] = data_2.apply(exp_home_goals_dif, axis=1)
	
	#data_2['avg3_goals_compare'] = data_2.apply(avg3_goals_dif, axis=1)



	#data_2['avg3_home_goals_compare'] = data_2.apply(avg3_home_goals_dif, axis=1)
	#data_2['exp_ftr_dif_compare'] = data_2.apply(exp_ftr_dif, axis=1)

	data_2['avg3_away_goals_compare'] = data_2.apply(avg3_away_goals_dif, axis=1)

	data_2['avg3_home_goals_compare'] = data_2.apply(avg3_home_goals_dif, axis=1)

	data_2['sum15_home_goals_compare'] = data_2.apply(goal_ratio_h, axis=1)
	data_2['sum15_away_goals_compare'] = data_2.apply(goal_ratio_a, axis=1)

	data_2['avg10_away_goals_compare'] = data_2.apply(avg10_away_goals_dif, axis=1)

	data_2['avg10_home_goals_compare'] = data_2.apply(avg10_home_goals_dif, axis=1)


	#explore new match ranking system

	explore_bays = data_2.groupby(['FTR']).agg({'avg3_home_goals_compare': np.mean})

	print explore_bays
	
	data_train = data_2[data_2.Date <= '2014-03-15']

	#split out data to be scores from training data
	score_data_s1 = data_2[data_2.Date > '2014-03-15']
	score_data = score_data_s1.fillna(0)

	#training data
	train = data_train
	target = data_train[['FTR']]

	

	score_data_sorted = score_data.sort(columns='Date')
	score_data_sorted.to_csv('mining_data/score_data.csv')

	#print train.sort(ascending=False)

	train.to_csv('mining_data/full_feature.csv')
	#print full_feature
	
	del train['HomeTeam']
	del train['FTR']
	del train['Date']
	del train['AwayTeam']
	del train['avg_3hthg_h']
	del train['avg_10htag_h']
	del train['sum_15htag_h']
	del train['avg_3htag_h']
	del train['avg_10hs_h']
	del train['sum_15hs_h']
	del train['avg_3hs_h']
	del train['avg_10as_h']
	del train['sum_15as_h']
	del train['avg_3as_h']
	del train['avg_10hst_h']
	del train['sum_15hst_h']
	del train['avg_3hst_h']
	del train['avg_10ast_h']
	del train['sum_15ast_h']
	del train['avg_3ast_h']
	del train['avg_10hf_h']
	del train['sum_15hf_h']
	del train['avg_3hf_h']
	del train['avg_10af_h']
	del train['sum_15af_h']
	del train['avg_3af_h']
	del train['avg_10hc_h']
	del train['sum_15hc_h']
	del train['avg_3hc_h']
	del train['avg_10ac_h']
	del train['sum_15ac_h']
	del train['avg_3ac_h']
	del train['avg_10fthg_a']
	del train['sum_15fthg_a']
	del train['avg_3fthg_a']
	del train['avg_10ftag_a']
	del train['sum_15ftag_a']
	del train['avg_3ftag_a']
	del train['avg_10hthg_a']
	del train['sum_15hthg_a']
	del train['avg_3hthg_a']
	del train['avg_10htag_a']
	del train['sum_15htag_a']
	del train['avg_3htag_a']
	del train['avg_10hs_a']
	del train['sum_15hs_a']
	del train['avg_3hs_a']
	del train['avg_10as_a']
	del train['sum_15as_a']
	del train['avg_3as_a']
	del train['avg_10hst_a']
	del train['sum_15hst_a']
	del train['avg_3hst_a']
	del train['avg_10ast_a']
	del train['sum_15ast_a']
	del train['avg_3ast_a']
	del train['avg_10hf_a']
	del train['sum_15hf_a']
	del train['avg_3hf_a']
	del train['avg_10af_a']
	del train['sum_15af_a']
	del train['avg_3af_a']
	del train['avg_10hc_a']
	del train['sum_15hc_a']
	del train['avg_3hc_a']
	del train['avg_10ac_a']
	del train['sum_15ac_a']
	del train['avg_3ac_a']


	
	del score_data_sorted['avg_3hthg_h']
	del score_data_sorted['avg_10htag_h']
	del score_data_sorted['sum_15htag_h']
	del score_data_sorted['avg_3htag_h']
	del score_data_sorted['avg_10hs_h']
	del score_data_sorted['sum_15hs_h']
	del score_data_sorted['avg_3hs_h']
	del score_data_sorted['avg_10as_h']
	del score_data_sorted['sum_15as_h']
	del score_data_sorted['avg_3as_h']
	del score_data_sorted['avg_10hst_h']
	del score_data_sorted['sum_15hst_h']
	del score_data_sorted['avg_3hst_h']
	del score_data_sorted['avg_10ast_h']
	del score_data_sorted['sum_15ast_h']
	del score_data_sorted['avg_3ast_h']
	del score_data_sorted['avg_10hf_h']
	del score_data_sorted['sum_15hf_h']
	del score_data_sorted['avg_3hf_h']
	del score_data_sorted['avg_10af_h']
	del score_data_sorted['sum_15af_h']
	del score_data_sorted['avg_3af_h']
	del score_data_sorted['avg_10hc_h']
	del score_data_sorted['sum_15hc_h']
	del score_data_sorted['avg_3hc_h']
	del score_data_sorted['avg_10ac_h']
	del score_data_sorted['sum_15ac_h']
	del score_data_sorted['avg_3ac_h']
	del score_data_sorted['avg_10fthg_a']
	del score_data_sorted['sum_15fthg_a']
	del score_data_sorted['avg_3fthg_a']
	del score_data_sorted['avg_10ftag_a']
	del score_data_sorted['sum_15ftag_a']
	del score_data_sorted['avg_3ftag_a']
	del score_data_sorted['avg_10hthg_a']
	del score_data_sorted['sum_15hthg_a']
	del score_data_sorted['avg_3hthg_a']
	del score_data_sorted['avg_10htag_a']
	del score_data_sorted['sum_15htag_a']
	del score_data_sorted['avg_3htag_a']
	del score_data_sorted['avg_10hs_a']
	del score_data_sorted['sum_15hs_a']
	del score_data_sorted['avg_3hs_a']
	del score_data_sorted['avg_10as_a']
	del score_data_sorted['sum_15as_a']
	del score_data_sorted['avg_3as_a']
	del score_data_sorted['avg_10hst_a']
	del score_data_sorted['sum_15hst_a']
	del score_data_sorted['avg_3hst_a']
	del score_data_sorted['avg_10ast_a']
	del score_data_sorted['sum_15ast_a']
	del score_data_sorted['avg_3ast_a']
	del score_data_sorted['avg_10hf_a']
	del score_data_sorted['sum_15hf_a']
	del score_data_sorted['avg_3hf_a']
	del score_data_sorted['avg_10af_a']
	del score_data_sorted['sum_15af_a']
	del score_data_sorted['avg_3af_a']
	del score_data_sorted['avg_10hc_a']
	del score_data_sorted['sum_15hc_a']
	del score_data_sorted['avg_3hc_a']
	del score_data_sorted['avg_10ac_a']
	del score_data_sorted['sum_15ac_a']
	del score_data_sorted['avg_3ac_a']


	del score_data_sorted['HomeTeam']
	del score_data_sorted['FTR']
	del score_data_sorted['Date']
	del score_data_sorted['AwayTeam']

	
	score_data_sorted.to_csv('mining_data/score_train.csv')

	train.to_csv('mining_data/train.csv')

	target.to_csv('mining_data/target.csv')

	#print score_data_sorted






if __name__ =="__main__":
	main()

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



