from bs4 import BeautifulSoup
import urllib2
import csv
import pandas as pd

#first scrape the site for the fixtures - date, home team and away team
response = urllib2.urlopen('http://www.theguardian.com/football/2013/jun/19/premier-league-2013-2014-fixtures')


soup = BeautifulSoup(response.read())

table = soup.find('table')


rows = table.findAll('tr')

#print rows

epl_fixtures =[]

for row in rows:
	cells = row.findAll('td')
	if len(cells) == 3:
		aux = []
		date = cells[0].find(text=True).string.strip()
		home = cells[1].find(text=True).string.strip()
		home_reg = home.replace('Manchester', 'Man')
		home_reg = home_reg.replace('Newcastle United', 'Newcastle')
		home_reg = home_reg.replace('Cardiff City', 'Cardiff')
		home_reg = home_reg.replace('Norwich City', 'Norwich')
		home_reg = home_reg.replace('West Ham United', 'West Ham')
		home_reg = home_reg.replace('Tottenham Hotspur', 'Tottenham')
		home_reg = home_reg.replace('Swansea City', 'Swansea')
		home_reg = home_reg.replace('Stoke City', 'Stoke')
		home_reg = home_reg.replace('Hull City', 'Hull')
		away = cells[2].find(text=True).string.strip()
		away_reg = away.replace('Manchester', 'Man')
		away_reg = away_reg.replace('Newcastle United', 'Newcastle')
		away_reg = away_reg.replace('Cardiff City', 'Cardiff')
		away_reg = away_reg.replace('Norwich City', 'Norwich')
		away_reg = away_reg.replace('West Ham United', 'West Ham')
		away_reg = away_reg.replace('Tottenham Hotspur', 'Tottenham')
		away_reg = away_reg.replace('Swansea City', 'Swansea')
		away_reg = away_reg.replace('Stoke City', 'Stoke')
		away_reg = away_reg.replace('Hull City', 'Hull')

		aux = [date.lstrip('\n'), home_reg.lstrip('\n'), away_reg.lstrip('\n')]
		epl_fixtures.append(aux)


header = ['Date', 'HomeTeam', 'AwayTeam']


c = csv.writer(open('processed_data/fixtures.csv', 'wb'))

c.writerow(header)
for row in epl_fixtures:
	c.writerow(row)






#print epl_fixtures

#now pull it into the correct format using Pandas and calculate the features for each fixture
# df1 = pd.DataFrame(epl_fixtures, columns = header)

# for row in df:
# 	print row
