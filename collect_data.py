import http.client
import json
import pandas as pd
import time


def get_teams(codes, venue):
	# this functions gets stats from API, inputs it into a dataframe, then returns the dataframe
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = {'X-Auth-Token': 'API-KEY'}
	df = pd.DataFrame()
	for a in codes:
		league_teams = 20
		connection.request('GET', '/v2/competitions/' + a + '/standings', None, headers)
		standings = json.loads(connection.getresponse().read().decode())
		table_raw = standings['standings']
		team_standing = table_raw[venue]['table']
		if a is 'BL1':
			league_teams = 16
		
		for i in range(0, league_teams):
			form = team_standing[i]['form']
			name = team_standing[i]['team']['name']
			formscore = 0
			if venue == 0:
				for j in form:
					# encoding form based on last 5 matches - win equals 1 point, draw equals 0.5 points, lose equals 0 points
					if j is 'W':
						formscore += 1
					elif j is 'D':
						formscore += 0.5
				
				data = [name, formscore, team_standing[i]['won'], team_standing[i]['draw'],
				        team_standing[i]['lost'],
				        team_standing[i]['goalsFor'], team_standing[i]['goalsAgainst']]
			else:
				data = [name, team_standing[i]['won'], team_standing[i]['draw'],
				        team_standing[i]['lost'],
				        team_standing[i]['goalsFor'], team_standing[i]['goalsAgainst']]
			df = df.append([data])
	return df


def get_matches(codes):
	# this function gets all matches that were played this season
	headers = {'X-Auth-Token': 'API-KEY'}
	data_connection = http.client.HTTPConnection('api.football-data.org')
	matches_df = pd.DataFrame()
	league_matches = 380
	for i in codes:
		if i is 'BL1':
			league_matches = 306
		data_connection.request('GET', '/v2/competitions/' + i + '/matches', None, headers)
		matches = json.loads(data_connection.getresponse().read().decode())
		matches_raw = matches['matches']
		for j in range(0, league_matches):
			if matches_raw[j]['score']['winner']:
				data = [matches_raw[j]['homeTeam']['name'],
				        matches_raw[j]['awayTeam']['name'],
				        matches_raw[j]['score']['winner']]
				matches_df = matches_df.append([data])
		
	return matches_df
		

league_codes = ['PL', 'BL1', 'SA', 'PD', 'FL1']

column_labels = {0: 'name',
                 1: 'form',
                 2: 'won',
                 3: 'draw',
                 4: 'lost',
                 5: 'goalsFor',
                 6: 'goalsAgainst'}

df = get_teams(league_codes, 0)
time.sleep(60)
home_df = get_teams(league_codes, 1)
time.sleep(60)
away_df = get_teams(league_codes, 2)
time.sleep(60)

matches = get_matches(league_codes)
matches.reset_index(drop=True, inplace=True)

matches.to_csv('matches.csv')

df.reset_index(drop=True, inplace=True)
home_df.reset_index(drop=True, inplace=True)
away_df.reset_index(drop=True, inplace=True)

df.to_csv('general.csv')
home_df.to_csv('home.csv')
away_df.to_csv('away.csv')
