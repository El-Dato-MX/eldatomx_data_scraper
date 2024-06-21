from nba_api.stats.endpoints import shotchartdetail
from utils.db_connection import connect_to_database
from utils.db_functions import get_player_team_df
from dotenv import load_dotenv
import pandas as pd
from utils.constants import insert_to_player_shotchart_table_query

def get_shot_chart_details(player_id, team_id):
    shotchartdetail_instance = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id)
    return shotchartdetail_instance.get_data_frames()[0]

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

player_team_df = get_player_team_df(cursor)

shot_chart_dfs = []

# Loop through all rows in the DataFrame
for _, row in player_team_df.iterrows():
    player_id = row['PLAYER_ID']
    team_id = row['TEAM_ID']

    # Skip rows where TEAM_ID is 0
    if team_id == 0:
        continue

    # Retrieve and store the shot chart details DataFrame
    shot_chart_df = get_shot_chart_details(player_id, team_id)
    shot_chart_dfs.append(shot_chart_df)

all_shot_chart_details = pd.concat(shot_chart_dfs, ignore_index=True)

# Insert or update data from gleague / nba dataframe into player_shotchart table
for _, row in all_shot_chart_details.iterrows():
    cursor.execute(insert_to_player_shotchart_table_query, (
        row['GRID_TYPE'], row['GAME_ID'], row['GAME_EVENT_ID'], row['PLAYER_ID'], row['TEAM_ID'], row['PERIOD'],
        row['MINUTES_REMAINING'], row['SECONDS_REMAINING'], row['EVENT_TYPE'], row['ACTION_TYPE'], row['SHOT_TYPE'],
        row['SHOT_ZONE_BASIC'], row['SHOT_ZONE_AREA'], row['SHOT_ZONE_RANGE'], row['SHOT_DISTANCE'], row['LOC_X'],
        row['LOC_Y'], row['SHOT_ATTEMPTED_FLAG'], row['SHOT_MADE_FLAG'], row['GAME_DATE'], row['HTM'], row['VTM']
    ))

conn.commit()
conn.close()
