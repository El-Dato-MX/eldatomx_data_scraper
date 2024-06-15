from nba_api.stats.endpoints import shotchartdetail
from utils.db_connection import connect_to_database
from utils.db_functions import get_player_team_df
from dotenv import load_dotenv
import pandas as pd

def get_shot_chart_details(player_id, team_id):
    shotchartdetail_instance = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id)
    return shotchartdetail_instance.get_data_frames()[0]

ENVIRONMENT = 'DEV'

insert_DEV_query = '''
INSERT INTO player_shotchart (
    GRID_TYPE,
    GAME_ID,
    GAME_EVENT_ID,
    PLAYER_ID,
    TEAM_ID,
    PERIOD,
    MINUTES_REMAINING,
    SECONDS_REMAINING,
    EVENT_TYPE,
    ACTION_TYPE,
    SHOT_TYPE,
    SHOT_ZONE_BASIC,
    SHOT_ZONE_AREA,
    SHOT_ZONE_RANGE,
    SHOT_DISTANCE,
    LOC_X,
    LOC_Y,
    SHOT_ATTEMPTED_FLAG,
    SHOT_MADE_FLAG,
    GAME_DATE,
    HTM,
    VTM
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    GRID_TYPE = VALUES(GRID_TYPE),
    GAME_ID = VALUES(GAME_ID),
    GAME_EVENT_ID = VALUES(GAME_EVENT_ID),
    PLAYER_ID = VALUES(PLAYER_ID),
    TEAM_ID = VALUES(TEAM_ID),
    PERIOD = VALUES(PERIOD),
    MINUTES_REMAINING = VALUES(MINUTES_REMAINING),
    SECONDS_REMAINING = VALUES(SECONDS_REMAINING),
    EVENT_TYPE = VALUES(EVENT_TYPE),
    ACTION_TYPE = VALUES(ACTION_TYPE),
    SHOT_TYPE = VALUES(SHOT_TYPE),
    SHOT_ZONE_BASIC = VALUES(SHOT_ZONE_BASIC),
    SHOT_ZONE_AREA = VALUES(SHOT_ZONE_AREA),
    SHOT_ZONE_RANGE = VALUES(SHOT_ZONE_RANGE),
    SHOT_DISTANCE = VALUES(SHOT_DISTANCE),
    LOC_X = VALUES(LOC_X),
    LOC_Y = VALUES(LOC_Y),
    SHOT_ATTEMPTED_FLAG = VALUES(SHOT_ATTEMPTED_FLAG),
    SHOT_MADE_FLAG = VALUES(SHOT_MADE_FLAG),
    GAME_DATE = VALUES(GAME_DATE),
    HTM = VALUES(HTM),
    VTM = VALUES(VTM);
'''

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
    if ENVIRONMENT == 'DEV':
        insert_query = insert_DEV_query
    # elif ENVIRONMENT == 'STAGE':
        # insert_query = insert_STAGE_query
    cursor.execute(insert_query, (
        row['GRID_TYPE'], row['GAME_ID'], row['GAME_EVENT_ID'], row['PLAYER_ID'], row['TEAM_ID'], row['PERIOD'],
        row['MINUTES_REMAINING'], row['SECONDS_REMAINING'], row['EVENT_TYPE'], row['ACTION_TYPE'], row['SHOT_TYPE'],
        row['SHOT_ZONE_BASIC'], row['SHOT_ZONE_AREA'], row['SHOT_ZONE_RANGE'], row['SHOT_DISTANCE'], row['LOC_X'],
        row['LOC_Y'], row['SHOT_ATTEMPTED_FLAG'], row['SHOT_MADE_FLAG'], row['GAME_DATE'], row['HTM'], row['VTM']
    ))

conn.commit()
conn.close()
