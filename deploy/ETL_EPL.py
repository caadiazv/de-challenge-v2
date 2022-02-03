import numpy as np
import pandas as pd
import os

DIRECTORY = '/app/'
COLUMNS_TRANSFORM = ['SEASON','TEAM','PTS','GOALS_FOR','GOAL_DIF','SHOTS_ON_TARGET','PE']
COLUMNS_RESULT = ['SEASON','TEAM','PTS','GOALS_FOR','GOAL_DIF','SHOTS_ON_TARGET','PE','POSITION']
AWAY_TEAM = 'AwayTeam'
HOME_TEAM = 'HomeTeam'
FULL_TIME_AWAY_GOALS = 'FTAG'
FULL_TIME_HOME_GOALS = 'FTHG'
FULL_TIME_RESULT = 'FTR'
HOME_SHOTS_TARGET = 'HST'
AWAY_SHOTS_TARGET = 'AST'
AWAY = 'A'
HOME = 'H'
DEUCE = 'D'


def unique_teams(df):
    df_teams = df.HomeTeam.unique()
    return df_teams

def team_goals(df,team):
    goals = df.loc[df[HOME_TEAM] == team,FULL_TIME_HOME_GOALS].sum() + df.loc[df[AWAY_TEAM] == team,FULL_TIME_AWAY_GOALS].sum()
    return goals

def team_goals_dif(df,team):
    goals_team = df.loc[df[HOME_TEAM] == team,FULL_TIME_HOME_GOALS].sum() + df.loc[df[AWAY_TEAM] == team,FULL_TIME_AWAY_GOALS].sum()
    goals_team_o = df.loc[df[HOME_TEAM] == team,FULL_TIME_AWAY_GOALS].sum() + df.loc[df[AWAY_TEAM] == team,FULL_TIME_HOME_GOALS].sum()
    dif_goals = goals_team - goals_team_o
    return dif_goals

def team_shots_on_target(df,team):
    shots_on_target = np.int64(df.loc[df[HOME_TEAM] == team,HOME_SHOTS_TARGET].sum()) + np.int64(df.loc[df[AWAY_TEAM] == team,AWAY_SHOTS_TARGET].sum())
    return shots_on_target[1]

def team_season_points(df,team):
    points = len(df.loc[(df[HOME_TEAM] == team) & (df[FULL_TIME_RESULT] == HOME)])*3 + len(df.loc[(df[AWAY_TEAM] == team) & (df[FULL_TIME_RESULT] == AWAY)])*3 + len(df.loc[(df[HOME_TEAM] == team) & (df[FULL_TIME_RESULT] == DEUCE)]) + len(df.loc[(df[AWAY_TEAM] == team) & (df[FULL_TIME_RESULT] == DEUCE)])
    return points

def team_position(df):
    position = df.sort_values(by=['PTS','GOAL_DIF'],ascending=False)
    position.insert(loc=0,column='POSITION',value=np.arange(len(position))+1)
    return position[['POSITION','TEAM']]

def transform(df,season):
    teams = unique_teams(df)
    result = pd.DataFrame(columns=COLUMNS_TRANSFORM,index=range(len(teams)),dtype=None)
    for i in range(len(teams)):
        goals = team_goals(df,teams[i])
        dif_goals = team_goals_dif(df,teams[i])
        points = team_season_points(df,teams[i])
        shots_on_target = team_shots_on_target(df,teams[i])
        pe = round(goals/shots_on_target,4)
        result.iloc[i] = (season,teams[i],np.int64(points),goals,np.int64(dif_goals),shots_on_target,pe)
    teams_position = team_position(result[['TEAM','PTS','GOAL_DIF']])
    result = result.merge(teams_position, on = 'TEAM', how='left').sort_values(by=['PTS','GOAL_DIF'],ascending=False)
    return result

def extract(df,name_file):
    season = os.path.basename(DIRECTORY+'data/'+name_file).split('_')[0].split('-')[1]
    df_epl = df[['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
    return (df_epl,season)

def load(df):
    df.to_csv(DIRECTORY+'premier_league.csv',index=False)
    return True


if __name__ == "__main__":

    files = os.listdir(DIRECTORY+'data')
    table_epl = pd.DataFrame(columns=COLUMNS_RESULT,dtype=None)
    
    for i in range(len(files)):
        df = pd.read_json(DIRECTORY+'data/'+files[i])

        # Extract
        df_epl,season = extract(df,files[i])

        # Transform
        table_season = transform(df_epl,season)
        table_epl = pd.concat([table_epl,table_season], ignore_index=True)
    
    # Load
    load_finished = load(table_epl)