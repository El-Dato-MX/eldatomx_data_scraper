from nba_api.stats.endpoints import teamyearbyyearstats
from utils.db_connection import connect_to_database
from utils.constants import insert_to_team_stats_table_query
from dotenv import load_dotenv
import pandas as pd

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

team_ids = pd.read_csv('unique_team_ids.csv')

for _, row in team_ids.iterrows():
    if row['TEAM_ID'] == 0:
        team_id = 0
        team_abbreviation = 'NA'
        team_nickname = 'NA'
        team_city = 'NA'
    else:
        team_yearly_stats = teamyearbyyearstats.TeamYearByYearStats(row['TEAM_ID']).get_data_frames()[0]
        for _, row in team_yearly_stats.iterrows():
            cursor.execute(insert_to_team_stats_table_query, (
                row['TEAM_ID'], row['TEAM_CITY'], row['TEAM_NAME'], row['YEAR'], row['GP'], row['WINS'], row['LOSSES'],
                row['WIN_PCT'],
                row['CONF_RANK'], row['DIV_RANK'], row['PO_WINS'], row['PO_LOSSES'], row['CONF_COUNT'],
                row['DIV_COUNT'],
                row['NBA_FINALS_APPEARANCE'], row['FGM'], row['FGA'], row['FG_PCT'], row['FG3M'], row['FG3A'],
                row['FG3_PCT'],
                row['FTM'], row['FTA'], row['FT_PCT'], row['OREB'], row['DREB'], row['REB'], row['AST'], row['PF'],
                row['STL'],
                row['TOV'], row['BLK'], row['PTS'], row['PTS_RANK']
            ))

conn.commit()
conn.close()
