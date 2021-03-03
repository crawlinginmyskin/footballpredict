import pandas as pd
from data_prep import get_team_stats
import keras
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import numpy as np

with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model('model.h5')


general_df = pd.read_csv('general.csv', index_col=[0])
home_df = pd.read_csv('home.csv', index_col=[0])
away_df = pd.read_csv('away.csv', index_col=[0])


name1 = input('Input the name of the home team')
name2 = input('Input the name of the away team')


team1_stats = get_team_stats(name1, general_df, 1) + get_team_stats(name1, home_df, 0)
team2_stats = get_team_stats(name2, general_df, 1) + get_team_stats(name2, away_df, 0)

model_data = np.array([team1_stats + team2_stats])
result = model.predict(model_data)

print(result)
print(np.argmax(result))
if np.argmax(result) == 0:
	print('draw')
elif np.argmax(result) == 1:
	print(name1)
else:
	print(name2)
	

