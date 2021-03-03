import pandas as pd


def get_team_stats(name, df, mode):
	for a in range(len(df.index)):
		if df.iloc[a][0] == name:
			if mode is 1:
				return [df.iloc[a][b] for b in range(1, 7)]
			else:
				return [df.iloc[a][b] for b in range(1, 6)]


if __name__ == '__main__':
	matches_df = pd.read_csv('matches.csv', index_col=[0])
	
	general_df = pd.read_csv('general.csv', index_col=[0])
	home_df = pd.read_csv('home.csv', index_col=[0])
	away_df = pd.read_csv('away.csv', index_col=[0])
	
	to_model_df = pd.DataFrame()
	
	for i in range(len(matches_df.index)):
		home_team_name = matches_df.iloc[i][0]
		away_team_name = matches_df.iloc[i][1]
		if matches_df.iloc[i][2] == 'HOME_TEAM':
			result = [1]
		elif matches_df.iloc[i][2] == 'AWAY_TEAM':
			result = [2]
		else:
			result = [0]
			
		home_team_stats = get_team_stats(home_team_name, general_df, 1) + get_team_stats(home_team_name, home_df, 0)
		away_team_stats = get_team_stats(away_team_name, general_df, 1) + get_team_stats(away_team_name, away_df, 0)
		match_stats = home_team_stats + away_team_stats + result
		to_model_df = to_model_df.append([match_stats])
		
	to_model_df.to_csv('model_input.csv')
