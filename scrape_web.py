import urllib2
import csv
import numpy as np

def replace_value(value):
	#print value
	aux = 0
	if value == 'H':
		aux = 1
	elif value == 'A':
		aux = 2
	elif value == 'D':
		aux = 0
	return str(aux)
#Open dataset


def extract_epl_features(data, year):
#extract useful features
	row_num = 0
	header = []
	target_list = []
	target_header = []
	data_list = []

	if year == '1213':

		for row in data:
			row_list = []
			header_list = []
			target_header_list = []
			target_b_list = []

			if row_num == 0:
				#header.append(row)
				header_list.extend(row[1:4])
				header_list.extend(row[4:6])
				header_list.extend(row[6:7])
				header_list.extend(row[7:9])
				header_list.extend(row[10:18])
				header.append(header_list)
				target_header_list.extend(row[1:3])
				target_header_list.extend(row[6:7])
				target_header.append(target_header_list)
					
			else:
				row_list.extend(row[1:4])
				row_list.extend(row[4:6])
				row_list.extend(replace_value(row[6:7][0]))
				row_list.extend(row[7:9])
				row_list.extend(row[10:18])
				data_list.append(row_list)
				
				target_b_list.extend(row[1:3])
				target_b_list.extend(replace_value(row[6:7][0]))
				target_list.append(target_b_list)

			row_num += 1
	else:
		for row in data:
			row_list = []
			header_list = []
			target_header_list = []
			target_b_list = []
			if row_num == 0:
				#header.append(row)
				header_list.extend(row[1:4])
				header_list.extend(row[4:6])
				header_list.extend(row[6:7])
				header_list.extend(row[7:9])
				header_list.extend(row[11:19])
				header.append(header_list)

				target_header_list.extend(row[1:3])
				target_header_list.extend(row[6:7])
				target_header.append(target_header_list)
			else:
				row_list.extend(row[1:4])
				row_list.extend(row[4:6])
				row_list.extend(replace_value(row[6:7][0]))
				row_list.extend(row[7:9])
				row_list.extend(row[11:19])
				data_list.append(row_list)
				
				target_b_list.extend(row[1:3])
				target_b_list.extend(replace_value(row[6:7][0]))
				target_list.append(target_b_list)

			row_num += 1

	print [(number, item) for (number, item) in enumerate(header[0])]
	return header, data_list, target_header, target_list


#save output as csv for further processing
def write_to_file(data_out, data_in,year):
	header, data, target_header, target_list = extract_epl_features(data_in, year)
	#write features to file
	c = csv.writer(open(data_out + '.csv', "wb"))

	c.writerow(header[0])
	for row in data:
		c.writerow(row)
	#write target to file

	c = csv.writer(open(data_out +'_target.csv', "wb"))
	c.writerow(target_header[0])

	for row in target_list:
		c.writerow(row)


def main():
	list_of_years = ['1314', '1213', '1112', '1011','0910','0809', '0708', '0607','0506', '0405', '0304']

	for year in list_of_years:
		response = urllib2.urlopen('http://www.football-data.co.uk/mmz4281/'+year+'/E0.csv')
#import csv
		data_in = csv.reader(response)

#export data
		data_out = 'processed_data/processed_epl_data_' + year

		write_to_file(data_out, data_in, year)

if __name__ =="__main__":
	main()


#########################################
#Utility functions below here!

#print header[0]

# data_list = []
# for row in data:
# 	data_list.append(row)
# print data_list


#np_data = np.array(data_list)
#print np_data